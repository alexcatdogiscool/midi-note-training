from flask import Flask, render_template, jsonify, request
import mido
import time
import threading
import requests
import random
import cv2

app = Flask(__name__)

midi_in = mido.open_input()


note_to_key = {
    60: 'C',
    61: 'Cs',
    62: 'D',
    63: 'Ds',
    64: 'E',
    65: 'F',
    66: 'Fs',
    67: 'G',
    68: 'Gs',
    69: 'A',
    70: 'As',
    71: 'B',
}

current_key = None
current_color = None
current_goal = "C5.png"
current_mode = "treble"


def random_note(mode):
    if mode == "bass":
        l = [("E", 2), 
            ("F", 2), 
            ("G", 2), 
            ("A", 2), 
            ("B", 2), 
            ("C", 3), 
            ("D", 3), 
            ("E", 3), 
            ("F", 3), 
            ("G", 3), 
            ("A", 3), 
            ("B", 3), 
            ("C", 4), 
            ("D", 4), 
            ]
        note = l[random.randint(0,13)]
        return note[0] + str(note[1])
    elif mode == "treble":
        i = random.randint(0,13)
        letter = chr(((i%7)+65))
        octave = (i//7) + 4
        return letter + str(octave)

def listen_to_midi():
    while True:
        for msg in midi_in.iter_pending():
            if msg.type == 'note_on':
                note = msg.note
                note = (note%12)+60
                key = note_to_key[note]
                print("fart")
                requests.post("http://127.0.0.1:5000/change_color", json={"key": key, "velocity": msg.velocity})


midi_thread =threading.Thread(target=listen_to_midi)
#midi_thread.deamon = True
midi_thread.start()


@app.route('/')
def paino():
    return render_template("start.html")

@app.route("/treble")
def treble():
    global current_mode
    current_mode = "treble"
    return render_template("index.html")

@app.route("/bass")
def trebble():
    global current_mode
    current_mode = "bass"
    return render_template("index.html")



@app.route("/change_color", methods=['POST'])
def change_key_color():
    global current_key, current_color, current_goal, current_mode
    content = request.get_json()
    key = content.get("key")
    velocity = content.get("velocity")
    print(velocity)
    if velocity == 0:
        current_color = "white"
        return jsonify({"status": "success"}), 200
        
    color = "red"
    print(key, current_goal, current_goal[0])
    if key == current_goal[0]:
        color = "green"
        current_goal = random_note(current_mode) + ".png"
        if current_mode == "treble":
            img = cv2.imread(f"static/images/treble/{current_goal}")
        else:
            img = cv2.imread(f"static/images/bass/{current_goal}")
        cv2.imwrite("static/images/current.png", img)


    current_key = key
    current_color = color
    print(f"yay!!! yipeeee :D   {key}, {color}")
    return jsonify({"status": "success"}), 200


@app.route("/get_last_color", methods=['GET'])
def get_last_color():
    return jsonify({"key": current_key, "color": current_color, "goal": current_goal})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", use_reloader=False)