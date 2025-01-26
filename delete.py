

import mido


midi_in = mido.open_input()

while True:
    for msg in midi_in.iter_pending():
        if msg.type == 'note_on':
            note = msg.note
            print("fart")