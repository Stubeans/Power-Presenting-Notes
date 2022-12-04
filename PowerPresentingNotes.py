from tkinter import *
import PySimpleGUI as sg

## Method to write to file 
# Takes in a fileName (Text file needs to be in the same file header as this .py file)
# A title (type String), and a body (stype String) and adds them to the end of the txt file including necessary formatting
def writeToFile(fileName, title, body):
    #f = open(fileName, "w")
    f = open(fileName, "a")
    f.write("$S$\n"+ title + "\n")
    f.write(body + "\n")
    f.close()

## Method to read to file 
# Takes in a fileName and returns a formatting List in the following format:
# List[Note][X] where X = 0 for Title | 1-n for Body strings
def readFromFile(fileName):
    f = open(fileName, "r")
    text = f.readlines()
    returnText = []
    for x in range(len(text)):
        if text[x].strip() == "$S$":
            returnText.append(recursiveText(text, x+1))
    f.close()
    return returnText

# A helper function for readFromFile. Once a $S$ is found, which is a custom code used to distinguish breaks between notes, this function is triggered
# The function starts at the begin variable, which simply designates which line to start on in the text, the text being the .txt file's lines
# It appends each following line to the textList which is essentially the body of the note, until another $S$ is found, or the end of the file is reached.
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

# Self-Explanatory
def clearFile(fileName):
    f = open(fileName, "w")
    f.close()

# Takes a fileName and completely rewrites it using new data (data being a formatted list in the following format: )
# data[Note][X] where X = 0 for Title | 1-n for Body strings
def overWriteFile(fileName, data):
    clearFile(fileName)
    f = open(fileName, "a")
    for note in data:
        f.write("$S$\n" + note[0])
        for x in range (len(note)-1):
            f.write(note[x+1])
    f.close()

# This function handles the main menu portion of our app
def mainMenu():
    # Designates the theme of the window
    sg.theme('Reddit')

    # All the stuff inside your window.
    layout = [  [sg.Text('Welcome to Power Presenting Notes!', text_color="Black")],
            [sg.Button('Start')],
            [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")],
    
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

# This function handles the setting of user preferences
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

# This function handles the input window of our app
def inputWindow(file):
   
   # counter keeps track of the current fade element, transparencyOptions handles fade values stored in a list
   # noteCounter keeps track of which note the user is currently viewing
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    noteCounter = 0
    
    sg.theme('Reddit')   # Add a touch of color

    #attempt to add image as button 
    #sg.set_options(font=font)
    #colors = (sg.theme_background_color(), sg.theme_background_color())
    
    # All the stuff inside your window.
    layout = [  
        [sg.Text('Title:'), sg.InputText(size=(30), key='title'), sg.Text('Note 1', key='NoteCount'), sg.Button('Add Note'), 
        sg.Button('Options')],
        [sg.Button('<-'), sg.Multiline(key="TextInput", size=(50,20), expand_x=True, expand_y=True), sg.Button('->')],
        [sg.Button('Opacity'), sg.Button('Swap'), sg.Text('note #'), sg.InputText(size=(2), key='note1'), sg.Text('with note #'), sg.InputText(size=(2), key='note2'), sg.Push(), sg.Button(' Return ')],
        [sg.Button('  Save  '), sg.Push(), sg.Button('Present')],
        [sg.Button('Close')],
        #[sg.Button('Fade\nAway', button_color=colors, image_data='C:\Users\Sherap\PPN\Fade.png',border_width=0)],




        [sg.Sizegrip()]
        ]
            

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", element_justification='c', keep_on_top = False, finalize = True)

    # This fills the Title and Body fields with text from the .txt file
    notes = readFromFile(file)
    title = notes[0][0]
    title = title.replace('\n', '')
    window['title'].update(title)
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
        elif event == '  Save  ': # saves the value in the text inputs into the current file
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
        elif event == 'Add Note': # Adds a note to the .txt file, while moving the user to the new note inside the app
            writeToFile(file, "default title", "default body")
            notes = readFromFile(file)
            noteCounter = len(notes) - 1
            window['NoteCount'].update("Note " + str(noteCounter + 1))
            window['title'].update(notes[noteCounter][0])
            bodyStr = ""
            for x in range(len(notes[noteCounter])-1):
                bodyStr += notes[noteCounter][x+1]
            window['TextInput'].update(bodyStr)
        elif event == ' Return ': # Returns you to the previous screen
            window.close()
            mainMenu()
        elif event == "Opacity": # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == 'Present': # Presents the notes by opening the output window
            window.close()
            outputWindow(file)
        elif event == '<-': # reduces the noteCounter by 1, and updates the NoteCount, Title and Body fields accordingly
            if(noteCounter > 0):
                noteCounter = noteCounter - 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                title = notes[noteCounter][0]
                title = title.replace('\n', '')
                window['title'].update(title)
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['TextInput'].update(bodyStr)
        elif event == '->': # increases the noteCounter by 1, and updates the NoteCount, Title and Body fields accordingly
            if(noteCounter < len(notes)-1):
                noteCounter = noteCounter + 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                title = notes[noteCounter][0]
                title = title.replace('\n', '')
                window['title'].update(title)
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['TextInput'].update(bodyStr)
        elif event == 'Swap': # Swaps the two notes indicated in inputText's 'note1' and 'note2' and overwrites the text file
            notes = readFromFile(file)
            note1 = int(values['note1']) - 1
            note2 = int(values['note2']) - 1
            if(note1 > len(notes) - 1 or note2 > len(notes) - 1 or note1 < 1 or note2 < 1):
                print("Not valid note numbers")
            else:
                temp = notes[note1]
                notes[note1] = notes[note2]
                notes[note2] = temp
                overWriteFile(file, notes)

    window.close()

# This function handles the output window of our app
def outputWindow(file):

    # counter keeps track of the current fade element, transparencyOptions handles fade values stored in a list
    # noteCounter keeps track of which note the user is currently viewing
    counter = 0
    transparencyOptions = [0.75, 0.5, 1]
    noteCounter = 0
    
    #sg.theme('Reddit')   # Add a touch of color

    # All the stuff inside your window.
    layout = [  [sg.Text('NOTES:', key="title"), sg.Push(), sg.Text('Note 1', key='NoteCount')],
                [sg.Button('<-'), sg.Text(size=(50, 20), key="body", background_color="light gray"), sg.Button('->')],
                [sg.Button('Return'), sg.Button('Opacity'), sg.Push(), sg.Button('Close')],
                [sg.Sizegrip()]]

    # Create the Window
    window = sg.Window('Power Presenting Notes', layout, icon="PPN.ico", keep_on_top = True, finalize = True)

    # This fills the Title and Body fields with text from the .txt file
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
        elif event == 'Opacity': # Runs through fade options on a button loop
            window.set_alpha(transparencyOptions[counter%3])
            counter += 1
        elif event == '<-': # reduces the noteCounter by 1, and updates the NoteCount, Title and Body fields accordingly
            if(noteCounter > 0):
                noteCounter = noteCounter - 1
                window['NoteCount'].update("Note " + str(noteCounter + 1))
                window['title'].update('NOTES: ' + notes[noteCounter][0])
                bodyStr = ""
                for x in range(len(notes[noteCounter])-1):
                    bodyStr += notes[noteCounter][x+1]
                window['body'].update(bodyStr)
        elif event == '->': # increases the noteCounter by 1, and updates the NoteCount, Title and Body fields accordingly
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
