#!/usr/bin/python
import time

from evdev import InputDevice, list_devices, ecodes, categorize, events

print("Press Ctrl-C to quit")

devices = [InputDevice(fn) for fn in list_devices()]
assert len(devices) == 1
dev = devices[0]

# print dev.capabilities(verbose=True)

state = {}

for event in dev.read_loop():
    print(categorize(event)), type(event), event, event.code

    if event.type == 0:
        state = {}
    elif event.type == 3:
        state[event.code] = event.value
