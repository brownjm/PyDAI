from os import curdir, sep
from string import Template

class BasePage():
    def __init__(self, Request):
        self.request = Request
        
    def run(self):
        try:
            #Process the request
            self.process()
        
            #Render and return the response
            f = open(curdir + sep + self.request['path'])
            page = Template(f.read())
            f.close()
            return page.substitute(self.render())
        except:
            raise
            
    def process(self):
        pass
        
    def render(self):
        pass
