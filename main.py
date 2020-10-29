from flask import Flask, render_template, request, make_response, jsonify
from repeat import RepeatedTimer
from random import randint
from threading import Thread
#import Start2

def main():
    try:
        app = Flask(__name__)

        def formatValue(value):
            max = 15
            return round((((value - 50) / 50) * max), 1)

        def moverobot(angles):
            if not angles:
                degrees = [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
            else:
                degrees = [int(angles[0]), int(angles[1]), int(angles[2]), int(angles[3])]
            print(f'move to {degrees}')
            #Thread(target = Start2.move, args=(0, formatValue(degrees[0])))
            #Thread(target = Start2.move, args=(1, formatValue(degrees[1])))
            #Thread(target = Start2.move, args=(2, formatValue(degrees[2])))
            #Thread(target = Start2.move, args=(3, formatValue(degrees[3])))
            #for i, value in enumerate(degrees):
                #Start2.move(i, formatValue(value))

        @app.route("/", methods=["GET"])
        def home():
            return render_template("index.html")

        @app.route('/send', methods=['POST'])
        def receive():
            data = request.get_json()
            moverobot(data['positions'])
            return make_response(jsonify({"message": "ok"}), 200)

        @app.route('/auto', methods=["POST"])
        def auto():
            data = request.get_json()
            if data['Auto']:
                print("Send automatic updates!")
                timer.start()
            else:
                timer.stop()
                print("Stop sending automatic updates!")
            return make_response(jsonify({"message": "ok"}), 200)

        timer = RepeatedTimer(4, moverobot, False)
        app.run(host='0.0.0.0', port=5005, debug=True)

    finally:
        try:
            timer.stop()
        except AttributeError:
            print("The timer have never been activated.")
        #Start2.end()
        print('Program closed.')

if __name__ == "__main__":
    main()