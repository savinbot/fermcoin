import cherrypy
import requests
import telebot


host = '127.0.0.1'
port = 443
listen = '0.0.0.0'
ssl_cert = 'webhook_cert.pem'
ssl_priv = 'webhook_pkey.pem'


bot_1_token = 'API_TOKEN'   # botcoins_bot
bot_1_address = 'http://127.0.0.1:7771'
bot_1 = telebot.TeleBot(bot_1_token)


class WebhookServer(object):
    @cherrypy.expose
    def botcoins_bot(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            requests.post(bot_1_address, data=json_string)
            return ''
        else:
            raise cherrypy.HTTPError(403)


if __name__ == '__main__':
    bot_1.remove_webhook()
    bot_1.set_webhook(url='https://127.0.0.1/botcoins_bot', certificate=open(ssl_cert, 'r'))

    cherrypy.config.update({
        'server.socket_host': listen,
        'server.socket_port': port,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': ssl_cert,
        'server.ssl_private_key': ssl_priv,
        'engine.autoreload.on': True,
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
