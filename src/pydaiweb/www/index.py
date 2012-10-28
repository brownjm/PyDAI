from src.pydaiweb.bin.basepage import BasePage

class index(BasePage):
    def render(self):
        return dict(name='Kyle')
