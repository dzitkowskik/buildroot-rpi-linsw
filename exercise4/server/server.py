#!/usr/bin/python
import json
import os

import tornado.escape
import tornado
import tornado.ioloop
import tornado.web

from player import MPG123Player

__UPLOADS__ = "/tmp/uploads/"
mp3 = MPG123Player()

class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")


class PlayPage(BaseHandler):
    def get(self):
        items = []
        for filename in os.listdir(__UPLOADS__):
            items.append(filename)
        self.render("views/play.html", items=items, working=mp3.working)

    def post(self):
        global mp3
        actionName = self.request.arguments['action'][0];
        if actionName == 'play':
            fileName = self.request.arguments['file'][0];
            pathToFile = os.path.join(__UPLOADS__, fileName);
            if os.path.isfile(pathToFile):
                mp3.play(pathToFile)
        elif actionName == 'pause':
            mp3.pause()
        elif actionName == 'stop':
            mp3.stop()
        elif actionName == 'forward':
            mp3.jump('+75')
        elif actionName == 'backward':
            mp3.jump('-25')
        else:
            self.write(json.dumps({"success", "false"}))
        self.write(json.dumps({"success": "true"}))

class UploadPage(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        self.render("views/upload.html")

    @tornado.web.authenticated
    def post(self):
        fileinfo = self.request.files['file'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        fh = open(__UPLOADS__ + fname, 'w')
        fh.write(fileinfo['body'])
        self.write(json.dumps({"success": "true"}))

class ManagePage(BaseHandler):
    def get(self):
        items = []
        for filename in os.listdir(__UPLOADS__):
            items.append(filename)
        self.render("views/manage.html", items=items)

    def post(self):
        fileName = self.request.arguments['file'][0];
        pathToFile = os.path.join(__UPLOADS__, fileName);
        if os.path.isfile(pathToFile):
            os.remove(pathToFile)
        self.redirect(u"/manage")

class ContactPage(BaseHandler):
    def get(self):
        self.render("views/contact.html")

class AuthLoginHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        try:
            error_message = self.get_argument("error")
        except:
            error_message = ""
        self.render("views/login.html", errormessage=error_message)

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
            self.redirect(u"/upload")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class AuthLogoutHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")

settings = {
    "cookie_secret": 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM=',
    "debug": True,
    "login_url": "/login",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", PlayPage),
    (r"/upload", UploadPage),
    (r"/manage", ManagePage),
    (r"/contact", ContactPage),
    (r"/downloadFile/(.*)", tornado.web.StaticFileHandler, {'path': __UPLOADS__}),
    (r"/login/*", AuthLoginHandler),
    (r"/logout", AuthLogoutHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    if not os.path.exists(__UPLOADS__): os.makedirs(__UPLOADS__)
    try:
        mp3.start()
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
    finally:
        mp3.quit()
        print("Bye bye!")