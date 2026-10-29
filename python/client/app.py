from flask import Flask, render_template, request
import os
import configparser
import dbus

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../../config/rgb_options.ini')

def read_config():
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def render_settings(config):
    jellyfin = config['jellyfin'] if config.has_section('jellyfin') else {}
    return render_template('index.html',
        brightness = int(config['DEFAULT']['brightness']),
        rows = int(config['DEFAULT']['rows']),
        columns = int(config['DEFAULT']['columns']),
        power = config['DEFAULT']['power'],
        refresh_rate = int(config['DEFAULT']['refresh_rate']),
        server_url = jellyfin.get('server_url', ''),
        api_key = jellyfin.get('api_key', ''),
        device = jellyfin.get('device', ''))

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

# home route
@app.route("/")
def saved_config():
    return render_settings(read_config())

# handling power status
@app.route("/power", methods=["GET", "POST"])
def handle_power():
    config = read_config()
    power = request.form['power']
    config.set('DEFAULT', 'power', power)
    with open(filename, 'w') as configfile:
        config.write(configfile)
    if power == 'on':
      job = manager.StartUnit('jellypi.service', 'replace')
    else:
      job = manager.StopUnit('jellypi.service', 'replace')
    return render_settings(config)

# handling form data
@app.route('/brightness', methods=['POST'])
def handle_brightness():
    config = read_config()
    config.set('DEFAULT', 'brightness', request.form['brightness'])
    with open(filename, 'w') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('jellypi.service', 'fail')
    return render_settings(config)

# handling form data
@app.route('/size', methods=['POST'])
def handle_size():
    config = read_config()
    config.set('DEFAULT', 'rows', request.form['rows'])
    config.set('DEFAULT', 'columns', request.form['columns'])
    with open(filename, 'w') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('jellypi.service', 'fail')
    return render_settings(config)

# handling form data
@app.route('/refresh-rate', methods=['POST'])
def handle_refresh_rate():
    config = read_config()
    config.set('DEFAULT', 'refresh_rate', request.form['refresh_rate'])
    with open(filename, 'w') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('jellypi.service', 'fail')
    return render_settings(config)

# handling jellyfin settings
@app.route('/jellyfin', methods=['POST'])
def handle_jellyfin():
    config = read_config()
    if not config.has_section('jellyfin'):
        config.add_section('jellyfin')
    config.set('jellyfin', 'server_url', request.form['server_url'])
    config.set('jellyfin', 'api_key', request.form['api_key'])
    config.set('jellyfin', 'device', request.form['device'])
    with open(filename, 'w') as configfile:
        config.write(configfile)
    return render_settings(config)

app.run(host='0.0.0.0', port=80)
