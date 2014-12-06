class Progress():
    def __init__(self, end_value, title="No title"):
        self._end_value = end_value
        self._title = title
        self._increment_size = max(int(end_value / 100), 1)
        self._done = False

    def percent(self, current):
        if self._done:
            return
        if current >= self._end_value:
            #print('{0}... Done!'.format(self._title))
            self._done = True
        elif current % self._increment_size == 0:
            print('{0}: {1:.0%}'.format(self._title, 1.0 / self._end_value * current), end='\r')

    def bar(self, current):
        pass


if __name__ == "__main__":
    end = 53204
    test = Progress(end, "test1")
    import time

    for i in range(int(end)):
        test.percent(i + 1)
        time.sleep(0.0002)

    end = 2344
    test = Progress(end, "test2")
    for i in range(int(end)):
        test.percent(i + 1)
        time.sleep(0.002)