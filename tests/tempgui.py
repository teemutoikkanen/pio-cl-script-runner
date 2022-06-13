import PySimpleGUI as sg
positionList = ["UTG8","UTG7","LJ","HJ","CO","BTN","SB","BB"]

# All the stuff inside your window.
layout = [  [sg.Text('eff stack')],
            [sg.Combo(list(range(8,100,2)), key='stack')],
            [sg.Text('rfi pos')],
            [sg.Combo(positionList, key = 'rfi_pos')],
            [sg.Text('cc pos')],
            [sg.Combo(positionList, key = 'cc_pos')],
            [sg.Text('Enter Flop')],
            [sg.Text(''), sg.InputText(key='flop')],
            [sg.Button('Ok'), sg.Button('Close Window')],
            [sg.Multiline(size=(30, 5), key='textbox')]]  # identify the multiline via key option

# Create the Window
window = sg.Window('Test', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    print('You entered in the textbox:')
    print(values['stack'], values['rfi_pos'], values['cc_pos'],values['flop'])  # get the content of multiline via its unique key

window.close()