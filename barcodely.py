from sys import argv
from os import system
from time import sleep

from pyautogui import typewrite 
import PySimpleGUI as sg


def send_barcode_event(barcode: str) -> None:
    typewrite(barcode)

def get_window_focus() -> None:
    system('xdotool search --name "New - Odoo" | xargs xdotool windowactivate')

def return_window_focus() -> None:
    system('xdotool search --name "Barcode Emulator" | xargs xdotool windowactivate')


barcode_list_col = [
    [
        sg.Text("Barcode"),
        sg.In(size=(25, 1), enable_events=True, key="-BARCODE-"),
    ],
    [
        sg.Button("Send"),
        sg.Button("Add"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-BARCODE LIST-"
        )
    ],
]

layout = [
    [
        sg.Column(barcode_list_col),
    ]
]

window = sg.Window("Barcode Emulator", layout)
barcode_list = []

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Send barcode event to window
    if event == "Send":
        if len(values["-BARCODE LIST-"]) > 0:
            get_window_focus()
            send_barcode_event(values["-BARCODE LIST-"][0])
            return_window_focus()

    # Add barcode to favorites
    if event == "Add":
        barcode_list.append(values.get('-BARCODE-'))
        window["-BARCODE LIST-"].update(barcode_list)

window.close()
