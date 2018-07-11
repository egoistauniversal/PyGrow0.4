from flask import Flask, render_template
from flask_socketio import SocketIO
from database import Database
import modules
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
        socketio.sleep(200)
        ext = randint(-10, 30)
        fr = randint(10, 30)

        socketio.emit('my_response',
                      {'data': 'Values', 'ext': ext, 'fr': fr},
                      namespace='/carpi')


@socketio.on('connect', namespace='/carpi')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


# ----------------------countdown-------------------------------------

# this is only called once index.html has been loaded.
@socketio.on('get_module_countdown_time', namespace='/carpi')
def on_get_module_countdown_time(data):
    module = get_module_by_program_id(data)
    socketio.emit('update_countdown_label_timers_on_start',
                  {'program_id': data['program_id'], 'timeout': module.get_seconds()},
                  namespace='/carpi')


@socketio.on('pause_countdown_timer', namespace='/carpi')
def on_pause_countdown_timer(data):
    module = get_module_by_program_id(data)
    module.timer_stop()


@socketio.on('resume_countdown_timer', namespace='/carpi')
def on_resume_countdown_timer(data):
    module = get_module_by_program_id(data)
    module.timer_resume()
    socketio.emit('update_countdown_label_timers_on_start',
                  {'program_id': data['program_id'], 'timeout': module.get_seconds()},
                  namespace='/carpi')


@socketio.on('countdown_change_state_manual', namespace='/carpi')
def on_countdown_change_state_manual(data):
    module = get_module_by_program_id(data)
    module.change_state_manual()


@socketio.on('countdown_reset', namespace='/carpi')
def on_countdown_reset(data):
    module = get_module_by_program_id(data)
    socketio.emit('update_countdown_label_timers_on_start',
                  {'program_id': data['program_id'], 'timeout': module.get_seconds()},
                  namespace='/carpi')


def countdown_state_changed(program_id, timeout):
    socketio.emit('countdown_state_changed',
                  {'program_id': program_id, 'timeout': timeout},
                  namespace='/carpi')


def get_module_by_program_id(data):
    for x in range(0, myModuleList.__len__()):
        m = myModuleList[x]
        if m.get_program_id() == data['program_id']:
            return m


# -------------------------------------------------------------------------------

def _setup_clock_properties():
    print("Clock properties set")


def _setup_countdown_properties(program_id, module_id):
    rows = myDataBase.query_select_countdown_properties(program_id)
    if len(rows) == 1:
        row = rows[0]
        my_countdown = modules.Countdown(countdown_state_changed)
        my_countdown.set_properties(program_id, module_id, row[0], row[1], row[2], row[3], row[4], row[5])
        myModuleList.append(my_countdown)
    else:
        print("Warning: Possible program_id duplication!!!")


def _run_on_start():
    global myModuleList
    rows = myDataBase.query_select_modules()
    for row in rows:
        # if module_id
        if row[1] == 11:
            print("Setup clock properties")
        elif row[1] == 12:
            _setup_countdown_properties(row[0], row[1])
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
