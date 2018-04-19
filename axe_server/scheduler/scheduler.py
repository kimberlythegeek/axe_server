import datetime
import sched
import time


class PeriodicScheduler(object):
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action):
        action()
        self.scheduler.enter(interval, 1, self.setup,
                             (interval, action))

    def run(self):
        self.scheduler.run()
