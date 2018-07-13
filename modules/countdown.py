import threading
import datetime


class TimerClass(threading.Thread):
    def __init__(self, my_function, timeout):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.timeout = timeout
        self.time_start = None
        self.my_function = my_function

    def run(self):
        self.time_start = datetime.datetime.now()
        while not self.event.wait(self.timeout):
            self.stop()
            self.my_function()

    def stop(self):
        self.event.set()

    def get_seconds(self):
        # datetime.datetime.now() - self.time_start created a timedelta object
        t = datetime.datetime.now() - self.time_start
        # get total seconds from timedelta object "t"
        return t.total_seconds()


class Countdown:
    def __init__(self, row, my_function):
        self._program_id = int(row[0])
        self._module_id = int(row[1])
        self._name = row[2]
        self._pin = int(row[3])
        self._time_on = int(row[4])
        self._time_off = int(row[5])
        self._state = row[6]
        self._automatic = int(row[7])
        self._pause_time = None
        self._timer = None
        self._callback_function = my_function

    def start(self):
        if self._automatic:
            self._timer = TimerClass(self.change_state_automatic, self.get_state_timeout())
            self._timer.start()
            # print("{} - OFF - {}".format(self._program_id, timeout))

    def change_state_automatic(self):
        # self._pause_time has to be always none in this method
        self._pause_time = None

        self.invert_state()
        self._timer = TimerClass(self.change_state_automatic, self.get_state_timeout())
        self._timer.start()
        self._callback_function(self._program_id, self.get_state_timeout())
        # print('program id: {} change state to: {}'.format(self._program_id, self._state))

    def invert_state(self):
        if self._state:
            self._state = 0
        else:
            self._state = 1

    def timer_stop(self):
        self._automatic = 0
        self._timer.stop()

        # if self._pause_exist
        if self._pause_time:
            self._pause_time = self._pause_time - self._timer.get_seconds()
        else:
            self._pause_time = self.get_seconds_on_automatic()
            # print("program id: {} - STOP-Pause time: {}".format(self._program_id, self._pause_time))
            self._timer = None

    def timer_resume(self):
        self._automatic = 1
        self._timer = TimerClass(self.change_state_automatic, self.get_seconds_on_manual())
        self._timer.start()
        # print("program id: {} - RESUME-Pause time: {}".format(self._program_id, self._pause_time))

    def timer_reset(self):
        self._pause_time = self.get_state_timeout()

    # -----------------------------Get-------------------------------

    def get_property_list(self):
        return [self._program_id, self._module_id, self._name, self._state, self._automatic]

    def get_program_id(self):
        return self._program_id

    def get_automatic(self):
        return self._automatic

    def get_state_timeout(self):
        if self._state:
            return self._time_on
        else:
            return self._time_off

    def get_seconds(self):
        pass

    def get_seconds_on_automatic(self):
        # if self._pause_time: only used when loading page
        if self._pause_time:
            return self._pause_time - self._timer.get_seconds()
        else:
            return int(self.get_state_timeout() - self._timer.get_seconds())

    def get_seconds_on_manual(self):
        # if self._pause_time has some value
        if self._pause_time:
            return self._pause_time
        else:
            return self.get_state_timeout()