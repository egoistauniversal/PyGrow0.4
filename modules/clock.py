import threading
import time
import datetime


class ClockTimerDateTime(threading.Thread):
    def __init__(self, my_function, timeout):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.timeout = timeout
        self.my_function = my_function

    def run(self):
        while datetime.datetime.now() < self.timeout:
            time.sleep(1)
            # print("{} < {}".format(datetime.datetime.now(), self.timeout))
        self.stop()
        self.my_function()

    def stop(self):
        self.event.set()


class ClockTimer(threading.Thread):
    def __init__(self, my_function, timeout):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.timeout = timeout
        self.my_function = my_function

    def run(self):
        # print("Switch off in: {}".format(self.timeout))
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
        self._timer = None
        self._callback_function = my_function

    @staticmethod
    def seconds_to_datetime(secs):
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        my_date = datetime.time(h, m, s)
        return datetime.datetime.combine(datetime.datetime.now(), my_date)

    def start(self):
        if self._automatic:
            if datetime.datetime.now() < self._datetime_to_switch_on:
                self._state = 0
                self._timer = ClockTimerDateTime(self.switch_on_automatic, self._datetime_to_switch_on)
                self._timer.start()
            else:
                datetime_duration = self._datetime_to_switch_on + datetime.timedelta(seconds=self._seconds_to_switch_off)
                if datetime.datetime.now() < datetime_duration:
                    self._state = 1
                    difference = abs((datetime.datetime.now() - datetime_duration).total_seconds())
                    self._timer = ClockTimer(self.switch_off_automatic, difference)
                    self._timer.start()
                    # print("On till {} seconds".format(datetime_duration))
                else:
                    d = (datetime.datetime.now() - self._datetime_to_switch_on).days
                    self._datetime_to_switch_on = self._datetime_to_switch_on + datetime.timedelta(days=d)
                    self._timer = ClockTimerDateTime(self.switch_on_automatic, self._datetime_to_switch_on)
                    self._timer.start()

    def switch_on_automatic(self):
        self._timer = None
        self.invert_state()
        self._timer = ClockTimer(self.switch_off_automatic, self._seconds_to_switch_off)
        self._timer.start()

    def switch_off_automatic(self):
        self._timer = None
        self.invert_state()
        self._datetime_to_switch_on = self._datetime_to_switch_on + datetime.timedelta(days=1)
        self._timer = ClockTimerDateTime(self.switch_on_automatic, self._datetime_to_switch_on)
        self._timer.start()

    def timer_stop(self):
        self._automatic = 0
        self._timer.stop()

    def timer_resume(self):
        self._automatic = 1
        self.start()

    def invert_state(self):
        if self._state:
            self._state = 0
            print("Foco is OFF")
        else:
            self._state = 1
            print("Foco is ON")

    def get_property_list(self):
        return [self._program_id, self._module_id, self._name, self._state, self._automatic]

    def get_program_id(self):
        return self._program_id

    def get_time_left(self):
        if self._state:
            datetime_duration = self._datetime_to_switch_on + datetime.timedelta(seconds=self._seconds_to_switch_off)
            s = abs((datetime.datetime.now() - datetime_duration).total_seconds())
        else:
            s = abs((self._datetime_to_switch_on - datetime.datetime.now()).total_seconds())
        return s
