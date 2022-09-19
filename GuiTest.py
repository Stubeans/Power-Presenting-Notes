from fileinput import filename
from turtle import position
import PySimpleGUI as sg

def writeToFile(fileName, myString):
    #f = open(fileName, "w")
    f = open(fileName, "a")
    f.write(myString)
    f.close()

def readFromFile(fileName):
    f = open(fileName, "r")
    text = f.readline()
    return text

def inputWindow():
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    
    sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('Title:'), sg.InputText(size=(30)), sg.Text('Note 1', key='NoteCount'), sg.Button('Add Note')],
            [sg.Button('<-'), sg.Multiline(key="TextInput", size=(50,20), expand_x=True, expand_y=True), sg.Button('->')],
            [sg.Button('Fade'), sg.Button('Debug Button')],
            [sg.Button('Save'), sg.Push(), sg.Button('Read Note'), sg.Button('Close')],
            [sg.Text('Debug', key='Debug')],
            [sg.Sizegrip()]  ]

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = False, finalize = True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Save': # saves the value in the text input into a file
            print('You entered Title: ' + values[0] + ' and contents: ' + values['TextInput'])
            writeToFile("myfile.txt", values[0] + "!$")
            writeToFile("myfile.txt", values['TextInput'] + "!$END!$")
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == 'Debug Button': # Reads the value from the first line of the file and displays it in the Debug text NOT FUNCTIONAL
            window['Debug'].update(readFromFile("myfile.txt"))
        elif event == 'Read Note':
            window.close()
            return "Read Note"

    window.close()

def outputWindow():
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    
    sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('NOTES:')],
                [sg.Button('<-'), sg.Output(size=(50, 20)), sg.Button('->')],
                [sg.Button('Return'), sg.Button('Fade'), sg.Push(), sg.Button('Close')],
                [sg.Sizegrip()]]

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = True, finalize = True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Return': # Returns to the inputWindow
            window.close()
            return "Return"
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1

    window.close()

def main():
    print("main")
    if(inputWindow() == "Read Note"):
        if(outputWindow() == "Return"):
            main()

main()
