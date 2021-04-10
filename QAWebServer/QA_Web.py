import asyncio

import tornado
#from terminado import SingleTermManager, TermSocket
from tornado.options import (define, options, parse_command_line,
                             parse_config_file)
from tornado.web import Application, RequestHandler, authenticated
from tornado_http2.server import Server

from QAWebServer.basehandles import QABaseHandler

__version__ = "1.410.001"


class INDEX(QABaseHandler):

    def get(self):
        self.write(
            {
                'status': 200,
                'message': 'This is a welcome page for quantaxis backend',
                'github_page':
                    'https://github.com/yutiansut/QUANTAXIS_WEBSERVER/blob/master/backendapi.md',
                'url': [item[0] for item in handlers]
            }
        )

handlers = [
    (r"/",
         INDEX),
]

def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    define("port", default=8010, type=int, help="服务器监听端口号")

    define("address", default='0.0.0.0', type=str, help='服务器地址')
    define("content", default=[], type=str, multiple=True, help="控制台输出内容")

    parse_command_line()
    port = options.port
    address = options.address

    start_server(handlers, address, port)

def start_server(handlers, address, port):
    apps = Application(
        handlers=handlers,
        debug=True,
        autoreload=True,
        compress_response=True
    )
    http_server = Server(apps)
    print('========WELCOME QUANTAXIS_WEBSERVER============')
    print('QUANTAXIS VERSION: {}'.format(__version__))
    print('QUANTAXIS WEBSERVER is Listening on: http://localhost:{}'.format(port))
    print('请打开浏览器/使用JavaScript等来使用该后台, 并且不要关闭当前命令行窗口')
    http_server.bind(port=port, address=address)
    """增加了对于非windows下的机器多进程的支持
    """
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()