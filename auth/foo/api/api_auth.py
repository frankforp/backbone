#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
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
import hashlib
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from bson import json_util
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from global_const import *
from dao import auth_login_dao
from dao import auth_account_dao
from dao import auth_access_token_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat
from bson import json_util


# 密码模式（Resource Owner Password Credentials Grant）中，用户向客户端提供自己的用户名和密码。
# 客户端使用这些信息，向"服务商提供商"索要授权。
#
# 在这种模式中，用户必须把自己的密码给客户端，但是客户端不得储存密码。
# 这通常用在用户对客户端高度信任的情况下，比如客户端是操作系统的一部分，或者由一个著名公司出品。
# 而认证服务器只有在其他授权模式无法执行的情况下，才能考虑使用这种模式。
class ApiAuthTokenXHR(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logging.info(self.request)
        logging.info(self.request.body)
        _body = json_decode(self.request.body)
        grant_type = _body['grant_type']
        logging.info("got grant_type %r", grant_type)

        if grant_type is None:
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return
        elif grant_type == 'password':
            username = _body['username']
            logging.info("got username %r", username)
            md5pwd = _body['password'] # 使用md5加密后的字符串

            if username is None or username == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

            if md5pwd is None or md5pwd == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

            _login = auth_login_dao.auth_login_dao().query_not_safe(username)
            if not _login:
                self.set_status(404) # Not Found
                self.write('login & password pair are wrong')
                self.finish()
                return

            _timestamp = int(time.time())
            logging.info("timestamp %r", _timestamp)
            salt = _login['salt']
            _hash_pwd = hash_pwd(md5pwd, salt)
            if _hash_pwd != _login['hash_pwd']:
                self.set_status(404) # Not Found
                self.write('login & password pair are wrong')
                self.finish()
                return

            access_token = generate_uuid_str()
            token_type = "session"
            expires_at = _timestamp + EXPIRES_IN # expires_in 7200s
            refresh_token = generate_uuid_str()
            scope = "all"
            _json = {'_id':access_token, 'token_type':token_type,
                    'expires_at':expires_at,
                    'refresh_token':refresh_token,
                    'account_id':_login['account_id'],
                    'scope':scope}
            auth_access_token_dao.auth_access_token_dao().create(_json)

            self.set_status(200) # OK
            token = {
                "access_token":access_token,
                "token_type":"session",
                "expires_in":EXPIRES_IN,
                "refresh_token":refresh_token
            }
            logging.info("got response %r", token)

            self.finish(JSON.dumps(token))
            return
        elif grant_type == 'refresh':
            refresh_token = _body['refresh_token']
            logging.info("got refresh_token %r", refresh_token)

            if refresh_token is None or refresh_token == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

            token = auth_access_token_dao.auth_access_token_dao().query_by_refresh(refresh_token)
            if token is None:
                self.set_status(404) # Not Found
                self.write('Not Found')
                self.finish()
                return

            _timestamp = int(time.time())
            access_token = generate_uuid_str()
            token_type = "session"
            expires_at = _timestamp + EXPIRES_IN # expires_in 7200s
            refresh_token = generate_uuid_str()
            scope = "all"
            _json = {'_id':access_token, 'token_type':token_type,
                    'expires_at':expires_at,
                    'refresh_token':refresh_token,
                    'account_id':token['account_id'],
                    'scope':scope}
            auth_access_token_dao.auth_access_token_dao().create(_json)

            self.set_status(200) # OK
            token = {
                "access_token":access_token,
                "token_type":"session",
                "expires_in":EXPIRES_IN,
                "refresh_token":refresh_token
            }
            logging.info("got response %r", token)
            self.finish(JSON.dumps(token))
            return
        elif grant_type == 'delete':
            access_token = _body['access_token']
            logging.info("got access_token %r", access_token)
            if access_token is None or access_token == "":
                self.set_status(403) # Forbidden
                self.write('Forbidden')
                self.finish()
                return

            auth_access_token_dao.auth_access_token_dao().delete(access_token)

            self.set_status(200) # OK
            self.finish('OK')
            return
        else: # default, could also just omit condition or 'if True'
            #raise tornado.web.HTTPError(400)
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return


# 创建账号
class ApiAuthAccountXHR(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logging.info(self.request)
        logging.info(self.request.body)
        _body = json_decode(self.request.body)

        grant_type = _body['grant_type']
        logging.info("got grant_type %r", grant_type)

        if grant_type is None:
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return
        elif grant_type == 'create':
            username = _body['username']
            logging.info("got username %r", username)
            md5pwd = _body['password'] # 使用md5加密后的字符串

            if username is None or username == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return
            if md5pwd is None or md5pwd == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

            _login = auth_login_dao.auth_login_dao().query_not_safe(username)
            if _login:
                logging.info("_login %r", _login['_id'])
                self.set_status(409) # Conflict
                self.write('Conflict')
                self.finish()
                return

            _timestamp = int(time.time())
            logging.info("timestamp %r", _timestamp)
            account_id = generate_uuid_str()
            _json = {'_id':account_id, 'create_time':_timestamp}
            auth_account_dao.auth_account_dao().create(_json)

            salt = generate_nonce_str()
            _hash_pwd = hash_pwd(md5pwd, salt)
            _json = {'_id':username, 'hash_pwd':_hash_pwd, 'salt':salt,
                    'account_id':account_id,
                    'create_time':_timestamp}
            auth_login_dao.auth_login_dao().create(_json)

            self.set_status(201) # Created
            account = {
                "account_id":account_id
            }
            logging.info("got account response %r", account)

            self.finish(JSON.dumps(account))
            return
        else: # default, could also just omit condition or 'if True'
            #raise tornado.web.HTTPError(400)
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        logging.info(self.request)
        access_token = self.get_argument("access_token", "")
        logging.info("got access_token %r", access_token)
        grant_type = self.get_argument("grant_type", "")
        logging.info("got grant_type %r", grant_type)

        if grant_type is None:
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return
        elif grant_type == 'read':
            if access_token is None or access_token == "":
                self.set_status(403) # Forbidden
                self.write('Forbidden')
                self.finish()
                return

            token = auth_access_token_dao.auth_access_token_dao().query(access_token)
            if token is None:
                self.set_status(403) # Forbidden
                self.write('Forbidden')
                self.finish()
                return

            account_id = token['account_id']
            logging.info("got account_id %r", account_id)
            account = auth_account_dao.auth_account_dao().query(account_id)
            if account is None:
                self.set_status(404) # Not Found
                self.write('Not Found')
                self.finish()
                return

            self.finish(JSON.dumps(account))
            return
        else: # default, could also just omit condition or 'if True'
            #raise tornado.web.HTTPError(400)
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        logging.info(self.request)
        logging.info(self.request.body)
        _body = json_decode(self.request.body)

        grant_type = _body['grant_type']
        logging.info("got grant_type %r", grant_type)

        if grant_type is None:
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return
        elif grant_type == 'write':
            nickname = _body['nickname']
            avatar = _body['avatar']
            logging.info("got nickname %r", nickname)
            logging.info("got avatar %r", avatar)
            if nickname is None or nickname == "":
                self.set_status(400) # Bad Request
                self.write('Bad Request')
                self.finish()
                return

            access_token = _body['access_token']
            logging.info("got access_token %r", access_token)
            if access_token is None or access_token == "":
                self.set_status(403) # Forbidden
                self.write('Forbidden')
                self.finish()
                return

            token = auth_access_token_dao.auth_access_token_dao().query(access_token)
            if token is None:
                self.set_status(403) # Forbidden
                self.write('Forbidden')
                self.finish()
                return

            account_id = token['account_id']
            logging.info("got account_id %r", account_id)

            _timestamp = int(time.time())
            if not avatar:
                _json = {"_id":account_id, "nickname":nickname, "last_update_time":_timestamp}
                auth_account_dao.auth_account_dao().update(_json)
            else:
                _json = {"_id":account_id, "nickname":nickname, "avatar":avatar,
                        "last_update_time":_timestamp}
                auth_account_dao.auth_account_dao().update(_json)

            self.set_status(200) # OK
            self.finish('OK')
            return
        else: # default, could also just omit condition or 'if True'
            #raise tornado.web.HTTPError(400)
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return


# 创建忘记密码的验证码
# 使用 sup-http proxy 实现, sup-http仍调用sendcloud
class ApiAuthVcodeXHR(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logging.info(self.request)
        logging.info(self.request.body)
        _body = json_decode(self.request.body)

        phone = _body['phone']
        logging.info("got phone %r", phone)
        if phone is None or phone == "":
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return

        _login = auth_login_dao.auth_login_dao().query_not_safe(phone)
        if not _login:
            self.set_status(404) # Not Found
            self.write('Not Found')
            self.finish()
            return

        _timestamp = int(time.time())
        last_time = 0
        try:
            last_time = int(_login['last_apply_vcode_time'])
        except: # Not found last_apply_vcode_time
            logging.warn("no found last_apply_vcode_time")
        logging.info("got timestamp %d last_time %d", _timestamp, last_time)
        if _timestamp > last_time and _timestamp < (last_time + 300): # ttl is 5 minutes
            self.set_status(200) # No Content
            self.write('OK')
            self.finish()
            return

        # store phone verify code
        vcode = generate_verify_code()
        logging.info("got verify_code %r", vcode)
        _json = {"_id":phone, "vcode":vcode, "last_update_time":_timestamp,
                "last_apply_vcode_time":_timestamp, "counts":0}
        auth_login_dao.auth_login_dao().update(_json)

        # Logic: send sms by sup-http
        param = {'phone':phone, 'ekey':vcode }
        headers = {'content-type': 'application/json'}
        _json = json_encode(param)
        logging.info("post body %r", _json)
        http_client = HTTPClient()
        response = None
        try:
            response = http_client.fetch("http://localhost:8080/sendcloud/sms",
                    method="POST", headers=headers, body=_json)
            logging.info("got sup-http sms response %r", response.body)
        except HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logging.error("sup-http sms error: %r", str(e))
            self.set_status(500) # Internal Server Error
            self.write(str(e))
            self.finish()
        except Exception as e:
            # Other errors are possible, such as IOError.
            logging.error("sup-http sms error: %r", str(e))
            self.set_status(500) # Internal Server Error
            self.write(str(e))
            self.finish()
        else:
            # if no exception,get here
            self.set_status(200) # OK
            self.write(response.body)
            self.finish()
        finally:
            http_client.close()

        return


# 创建忘记密码的验证码
# 使用sendcloud实现
# class ApiSendCloudVcodeXHR(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     @tornado.gen.coroutine
#     def post(self):
#         logging.info(self.request)
#         logging.info(self.request.body)
#         _body = json_decode(self.request.body)
#
#         phone = _body['phone']
#         logging.info("got phone %r", phone)
#         if phone is None or phone == "":
#             self.set_status(400) # Bad Request
#             self.write('Bad Request')
#             self.finish()
#             return
#
#         _login = auth_login_dao.auth_login_dao().query_not_safe(phone)
#         if not _login:
#             self.set_status(404) # Not Found
#             self.write('Not Found')
#             self.finish()
#             return
#
#         _timestamp = int(time.time())
#         logging.info("got timestamp %d", _timestamp)
#         try:
#             last_time = int(_login['last_apply_vcode_time'])
#             logging.info("got last_time %d", last_time)
#             if (_timestamp > last_time) and (_timestamp < last_time + 300): # ttl is 5 minutes
#                 self.set_status(204) # No Content
#                 self.write('No Content')
#                 self.finish()
#                 return
#         except: # Not found last_apply_vcode_time
#             logging.info("no found last_time")
#
#         # store phone verify code
#         vcode = generate_verify_code()
#         logging.info("got verify_code %r", vcode)
#         _json = {"_id":phone, "vcode":vcode, "last_update_time":_timestamp,
#                 "last_apply_vcode_time":_timestamp, "counts":0}
#         auth_login_dao.auth_login_dao().update(_json)
#
#         # Logic: send sms by sendcloud
#         param = {
#             'smsUser': SMS_USER,
#             'templateId': 151,
#             'msgType': 0,
#             'phone': phone,
#             'vars': {'%ekey%': vcode},
#         }
#         sign = generate_sms_sign(SMS_KEY, param)
#         param['signature'] = sign
#
#         headers = {'content-type': 'application/json'}
#         _json = json_encode(param)
#         logging.info("post body %r", _json)
#         http_client = HTTPClient()
#         response = None
#         try:
#             response = http_client.fetch(SMS_URL,
#                     method="POST", headers=headers, body=_json)
#             logging.info("got sendcloud sms response %r", response.body)
#         except httpclient.HTTPError as e:
#             # HTTPError is raised for non-200 responses; the response
#             # can be found in e.response.
#             logging.error("sendcloud sms error: %r", str(e))
#             self.set_status(500) # Internal Server Error
#             self.write(str(e))
#             self.finish()
#         except Exception as e:
#             # Other errors are possible, such as IOError.
#             logging.error("sendcloud sms error: %r", str(e))
#             self.set_status(500) # Internal Server Error
#             self.write(str(e))
#             self.finish()
#         else:
#             # if no exception,get here
#             self.set_status(200) # OK
#             self.write('OK')
#             self.finish()
#         finally:
#             http_client.close()
#
#         return


# 忘记密码后修改密码
class ApiAuthLostPwdXHR(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logging.info(self.request)
        logging.info(self.request.body)
        _body = json_decode(self.request.body)

        phone = _body['phone']
        logging.info("got phone %r", phone)
        if phone is None or phone == "":
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return

        vcode = _body['vcode']
        logging.info("got vcode %r", vcode)
        if vcode is None or vcode == "":
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return

        md5pwd = _body['password']
        if md5pwd is None or md5pwd == "":
            self.set_status(400) # Bad Request
            self.write('Bad Request')
            self.finish()
            return

        _login = auth_login_dao.auth_login_dao().query_not_safe(phone)
        if not _login:
            self.set_status(404) # Not Found
            self.write('Not Found')
            self.finish()
            return

        try:
            if vcode != _login['vcode']:
                self.set_status(401) # Unauthorized
                self.write('Unauthorized')
                self.finish()
                return
        except: # Not found vcode
            self.set_status(401) # Unauthorized
            self.write('Unauthorized')
            self.finish()
            return

        _timestamp = int(time.time())
        try:
            if _timestamp > int(_login['last_apply_vcode_time']) + 300: # ttl is 5 minutes
                self.set_status(408) # Request Timeout
                self.write('Request Timeout')
                self.finish()
                return
        except: # Not found last_apply_vcode_time
            self.set_status(401) # Unauthorized
            self.write('Unauthorized')
            self.finish()
            return

        # store new password & salt
        salt = generate_nonce_str()
        _hash_pwd = hash_pwd(md5pwd, salt)
        _json = {'_id':phone, 'hash_pwd':_hash_pwd, 'salt':salt,
                'last_update_time':_timestamp}
        auth_login_dao.auth_login_dao().update(_json)

        self.set_status(200) # OK
        self.write('OK')
        self.finish()
        return
