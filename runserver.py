#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

# 启动脚本
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SinDB.settings")
import django.conf
import django.contrib.auth
import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application
import django.db

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
# from tornado.netutil import bind_unix_socket
from tornado.options import options, define

define('port', type=int, default=8000)


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    tornado_app = tornado.web.Application(
        [
            (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], **settings)

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    # socket = bind_unix_socket("/opt/SinAlarm/SinAlarm.sock", mode=0777)
    # tornado.process.fork_processes(4)
    # server.add_socket(socket)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    print("已启动SinDB 服务,启动端口为%d"%options.port)
    main()