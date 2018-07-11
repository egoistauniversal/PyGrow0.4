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


# ------------------------------------------------------


class Clock:
    def __init__(self, program_id, module_id, pin, time_on, time_off):
        self.program_id = program_id
        self.module_id = module_id
        self.pin = pin
        self.time_on = int(time_on)
        self.time_off = int(time_off)
        self.state = 0
        self.active = 1

# -------------------------------------------------


class Countdown:
    def __init__(self, my_function):
        self._program_id = 0
        self._module_id = 0
        self._name = ''
        self._pin = 0
        self._time_on = 0
        self._time_off = 0
        self._state = 0
        self._automatic = 0
        self._pause_time = None
        self._timer = None
        self._callback_function = my_function

    def set_properties(self, program_id, module_id, name, pin, time_on, time_off, state, automatic):
        self._program_id = program_id
        self._module_id = module_id
        self._name = name
        self._pin = pin
        self._time_on = int(time_on)
        self._time_off = int(time_off)
        self._state = state
        self._automatic = automatic

    def start(self):
        if self._automatic:
            if self._state:
                timeout = self._time_on
            else:
                timeout = self._time_off
            self._timer = TimerClass(self.change_state_automatic, timeout)
            self._timer.start()
            # print("{} - OFF - {}".format(self._program_id, timeout))

    def change_state_automatic(self):
        self._pause_time = None
        if self._state:
            self._state = 0
            timeout = self._time_off
        else:
            self._state = 1
            timeout = self._time_on
        self._timer = TimerClass(self.change_state_automatic, timeout)
        self._timer.start()
        self._callback_function(self._program_id, timeout)
        # print('program id: {} change state to: {}'.format(self._program_id, self._state))

    def change_state_manual(self):
        if self._state:
            self._state = 0
        else:
            self._state = 1

    def timer_stop(self):
        self._automatic = 0
        self._timer.stop()
        self._pause_time = self.get_seconds()
        self._timer = None

    def timer_resume(self):
        self._automatic = 1
        # check if app starts with automatic set to 0
        if self._pause_time:
            s = self._pause_time
        else:
            s = self.get_seconds()

        self._timer = TimerClass(self.change_state_automatic, s)
        self._timer.start()

    # -----------------------------Set-------------------------------

    def set_state(self, value):
        self._state = value

    # -----------------------------Get-------------------------------

    def get_property_list(self):
        return [self._program_id, self._module_id, self._name, self._state, self._automatic]

    def get_program_id(self):
        return self._program_id

    def get_automatic(self):
        return self._automatic

    def get_timeout(self):
        if self._state:
            return self._time_on
        else:
            return self._time_off

    def get_seconds(self):
        # if self._pause_time as not been set
        if self._pause_time is None:
            if self._state:
                # if self._state == 1 return self._time_on
                s = self._time_on
            else:
                # if self._state == 0 return self._time_off
                s = self._time_off
            # if self._timer has not been set
            if self._timer is None:
                return int(s)
            else:
                return int(s - self._timer.get_seconds())
        else:
            if self._timer is None:
                return int(self._pause_time)
            else:
                return int(self._pause_time - self._timer.get_seconds())


# -----------------------------------------------------------------


class Sensor:
    def __init__(self, program_id, module_id, pin, trigger_time):
        self.program_id = program_id
        self.module_id = module_id
        self.pin = pin
        self.trigger_time = trigger_time

