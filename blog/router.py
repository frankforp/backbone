# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by lwz7512
# @2016/05/17

import tornado.web

from foo import comm
from foo.auth import auth_account
from foo.ajax import ajax_auth
from foo.ajax import ajax_article
from foo.blog import blog_article


def map():

    config = [

        # GET: 根据 HTTP header 收集客户端相关信息：是否手机、操作系统、浏览器等信息。
        (r'/', getattr(blog_article, 'BlogArticleIndexHandler')),

        # auth
        ('/login', getattr(auth_account, 'AuthLoginHandler')),
        ('/logout', getattr(auth_account, 'AuthLogoutHandler')),
        ('/register', getattr(auth_account, 'AuthRegisterHandler')),
        ('/lost-pwd', getattr(auth_account, 'AuthLostPwdHandler')),
        ('/profile', getattr(auth_account, 'AuthProfileHandler')),
        ('/profile-edit', getattr(auth_account, 'AuthProfileEditHandler')),
        ('/avatar-edit', getattr(auth_account, 'AuthAvatarEditHandler')),

        ('/ajax/verify-code', getattr(ajax_auth, 'AjaxAuthVerifyCodeXHR')),

        # blog
        ('/blog/articles', getattr(blog_article, 'BlogArticleIndexHandler')),
        ('/blog/articles/create', getattr(blog_article, 'BlogArticleCreateHandler')),
        ('/blog/articles/mine', getattr(blog_article, 'BlogArticleMineHandler')),
        ('/blog/articles/([a-z0-9]*)', getattr(blog_article, 'BlogArticleHandler')),

        # ajax
        ('/ajax/blog/accounts/([a-z0-9]*)/articles', getattr(ajax_article, 'AjaxAccountArticleXHR')),

        # comm
        ('.*', getattr(comm, 'PageNotFoundHandler'))

    ]

    return config