import PySimpleGUI as sg
from main import main
positionList = ["UTG8","UTG7","LJ","HJ","CO","BTN","SB","BB"]
flop_betsizes = ["ip-30","ip-30-70", "50", "30-70"]


frame_layout = [[sg.Multiline("", size=(80, 20), autoscroll=True,
    reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]]

layout = [  [sg.Text('eff stack')],
            [sg.Combo(list(range(8,100,2)), default_value=20, key='stack')],
            [sg.Text('rfi pos')],
            [sg.Combo(positionList, default_value='LJ', key = 'rfi_pos')],
            [sg.Text('cc pos')],
            [sg.Combo(positionList, default_value='BB', key = 'cc_pos')],
            [sg.Text('Enter Flop')],
            [sg.InputText(default_text="2c2h2d", key='flop')],
            [sg.Text('flop betting scheme')],
            [sg.Combo(flop_betsizes, key = 'flop_betsizes')],
            [sg.Frame("Output console", frame_layout)],
            [sg.Push(), sg.Button("Run")],

]
# Create the Window
window = sg.Window('Test', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "Run":


        print('You entered in the textbox:')
        print(values['stack'], values['rfi_pos'], values['cc_pos'],values['flop'],values['flop_betsizes']) 

        main(int(values['stack']), values['rfi_pos'], values['cc_pos'], values['flop'], values['flop_betsizes'])
        sp = sg.execute_command_subprocess(values['-IN-'], pipe_output=True, wait=False)
        results = sg.execute_get_results(sp, timeout=1)
        print(results[0])



window.close()