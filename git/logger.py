class Logger:
    def __init__(self, display: bool = True):
        self.display = display
    
    def print(self, *args):
        if self.display:
            print(*args)