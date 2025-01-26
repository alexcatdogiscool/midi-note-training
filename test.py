import mido


print(mido.get_input_names())

with mido.open_input() as inport:
    for msg in inport:
        print(msg)