#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 planc2c.com
# thomas@time2box.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import uuid
import smtplib
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util
from tornado.escape import json_decode
from tornado.escape import json_encode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from dao import kit_dao
from wx import wx_wrap
from global_const import *


class IndexHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)

        self.render('index.html')


class ApiKitHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info(self.request)
        before = self.get_argument("before", '0')
        logging.info("got before %r", before)
        if before == '':
            before = time.time()
        else:
            before = float(before)
        limit = 20
        logging.info("got before %r limit %r", before, limit)

        _array = kit_dao.kit_dao().query_pagination(before, limit)

        docs_list = list(_array)
        self.write(JSON.dumps(docs_list, default=json_util.default))
        self.finish()

    def post(self):
        logging.info(self.request)

        app = self.get_argument("app", "")
        name = self.get_argument("name", "")
        email = self.get_argument("email", "")
        message = self.get_argument("message", "")
        app = app.encode("utf-8")
        name = name.encode("utf-8")
        email = email.encode("utf-8")
        message = message.encode("utf-8")
        logging.info("got app %r", app)
        logging.info("got name %r", name)
        logging.info("got email %r", email)
        logging.info("got message %r", message)

        if not app:
            try:
                req_body = json_decode(self.request.body)
                app = req_body['app']
                name = req_body['name']
                email = req_body['email']
                message = req_body['message']
                app = app.encode("utf-8")
                name = name.encode("utf-8")
                email = email.encode("utf-8")
                message = message.encode("utf-8")
                if not app or not name or not email or not message:
                    logging.warn("Bad Request(400): create kit req_body=[%r]", self.request.body)
                    self.set_status(400) # Bad Request
                    self.write('Bad Request')
                    self.finish()
                    return
            except:
                logging.warn("Bad Request(400): create kit req_body=[%r]", self.request.body)
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

        # save message into mongodb
        timestamp = time.time()
        _id = generate_uuid_str()
        _json = {'_id':_id, 'app':app, 'name':name, 'email':email, 'message':message,
                'create_time':timestamp}
        kit_dao.kit_dao().create(_json)

        # save message into file
        # _id = str(uuid.uuid1()).replace('-', '')
        # _date = timestamp_date(time.time())
        # path = cur_file_dir()
        # logging.info("got path %r", path)
        # filename = path + '/static/mail/' + _date + '/' + _id
        # logging.info("got filename %r", filename)
        # if not os.path.exists(path + "/static/mail/" + _date):
        #     os.makedirs(path + "/static/mail/" + _date)
        # content = 'from: ' + name + '\n' \
        #         + 'email: ' + email + '\n' \
        #         + 'message: ' + message
        # logging.info("got content %r", content)
        # f = file(filename,'w')
        # f.write(content)
        # f.close()
        # send mail by smtp
        # os.system('mail -s "kits notify" thomas.zh@qq.com < ' + filename)

        # send message to wx 公众号客户 by template
        wx_access_token = wx_wrap.getAccessTokenByClientCredential(WX_APP_ID, WX_APP_SECRET)
        logging.info("got wx_access_token %r", wx_access_token)
        # openid = 店小二openid
        openid = "oy0Kxt7zNpZFEldQmHwFF-RSLNV0"
        wx_wrap.sendWorkflowMessage(wx_access_token, openid, _id, app, name, email, message, timestamp)

        self.write("SUCCESS")
        self.finish()


class SysErrorHandle(tornado.web.RequestHandler):
    def get(self, error_id):
        logging.info(self.request)
        logging.info("got error_id %r in uri", error_id)

        data = kit_dao.kit_dao().query(error_id)
        data['create_time'] = timestamp_datetime(data['create_time'])

        self.render('sys-error.html', sys_error=data)


class WorkflowHandle(tornado.web.RequestHandler):
    def get(self, workflow_id):
        logging.info(self.request)
        logging.info("got workflow_id %r in uri", workflow_id)

        data = kit_dao.kit_dao().query(workflow_id)
        data['create_time'] = timestamp_datetime(data['create_time'])
        logging.info("got workflow %r", data)

        self.render('workflow.html', data=data)


class ApiSysErrorHandle(tornado.web.RequestHandler):
    def post(self):
        logging.info(self.request)

        app = self.get_argument("app", "")
        sys = self.get_argument("sys", "")
        level = self.get_argument("level", "")
        message = self.get_argument("message", "")
        app = app.encode("utf-8")
        sys = sys.encode("utf-8")
        level = level.encode("utf-8")
        message = message.encode("utf-8")
        logging.info("got app %r", app)
        logging.info("got sys %r", sys)
        logging.info("got level %r", level)
        logging.info("got message %r", message)

        # save message into mongodb
        timestamp = time.time()
        _id = generate_uuid_str()
        _json = {'_id':_id,
                'app':app, 'sys':sys, 'level':level, 'message':message,
                'create_time':timestamp}
        kit_dao.kit_dao().create(_json)

        # send message to wx 公众号客户 by template
        wx_access_token = wx_wrap.getAccessTokenByClientCredential(WX_APP_ID, WX_APP_SECRET)
        logging.info("got wx_access_token %r", wx_access_token)
        # openid = 店小二openid
        openid = "oy0Kxt7zNpZFEldQmHwFF-RSLNV0"
        wx_wrap.sendSysErrorMessage(wx_access_token, openid, _id, app, sys, level, message, timestamp)

        self.write("SUCCESS")
        self.finish()
