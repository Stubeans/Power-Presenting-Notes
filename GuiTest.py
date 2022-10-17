from distutils.log import debug
from tokenize import String
from turtle import color, position
import PySimpleGUI as sg

def writeToFile(fileName, title, body):
    #f = open(fileName, "w")
    f = open(fileName, "a")
    f.write("$S$\n"+ title + "\n")
    f.write(body + "\n")
    f.close()

def readFromFile(fileName):
    f = open(fileName, "r")
    text = f.readlines()
    returnText = []
    for x in range(len(text)):
        if text[x].strip() == "$S$":
            returnText.append(recursiveText(text, x+1))
    f.close()
    return returnText

def recursiveText(text, begin):
    textList = []
    if begin != len(text)-1:
        if text[begin + 1].strip() == "$S$":
            textList.append(text[begin])
            return textList
        else:
            textList.append(text[begin])
            textList = textList + recursiveText(text, begin + 1)
            return textList
    #if the next element IS the last element
    else:
        textList.append(text[begin])
        return textList

def mainMenu():
    sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('Welcome to Power Presenting Notes!')],
            [sg.Button('Start')],
            [sg.Sizegrip()]]
            

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, element_justification='c', icon="PPN.ico", keep_on_top = False, finalize = True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Start':
            window.close()
            inputWindow()

    window.close()

def inputWindow():
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    
    sg.theme('Reddit')   # Add a touch of color
    
    # list of  items in the dropdown menu
    selection = ('Opacity', 'Timer', 'Theme', 'Font', 'Font Size', 'Speech to Text') 

    # All the stuff inside your window.
    layout = [  
        [sg.Text('Title:'), sg.InputText(size=(30)), sg.Text('Note 1', key='NoteCount'), sg.Button('Add Note'), sg.Combo(selection, enable_events=True, key='-COMBO-', default_value= 'Options')],
        [sg.Button('<-'), sg.Multiline(key="TextInput", size=(50,20), expand_x=True, expand_y=True), sg.Button('->')],
        [sg.Button('Opacity'), sg.Button('Debug Button')],
        [sg.Button('Save'), sg.Push(), sg.Button('Read Note'), sg.Button('Close')],
        [sg.Text('Debug', key='Debug')],
        [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")],
        [sg.Sizegrip()]
        ]
            

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = False, finalize = True)
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Save': # saves the value in the text input into a file
            print('You entered Title: ' + values[0] + ' and contents: ' + values['TextInput'])
            writeToFile("myfile.txt", values[0], values['TextInput'])
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == 'Debug Button': # Reads the value from the first line of the file and displays it in the Debug text NOT FUNCTIONAL
            window['Debug'].update(readFromFile("myfile.txt"))
        elif event == "Submit":
            print(values["-IN-"])
        elif event == "Opacity":
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
            #choice, _ = sg.Window('Settings', [[sg.T('Would you like to return?')], [sg.Yes(s=10), sg.No(s=10)]], disable_close=True).read(close=True)
            #if(choice == "Yes"):
                #print("answer was yes")
            #elif(choice == "No"):
                #print("answer was no")
        elif event == 'Read Note':
            window.close()
            outputWindow()

    window.close()

def outputWindow():
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    noteCounter = 0
    print(noteCounter)
    
    sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('NOTES:', key="title")],
                [sg.Button('<-'), sg.Text(size=(50, 20), key="body", background_color="light gray"), sg.Button('->')],
                [sg.Button('Return'), sg.Button('Fade'), sg.Push(), sg.Button('Close')],
                [sg.Sizegrip()]]

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = True, finalize = True)

    notes = readFromFile("myfile.txt")
    window['title'].update('NOTES: ' + notes[0][0])
    bodyStr = ""
    for x in range(len(notes[0])-1):
        bodyStr += notes[0][x+1]
    window['body'].update(bodyStr)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Return': # Returns to the inputWindow
            window.close()
            inputWindow()
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == '<-':
            if(noteCounter > 0):
                noteCounter = noteCounter - 1
                window['title'].update('NOTES: ' + notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['body'].update(bodyStr)
        elif event == '->':
            if(noteCounter < len(notes)-1):
                noteCounter = noteCounter + 1
                window['title'].update('NOTES: ' + notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['body'].update(bodyStr)

    window.close()
    
mainMenu()
