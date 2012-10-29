from src.pydaiweb.bin.basepage import BasePage
import json

class screenupdate(BasePage):
    def process(self):
        if self.request['type'] == 'POST' and \
        self.request['post'].has_key('window'):
            scr = ''.join(['window=', \
            self.request['post']['window'].value])
            self.request['server'].webOutQueue.put(scr)

    def render(self):
        return dict(text=self.formatOutput())
        
    def formatOutput(self):
        if not self.request['server'].webInQueue.empty():
            return self.request['server'].webInQueue.get()
        else:
            return json.dumps(dict())
