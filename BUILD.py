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


def main1():
    layout = [
            [sg.Text('eff stack')],
            [sg.Combo(list(range(8,100,2)), default_value=20, key='stack')],
            [sg.Text('rfi pos')],
            [sg.Combo(positionList, default_value='LJ', key = 'rfi_pos')],
            [sg.Text('cc pos')],
            [sg.Combo(positionList, default_value='BB', key = 'cc_pos')],
            [sg.Text('Enter Flop')],
            [sg.InputText(default_text="2c2h2d", key='flop')],
            [sg.Text('flop betting scheme')],
            [sg.Combo(flop_betsizes, key = 'flop_betsizes')],
            [sg.Button('Run', bind_return_key=True), sg.Button('Exit')]

        ]

    window = sg.Window('Realtime Shell Command Output', layout)
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Run':
            window.close()
            main(int(values['stack']), values['rfi_pos'], values['cc_pos'], values['flop'], values['flop_betsizes'])
            break

    window.close()


main1()