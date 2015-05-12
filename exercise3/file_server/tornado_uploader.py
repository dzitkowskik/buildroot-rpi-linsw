#!/usr/bin/python
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.options
import tornado
import tornado.ioloop
import tornado.web
import os, uuid

__UPLOADS__ = "/tmp/"

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class Mainform(BaseHandler):
    def get(self):
        items = []
        for filename in os.listdir(__UPLOADS__):
            items.append(filename)
        self.render("fileuploadform.html", items=items)

class Upload(BaseHandler):
    def post(self):
	if not self.current_user: self.redirect(u"/login/")
	username = tornado.escape.xhtml_escape(self.current_user)
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        fh = open(__UPLOADS__ + fname, 'w')
        fh.write(fileinfo['body'])
        backButton = '<input type="button" value="Go Back From Whence You Came!" onclick="history.back(-1)" />'
        successPage = "{0} is uploaded by {1}, check {2} folder".format(fname, str(username), __UPLOADS__)
        self.finish(successPage + backButton)

class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)
 
    def check_permission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        return False
 
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect(u"/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login/" + error_msg)
 
    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")

settings = {
    "cookie_secret": 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM=',
    "debug": True,
    "login_url": "/login/",
}

application = tornado.web.Application([
    (r"/", Mainform),
    (r"/upload", Upload),
    (r"/download/(.*)",tornado.web.StaticFileHandler,{'path':__UPLOADS__}),
    (r"/login", AuthLoginHandler),
    (r"/login/", AuthLoginHandler),
    (r"/logout", AuthLogoutHandler),
   (r"/logout/", AuthLogoutHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

