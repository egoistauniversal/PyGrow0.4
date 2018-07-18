import sched
import threading
import time
import datetime


class ClockTimerClass(threading.Thread):
    def __init__(self, my_function, timeout):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.timeout = timeout
        self.my_function = my_function

    def run(self):
        while not self.event.wait(self.timeout):
            self.stop()
            self.my_function()

    def stop(self):
        self.event.set()


class Clock:
    def __init__(self, row, my_function):
        self._program_id = int(row[0])
        self._module_id = int(row[1])
        self._name = row[2]
        self._pin = int(row[3])
        self._datetime_to_switch_on = self.seconds_to_datetime(int(row[4]))
        self._seconds_to_switch_off = int(row[5])
        self._state = row[6]
        self._automatic = int(row[7])
        self._schedule = sched.scheduler(time.time, time.sleep)
        self._timer = None
        self._callback_function = my_function

    @staticmethod
    def seconds_to_datetime(secs):
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        my_date = datetime.time(h, m, s)
        return datetime.datetime.combine(datetime.datetime.now(), my_date)

    def start(self):
        # time to switch on + duration of time on
        datetime_duration = self._datetime_to_switch_on + datetime.timedelta(seconds=self._seconds_to_switch_off)
        if self._datetime_to_switch_on >= datetime.datetime.now() < datetime_duration:
            self._state = 1
            difference = (datetime.datetime.now() - datetime_duration).total_seconds()
            self._timer = ClockTimerClass(self.switch_off, difference)
        else:
            self._state = 0
            if datetime.datetime.now() > self._datetime_to_switch_on:
                self._datetime_to_switch_on = self._datetime_to_switch_on + datetime.timedelta(days=1)
            self._schedule.enter(1, 1, self.check_datetime_to_switch_on)
            self._schedule.run(blocking=False)
            print("hey")

    def check_datetime_to_switch_on(self):
        if self._datetime_to_switch_on >= datetime.datetime.now():
            self.switch_on()
            print("Bingo")
        else:
            self._schedule.enter(1, 1, self.check_datetime_to_switch_on)
            self._schedule.run(blocking=False)
            print("Checking current time: {} against {}".format(datetime.datetime.now(), self._datetime_to_switch_on))

    def switch_on(self):
        self.invert_state()
        self._timer = ClockTimerClass(self.switch_off, self._seconds_to_switch_off)

    def switch_off(self):
        self.invert_state()
        self._schedule.enter(1, 1, self.check_datetime_to_switch_on)
        self._schedule.run(blocking=False)

    def invert_state(self):
        if self._state:
            self._state = 0
            print("Foco is OFF")
        else:
            self._state = 1
            print("Foco is ON")

    def get_property_list(self):
        return [self._program_id, self._module_id, self._name, self._state, self._automatic]
