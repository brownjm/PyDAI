from src.pydaiweb.bin.basepage import BasePage

class cmd(BasePage):
    def process(self):
        cmd = self.request['post']['cmd'].value
        self.request['server'].webOutQueue.put(cmd)
