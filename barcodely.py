from os import system, makedirs, path
import csv

from pyautogui import typewrite 
import PySimpleGUI as sg


BARCODE_CSV = "/home/jbos/.barcodely/barcodes.csv"


def send_barcode_event(barcode: str) -> None:
    typewrite(barcode)

def get_window_focus() -> None:
    system('xdotool search --name "New - Odoo" | xargs xdotool windowactivate')

def return_window_focus() -> None:
    system('xdotool search --name "Barcode Emulator" | xargs xdotool windowactivate')

def update_barcode_csv(barcode_list: list) -> None:
    try:
        print(barcode_list)
        with open(BARCODE_CSV, 'w', encoding='UTF-8') as file:
            writer = csv.writer(file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for barcode in barcode_list:
                writer.writerow([barcode])
    except:
        makedirs(path.dirname(BARCODE_CSV), exist_ok=True)
        update_barcode_csv(barcode_list)

def load_barcode_list() -> list:
    with open(BARCODE_CSV, encoding='UTF-8') as file:
        csv_reader = csv.reader(file)

        return [x[0] for x in list(csv_reader)] or []

barcode_list = load_barcode_list()

ttk_style = 'alt'
sg.theme('SystemDefaultForReal')

barcode_list_col = [
    [
        sg.Text("Barcode"),
        sg.In(size=(25, 1), enable_events=True, key="-BARCODE-"),
        sg.Button("Add"),
    ],
    [
        sg.Listbox(
            values=barcode_list, size=(40, 20), key="-BARCODE LIST-"
        )
    ],
    [
        sg.Button("Send", expand_x=True),
        sg.Button("Delete"),

    ],
]


layout = [
    [
        sg.Column(barcode_list_col),
    ]
]

window = sg.Window("Barcode Emulator", layout, ttk_theme=ttk_style)

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
        window['-BARCODE-'].Update('')
        window["-BARCODE LIST-"].update(barcode_list)

        update_barcode_csv(barcode_list)

    if event == "Delete":
        if barcode_list:
            selected = values["-BARCODE LIST-"][0] 
            barcode_list.pop(barcode_list.index(selected))
            window["-BARCODE LIST-"].update(barcode_list)

            update_barcode_csv(barcode_list)

window.close()
