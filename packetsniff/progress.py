
class ProgressDisplay:
    
    def __init__(self, msgpre, msgpost):
        self.count = 0 # number processed
        self.msgpre = msgpre
        self.msgpost = msgpost
        print(msgpre + '0' + msgpost, end='')


    def next(self):
        self.erase(len(str(self.count)) + len(self.msgpost))
        self.count += 1
        print(str(self.count) + self.msgpost, end='')

    def clear(self):
        self.erase(len(self.msgpre) + len(str(self.count)) + len(self.msgpost))

    def newline(self):
        print('\n',end='')

    def erase(self, n):
        for x in range(0, n):
            print("\b", end='')