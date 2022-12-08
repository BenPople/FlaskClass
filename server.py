from flask import Flask, request, redirect, jsonify, url_for
import random as rand
from sense_hat import SenseHat

Sense = SenseHat()

app = Flask(__name__)

@app.route('/success/<action>')
def success(action):
   return (f'{action} complete!')

@app.route('/api/v1/Temperature')
def sendTemperature():
    TemperatureJSON = jsonify(
            {
                "Temperature" : rand.randint(1,10)
            }
        )
    
    TemperatureJSON.headers.add('Access-Control-Allow-Origin', '*')

    return TemperatureJSON

@app.route('/api/v1/SensorData/all')
def sendSensorData():
    SensorDataJSON = jsonify(
            {
                "Temperature" : Sense.get_temperature(),
                "Pressure" : Sense.get_pressure(),
                "Humidity" : Sense.get_humidity()
            }
        )
    
    SensorDataJSON.headers.add('Access-Control-Allow-Origin', '*')

    return SensorDataJSON

@app.route('/api/v1/requests/temperatureLimit', methods=['GET'])
def requestTemperatureExceeded():
    if 'maxTemp' in request.args:
        maxTemperature = int(request.args.get('maxTemp'))
    else:
        return jsonify({"Error" : "Max Temperature Not Provided"})

    currentTemperature = Sense.get_temperature()
    exceeded = False

    if  currentTemperature >= maxTemperature:
        exceeded = True

    maxTemperatureResponseJSON = jsonify(
        {
            "TempLimitExceeded" : exceeded,
            "CurrentTemperatre" : currentTemperature,
            "ProvidedMaxTemperature" : maxTemperature
        }
    )

    maxTemperatureResponseJSON.headers.add('Access-Control-Allow-Origin', '*')

    return maxTemperatureResponseJSON

@app.route('/api/v1/LED/SetLight', methods=['GET'])
def setLight():
    color = request.args.get('lightColour')
    #color = "'255','255','0'" -> color = [255,255,0]
    trueColor = []

    for value in color:
        trueColor.append(int(value))

    Sense.clear(trueColor)
    return jsonify(
        {
            "SetLightSuccess" : True,
            "SetColor" : trueColor
            }
        )

@app.route('/sensors')
def sensors():
    temperature = Sense.get_temperature()
    humidity = Sense.get_humidity()
    pressure = Sense.get_pressure()

    response = jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run(debug=True)