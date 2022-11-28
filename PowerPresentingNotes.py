from distutils.log import debug
from tkinter import font
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

def clearFile(fileName):
    f = open(fileName, "w")
    f.close()

def overWriteFile(fileName, data):
    clearFile(fileName)
    f = open(fileName, "a")
    for line in data:
        f.write("$S$\n" + line[0])
        for x in range (len(line)-1):
            f.write(line[x+1])
    f.close()


def mainMenu():
    #sg.theme(settings['theme'])   # Add a touch of color

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
            inputWindow("myfile.txt")
        
    window.close()


def create_settings_window():
    #sg.theme(settings['theme'])

    #selections in options menu
    font_selections = ('Font', 'font', 'font', 'font')
    font_size = ('1', '2', '3')
    theme_selections = ('Dark', 'Light', 'Reddit')
    timer_selections = ('1', '2', '3')
    opacity_selections = ('1', '2', '3')
    speechToText_selections = ('Enable', 'Disable')


    # list of  items in the dropdown menu
    options_menu_layout = [
        [sg.Text('OPTIONS:')],
        [sg.Text("Select Font"),sg.Push(),(sg.Combo(font_selections, enable_events=True, key='-FONTS-', default_value= 'Font'))],
        [sg.Text('Font Size'), sg.Push(),(sg.Combo(font_size, enable_events=True, key='-FONT SIZE-', default_value= '1'))],
        [sg.Text('Timer'), sg.Push(),(sg.Combo(timer_selections, enable_events=True, key='-TIMER-', default_value= '1'))], 
        [sg.Text('Theme'), sg.Push(),(sg.Combo(theme_selections, enable_events=True, key='-THEME-', default_value= 'reddit'))], 
        [sg.Text('Opacity'), sg.Push(),(sg.Combo(opacity_selections, enable_events=True, key='-OPACITY-', default_value= '1'))], 
        [sg.Text('Speech to Text'), sg.Push(),(sg.Combo(speechToText_selections, enable_events=True, key='-SPEECH TO TEXT-', default_value= 'Disabled'))],
        [sg.Text('Alignment')],
        [sg.Button('Return'), sg.Push(),sg.Button('Save')]
    ]

    window = sg.Window('Settings', options_menu_layout, keep_on_top=True, finalize=True)

    return window

def inputWindow(file):
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    noteCounter = 0
    
    sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  
        [sg.Text('Title:'), sg.InputText(size=(30), key='title'), sg.Text('Note 1', key='NoteCount'), sg.Button('Add Note'), sg.Button('Options')],
        [sg.Button('<-'), sg.Multiline(key="TextInput", size=(50,20), expand_x=True, expand_y=True), sg.Button('->')],
        [sg.Button('Opacity'), sg.Button('Debug Button')],
        [sg.Button('Save'), sg.Push(), sg.Button('Read Note'), sg.Button('Close')],
        [sg.Text('Debug', key='Debug')],
        [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")],
        [sg.Sizegrip()]
        ]
            

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = False, finalize = True)

    notes = readFromFile(file)
    window['title'].update(notes[0][0])
    bodyStr = ""
    for x in range(len(notes[0])-1):
        bodyStr += notes[0][x+1]
    window['TextInput'].update(bodyStr)

    
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break
        elif event == 'Options':
            create_settings_window()
            #window = sg.Window("Options Window", options_menu_layout, icon="PPN.ico", keep_on_top = True) 
        elif event == 'Save': # saves the value in the text input into a file
            print("The note before saving looks like: ")
            print(notes)
            print('You entered Title: ' + values['title'] + ' and contents: ' + values['TextInput'])
            notes = readFromFile(file)
            title = values['title']
            title = title.replace('\n', '')
            newLine = [title + "\n", values['TextInput'] + "\n"]
            notes[noteCounter] = newLine
            print("The note after saving looks like: ")
            print(notes)
            overWriteFile(file, notes)
            print("done!")
        elif event == 'Add Note':
            writeToFile(file, "default title", "default body")
            notes = readFromFile(file)
            noteCounter = len(notes) - 1
            window['NoteCount'].update("Note " + str(noteCounter + 1))
            window['title'].update(notes[noteCounter][0])
            bodyStr = ""
            for x in range(len(notes[noteCounter])-1):
                bodyStr += notes[noteCounter][x+1]
            window['TextInput'].update(bodyStr)
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == 'Debug Button': # 
            notes = readFromFile(file)
            print(notes)
            print(parseBody(notes[0]))
            window['Debug'].update("Done!")
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
            outputWindow(file)
        elif event == '<-':
            if(noteCounter > 0):
                noteCounter = noteCounter - 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                window['title'].update(notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['TextInput'].update(bodyStr)
        elif event == '->':
            if(noteCounter < len(notes)-1):
                noteCounter = noteCounter + 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                window['title'].update(notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['TextInput'].update(bodyStr)

    window.close()


def outputWindow(file):
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    noteCounter = 0
    
    #sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('NOTES:', key="title"), sg.Push(), sg.Text('Note 1', key='NoteCount')],
                [sg.Button('<-'), sg.Text(size=(50, 20), key="body", background_color="light gray"), sg.Button('->')],
                [sg.Button('Return'), sg.Button('Fade'), sg.Push(), sg.Button('Close')],
                [sg.Sizegrip()]]

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = True, finalize = True)

    notes = readFromFile(file)
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
            inputWindow(file)
        elif event == 'Fade': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == '<-':
            if(noteCounter > 0):
                noteCounter = noteCounter - 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                window['title'].update('NOTES: ' + notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['body'].update(bodyStr)
        elif event == '->':
            if(noteCounter < len(notes)-1):
                noteCounter = noteCounter + 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                window['title'].update('NOTES: ' + notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['body'].update(bodyStr)

    window.close()
    
mainMenu()
