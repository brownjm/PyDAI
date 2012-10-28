from src.pydaiweb.bin.basepage import BasePage
import json

class screenupdate(BasePage):
    def render(self):
        return dict(text=self.formatOutput())
        
    def formatOutput(self):
        if not self.request['server'].webInQueue.empty():
            return json.dumps(self.request['server'].webInQueue.get())
        else:
            return json.dumps({})
