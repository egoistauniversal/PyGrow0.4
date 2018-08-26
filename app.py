from flask import Flask, render_template
from flask_socketio import SocketIO
from database import Database
from modules import countdown
from modules import clock
import json
from random import randint


async_mode = None
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

# https://stackoverflow.com/questions/43801884/how-to-run-python-socketio-in-thread
# switching to threading mode in Flask + python-socketio as documented here:
# http://python-socketio.readthedocs.io/en/latest/#standard-threading-library
socketio = SocketIO(app, async_mode='threading')
thread = None

myDataBase = Database()
myModuleList = []


@app.route('/')
def index():
    json_list = []
    for x in range(0, myModuleList.__len__()):
        module = myModuleList[x]
        json_list.append(module.get_property_list())

    return render_template('index.html', modules_property_list=json.dumps(json_list))


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(5)
        ext = randint(-10, 30)
        fr = randint(10, 30)

        socketio.emit('my_response',
                      {'data': 'Values', 'ext': ext, 'fr': fr})


@socketio.on('connect')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)

# ----------------------Clock-------------------------------------


# this is only called once index.html has been loaded.
@socketio.on('clock_get_timer_on_load')
def on_clock_get_timer_on_load(data):
    module = get_module_by_program_id(data)
    # print("Time left: {}".format(module.get_time_left()))
    # socket_emit_clock_timer(data, module.get_time_left())
    socketio.emit('update_clock_label_timers_on_start',
                  {'program_id': data['program_id'], 'switch_on': module.get_seconds_to_switch_on(),
                   'switch_off': module.get_seconds_to_switch_off(), 'timeout': module.get_time_left()})


@socketio.on('clock_pause_timer')
def on_clock_pause_timer(data):
    module = get_module_by_program_id(data)
    module.timer_stop()


@socketio.on('clock_resume_timer')
def on_clock_resume_timer(data):
    module = get_module_by_program_id(data)
    # socket_emit_clock_timer(data, module.get_time_left())
    socketio.emit('update_clock_label_timers_on_start',
                  {'program_id': data['program_id'], 'switch_on': module.get_seconds_to_switch_on(),
                   'switch_off': module.get_seconds_to_switch_off(), 'timeout': module.get_time_left()})
    module.timer_resume()


# REMOVE
def socket_emit_clock_timer(d, s):
    socketio.emit('update_clock_label_timers_on_start',
                  {'program_id': d['program_id'], 'timeout': s})


def clock_state_changed(program_id, timeout):
    socketio.emit('clock_state_changed',
                  {'program_id': program_id, 'timeout': timeout})

# ----------------------Countdown-------------------------------------


# this is only called once index.html has been loaded.
@socketio.on('countdown_get_timer_on_load')
def on_countdown_get_timer_on_load(data):
    module = get_module_by_program_id(data)
    # if automatic == 1
    if module.get_automatic():
        seconds = module.get_seconds_on_automatic()
    else:
        seconds = module.get_seconds_on_manual()
    socket_emit_countdown_timer(data, seconds)


@socketio.on('countdown_pause_timer')
def on_countdown_pause_timer(data):
    module = get_module_by_program_id(data)
    module.timer_stop()


@socketio.on('countdown_resume_timer')
def on_countdown_resume_timer(data):
    module = get_module_by_program_id(data)
    socket_emit_countdown_timer(data, module.get_seconds_on_manual())
    module.timer_resume()


@socketio.on('countdown_reset_timer')
def on_countdown_reset_timer(data):
    module = get_module_by_program_id(data)
    module.timer_reset()
    socket_emit_countdown_timer(data, module.get_seconds_on_manual())


@socketio.on('countdown_change_state_manual')
def on_countdown_change_state_manual(data):
    module = get_module_by_program_id(data)
    module.invert_state()


def countdown_state_changed(program_id, timeout):
    socketio.emit('countdown_state_changed',
                  {'program_id': program_id, 'timeout': timeout})


def socket_emit_countdown_timer(d, s):
    socketio.emit('update_countdown_label_timers_on_start',
                  {'program_id': d['program_id'], 'timeout': s})


def get_module_by_program_id(data):
    for x in range(0, myModuleList.__len__()):
        m = myModuleList[x]
        if m.get_program_id() == data['program_id']:
            return m


# -------------------------------------------------------------------------------

def _run_on_start():
    global myModuleList
    rows = myDataBase.query_select_all_modules()
    for row in rows:
        # if module_id
        if row[1] == 11:
            m = clock.Clock(row, clock_state_changed)
            myModuleList.append(m)
        elif row[1] == 12:
            m = countdown.Countdown(row, countdown_state_changed)
            myModuleList.append(m)
        elif row[1] == 13:
            print("Setup temperature properties")

    # Example on how to get access to data from lists
    # print(myListModules[0].program_id)

    # loop from 0 to length list
    for x in range(0, myModuleList.__len__()):
        module = myModuleList[x]
        # start all modules
        module.start()

    socketio.run(app, debug=True, use_reloader=False)


if __name__ == '__main__':
    # Call function after a flask app is run
    _run_on_start()
