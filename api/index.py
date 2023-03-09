from flask import Flask,render_template,request, redirect, url_for, jsonify
from flask_mqtt import Mqtt
from configparser import ConfigParser

config = ConfigParser()



app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 3600
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/information')
def about():
    return render_template('information.html')

@app.route('/member')
def member():
    return render_template('member.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/sentdata', methods=['GET', 'POST'])
def signupForm():
    use = request.form['in_text']
    return render_template('signup.html', use = use)

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    use = request.form['in_text']
    use = int(use)
    if(use >=0 and use <= 450):
        mqtt.publish('hello_poommipat/command', use)
        return render_template('success.html')
    else:
        return render_template('error.html')

@app.route('/data')
def get_data():
    config.read("Config.ini")
    dat = config.get("setting", "val1")
    data = [dat,dat,dat,dat]
    return jsonify(data)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('hello_poommipat/#')

@mqtt.on_message()
def handle_message(client, userdata, message):
    a = (message.payload.decode())
    config["setting"] = {
        "val1" : int(a),
        "val2" : ""
    }
    with open("Config.ini", "w") as f:
        config.write(f)

if __name__=="__main__":
    app.run(debug=True)
