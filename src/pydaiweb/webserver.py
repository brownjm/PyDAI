#Copyright Jon Berg , turtlemeat.com

import string,cgi,time,os,sys
import src.pydaiweb.www
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from multiprocessing import Queue
import traceback
#import pri

class PyDAIRequestHandler(BaseHTTPRequestHandler):
    def handlePath(self, selfpath):
        parsedPath = urlparse(selfpath)
        path = parsedPath.path
        query = parse_qs(parsedPath.query)
        
        if path == '/':
            path = '/index.pdsp'
            
        if not path.startswith("/src/pydaiweb/www"): 
            path = ''.join([curdir, sep, "src/pydaiweb/www", path])
            
        query['path'] = path
        
        return query


    def do_GET(self):
        request = self.handlePath(self.path)
        path  = request['path']
        try:                
            if path.endswith(".html") or path.endswith('.js') or path.endswith('.css'):
                f = open(curdir + sep + path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if path.endswith(".pdsp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                
                pyFile = os.path.basename(path).split('.')[0]
                                
                m = __import__("src.pydaiweb.www.%s" % pyFile)
                c = getattr(m.pydaiweb.www, pyFile)
                p = getattr(c, pyFile)(request)
                self.wfile.write(p.run())
                return
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % path)
     

    def do_POST(self):
        global rootnode
        
        request = self.handlePath(self.path)
        path = request['path']
        request['server'] = self.server
        try:
            if path.endswith('.pdsp'):
                form = cgi.FieldStorage(
           			fp=self.rfile, 
				    headers=self.headers,
				    environ={'REQUEST_METHOD':'POST'}
                )

                request['post'] = form
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                
                pyFile = os.path.basename(path).split('.')[0]
                                
                m = __import__("src.pydaiweb.www.%s" % pyFile)
                c = getattr(m.pydaiweb.www, pyFile)
                p = getattr(c, pyFile)(request)
                self.wfile.write(p.run())
                return
            
        except:
            print traceback.print_exc()

class PyDAIHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.webInQueue = None
        self.webOutQueue = None

def WebServerMain(address, wInQueue, wOutQueue):
    try:
        server = PyDAIHTTPServer(address, PyDAIRequestHandler)
        
        server.webInQueue = wInQueue
        server.webOutQueue = wOutQueue
        
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    WebServerMain(('localhost', 80), Queue(), Queue())

