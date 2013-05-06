import sae
import tornado.wsgi

from blog import urls as blogurls
from admin import urls as adminurls

saeurls = blogurls + adminurls

settings = {
    'debug': True,
    'cookie_secret': '7nVA0WeZSJSzTCUF8UZB/C3OfLrl7k26iHxfnVa9x0I=',
    'login_url': "/login",
    #'gzip': True,
}

app = tornado.wsgi.WSGIApplication(saeurls, **settings)

application = sae.create_wsgi_app(app)
