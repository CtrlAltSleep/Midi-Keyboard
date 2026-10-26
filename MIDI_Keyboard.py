import board
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Initialize USB MIDI out on channel 1 (index 0)
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Map the GPIO pins to the buttons based on your KiCad schematic
button_pins = [
    board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9
]

# Assign a MIDI note number to each button (60 is Middle C)
midi_notes = [60, 62, 64, 65, 67, 69, 71, 72]

# Setup the hardware pins as inputs with pull-up resistors
buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

# Track the previous state of each button to detect changes
previous_states = [True] * 8

while True:
    for i in range(8):
        # The value is False when the button is pressed (connected to Ground)
        current_state = buttons[i].value
        
        # Detect if a button was just pressed
        if previous_states[i] and not current_state:
            midi.send(NoteOn(midi_notes[i], 127)) # 127 is max velocity
            
        # Detect if a button was just released
        elif not previous_states[i] and current_state:
            midi.send(NoteOff(midi_notes[i], 0))
            
        # Update the state for the next loop
        previous_states[i] = current_state