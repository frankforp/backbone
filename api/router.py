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

from foo import comm
from foo.api import api_auth
from foo.api import blog_article


def map():

    config = [
        # 登录
        # 删除（登出）
        # 检验授权凭证（access_token）是否有效
        ('/auth/token', getattr(api_auth, 'AuthTokenXHR')),
        # 刷新（代替重新登录）
        ('/auth/refresh-token', getattr(api_auth, 'AuthRefreshTokenXHR')),
        # 注册
        ('/auth/basic', getattr(api_auth, 'AuthBasicXHR')),
        # 查询用户账号基本信息
        # 修改用户账号基本信息
        ('/auth/basic/([a-z0-9]*)', getattr(api_auth, 'AuthBasicXHR')),
        # 获取验证码
        ('/auth/verify-code', getattr(api_auth, 'AuthVerifyCodeXHR')),
        # 修改密码
        ('/auth/pwd', getattr(api_auth, 'AuthPwdXHR')),

        # 创建文章
        # 查询博客文章列表
        ('/blog/articles', getattr(blog_article, 'BlogAritcleIndexXHR')),
        # 查询某人博客文章列表
        ('/blog/accounts/([a-z0-9]*)/articles', getattr(blog_article, 'BlogAccountAritclesXHR')),
        # 查询文章详情
        # 删除文章
        # 修改文章
        ('/blog/articles/([a-z0-9]*)', getattr(blog_article, 'BlogAritcleXHR')),
        # 发布文章
        ('/blog/articles/([a-z0-9]*)/pub', getattr(blog_article, 'BlogAritclePubXHR')),
        # 修改文章段落内容
        ('/blog/articles/([a-z0-9]*)/paragraphs', getattr(blog_article, 'BlogAritcleGaragraphXHR')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config
