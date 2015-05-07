#!/usr/bin/python
import tornado
import tornado.ioloop
import tornado.web
import os, uuid

__UPLOADS__ = "/tmp/"

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")

class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

#define pins
LEDS=[17,18,23,24]
SWS=[10,22,27]
#Export pins
for i in LEDS+SWS:
  os.system("echo "+str(i)+" > /sys/class/gpio/export")
#Set LEDS to outputs and switch them off
for i in LEDS:
  os.system("echo low > /sys/class/gpio/gpio"+str(i)+'/direction')
os.system("echo high > /sys/class/gpio/gpio18/direction")

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        led_state={}
        switch_state={}
        #Read state of leds
        for i in LEDS:
            led_state[i]=int(open('/sys/class/gpio/gpio'+str(i)+'/value','r').read())
        #Read state of switches
        for i in SWS:
            switch_state[i]=int(open('/sys/class/gpio/gpio'+str(i)+'/value','r').read())
        resp='<html><body>'
        resp+='<form action="/" method="post">'
        for i in LEDS:
          print led_state[i]
          if led_state[i] == 1:
             state1=' checked ="checked" '
             state2=''
          else:
             state1=''
             state2=' checked ="checked" '
          resp+='<input type="radio" name="L'+str(i)+'" value="0" '+state2+'"/> Off '
          resp+='<input type="radio" name="L'+str(i)+'" value="1" '+state1+'"/> On L'+str(i)+'<p>'
        for i in SWS:
          resp+='Switch '+str(i)+': '+str(switch_state[i])+'<p>'
        resp+='<input type="submit" value="Submit">'
        resp+='</form></body></html>'
        print resp
        self.write(resp)

    def post(self):
        #self.set_header("Content-Type", "text/plain")
        #self.write("You wrote " + self.get_argument("message"))
        for i in LEDS:
            v=self.get_argument("L"+str(i))
            #a='checked'
            #print i, a
            #if a=="checked":
            #   v='1'
            #else:
            #   v='0'
            print "switching LED"+str(i)+" to:"+v
            open('/sys/class/gpio/gpio'+str(i)+'/value','w').write(v)
        self.get()

application = tornado.web.Application([
    (r"/", Userform),
    (r"/upload", Upload),
    (r"/leds", MyFormHandler),
    (r'/download/(.*)',tornado.web.StaticFileHandler,{'path':"/tmp/"}),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
