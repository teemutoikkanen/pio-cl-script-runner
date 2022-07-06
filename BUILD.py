import PySimpleGUI as sg
from main import main
"""
	Demo Program - Realtime output of a shell command in the window
		Shows how you can run a long-running subprocess and have the output
		be displayed in realtime in the window.
    
    Copyright 2022 PySimpleGUI		
"""
positionList = ["UTG8","UTG7","LJ","HJ","CO","BTN","SB","BB"]
flop_betsizes = ["ip-30","ip-30-70", "50", "30-70"]

rPosList = ["rUTG8","rUTG7","rLJ","rHJ","rCO","rBTN","rSB","rBB"]
cPosList = ["cUTG8","cUTG7","cLJ","cHJ","cCO","cBTN","cSB","cBB"]


def main1():

    stacks = [10,12,14,16,18,20,22,24,26,28,30,35,40,45,50,55,60,65,70,80,90]
    # stacks = ["10","12","14"]


    layout = [
            [sg.Text('Stack')],
            [sg.Button(s, key=s, size=(2,1)) for s in stacks],
            [sg.InputText(key='stack', size=(2,1), default_text = 20)],
            [sg.Text('RFI pos')],
            [sg.Button(s[1:], key=s, size=(4,1)) for s in rPosList],
            [sg.InputText(key = 'rfi_pos', size=(5,1), default_text = "LJ")],
            [sg.Text('CC pos')],
            [sg.Button(s[1:], key=s, size=(4,1)) for s in cPosList],
            [sg.InputText(key = 'cc_pos', size=(5,1), default_text = "BB")],
            [sg.Text('Enter Flop')],
            [sg.InputText(default_text="2c2h2d", key='flop')],
            [sg.Text('Flop betsizes')],
            [sg.Button(s, key=s, size=(7,1)) for s in flop_betsizes],
            [sg.InputText(key = 'flop_betsizes', default_text = "30-70")],
            [sg.Button('Run', bind_return_key=True), sg.Button('Tree only')],

        ]

    window = sg.Window('Realtime Shell Command Output', layout)
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "exit"):
            break
        elif event in stacks:
            window['stack'].update(event)
        elif event in rPosList:
            window['rfi_pos'].update(event[1:])
        elif event in cPosList:
            window['cc_pos'].update(event[1:])
        elif event in flop_betsizes:
            window['flop_betsizes'].update(event)
        elif event == 'Run':
            window.close()
            main(int(values['stack']), values['rfi_pos'], values['cc_pos'], values['flop'], values['flop_betsizes'])
            break
        elif event == 'Tree only':
            window.close()
            main(int(values['stack']), values['rfi_pos'], values['cc_pos'], values['flop'], values['flop_betsizes'], 1)
            break


    window.close()


main1()