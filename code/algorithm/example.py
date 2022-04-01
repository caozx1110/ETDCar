import threading
import time

lock = threading.Lock()


class MyThread(threading.Thread):
    target = None
    args = ()
    result = None

    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


class exp:
    a: int
    data = None
    is_change: bool

    def __init__(self):
        self.a = 0
        self.is_change = True

    def b(self):
        while True:
            if self.data is not None:
                self.a += self.data
                self.data = None
                self.is_change = True
                print('result {}'.format(self.a))
            time.sleep(1)

    def get_data(self):
        while True:
            if self.is_change:
                print('data input: ', end='')
                self.is_change = False
            self.data = int(input(''))
            time.sleep(1)


if __name__ == "__main__":
    x = exp()
    t = [MyThread(target=x.b), MyThread(target=x.get_data)]
    for thr in t:
        thr.start()

    for thr in t:
        thr.join()
