import PySimpleGUI as sg

counter = 0
transparencyOptions = [0.75, 0.5, 1]

def writeToFile(myString):
    f = open("myfile.txt", "w")
    f = open("myfile.txt", "a")
    f.write(myString)
    f.close()
    
sg.theme('Reddit')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Fade'), sg.Button('Read File')],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Text('Debug', key='Debug')]]

# Create the Window
window = sg.Window('Window Title', layout, keep_on_top = True, finalize = True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == 'Ok':
        print('You entered ', values[0])
        writeToFile(values[0])
    elif event == 'Fade':
        window.set_alpha(transparencyOptions[counter%3])
        counter += 1
    elif event == 'Read File':
        f = open("myFile.txt", "r")
        text = f.readline()
        window['Debug'].update(text)

window.close()
