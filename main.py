import sys
import os
from SolverConnection.solver import Solver
from get_pio_ranges import get_pio_ranges
from get_pio_hand_order import get_pio_hand_order

import subprocess
import datetime


import PySimpleGUI as sg




pio_path = "C:\\PioSOLVER2edge\\PioSOLVER2-edge.exe"
positionList = ["UTG8","UTG7","LJ","HJ","CO","BTN","SB","BB"]


def get_script_range(pio_range):




    ## inits
    pio_hand_order = get_pio_hand_order()
    script_range_arr = [0]*len(pio_hand_order)
    pio_range_arr = pio_range.split(",")
    
    pio_combos_weights_arr = []

    for i in pio_range_arr:
        if (len(i.split(":"))==1):
            pio_combos_weights_arr.append(i + ":1")
        else:
            pio_combos_weights_arr.append(i)

    for i in range(len(pio_hand_order)):
        exact_combo = pio_hand_order[i]



        ## if suited
        if (exact_combo[1] == exact_combo[3]):
            #for each pio combo-weight
            for pio_combo_weight in pio_combos_weights_arr:
                pio_combo = pio_combo_weight.split(":")[0]
                if (str(pio_combo[:2]) == exact_combo[0]+exact_combo[2] and pio_combo[2] == "s"):
                    script_range_arr[i] = pio_combo_weight.split(":")[1]
                
        ## if offsuit (incl pairs)
        if (exact_combo[1] != exact_combo[3]):
            for pio_combo_weight in pio_combos_weights_arr:
                pio_combo = pio_combo_weight.split(":")[0]
                ## len == 2 eli pari (ei s eikä o)
                if(len(pio_combo) == 2):
                    if (str(pio_combo[:2]) == exact_combo[0]+exact_combo[2]):
                        script_range_arr[i] = pio_combo_weight.split(":")[1]
                if (len(pio_combo) == 3):
                    if (pio_combo[2] == 'o'):
                        if (str(pio_combo[:2]) == exact_combo[0]+exact_combo[2]):
                            script_range_arr[i] = pio_combo_weight.split(":")[1]



    return script_range_arr




    # AA:1, AK


    
    return "drep"


def get_add_lines(eff_stack, flop_betsizes):

    add_lines_str = ""
    script_path = "C:\\Users\\Teemu-amd\\Desktop\\PYTHON SCRIPTIT\\pio-script-builder-v2-git\\pio-cl-script-runner\\material\\script-temps\\" + flop_betsizes + ".txt"

    with open(script_path, "r") as f:
        for line in f:
            if ("add_line" in line):

                temp_arr = []
                
                #fix add_lines, siis tsekkaa rivin isoin arvo, jos yli 70% eff_stackista niin pyöristä all_inksi, ja poista sitä suuremmat arvot, ja aina pitää olla maksu vihulle
                lines_arr = line.split(" ")[1:]

                for node in lines_arr:
                    if (int(node) < eff_stack):
                        temp_arr.append(node)
                temp_arr.append(int(eff_stack))

                add_lines_str += "add_line " + ' '.join(str(i) for i in temp_arr) + "\n"
                #add_lines_str += line

    return add_lines_str




def main(stack = 15, r_pos = "LJ", cc_pos = "BTN", board = "2c2d2", flop_betsizes = "50"):


    #init script string


    script_str = "set_algorithm original_pio\n"
    script_str += "set_threads 24\n"
    
    script_str += "set_board " + board + "\n"
    eff_stack = int(stack)*10-21
    script_str += "set_eff_stack " + str(eff_stack) + "\n"
    script_str += "set_isomorphism 1 0\n"


    pot = 0
    if (cc_pos == "BB"):
        pot = 21*2+5+10
        script_str += "set_pot 0 0 " + str(pot)
    elif (cc_pos == "SB"):
        pot = 21*2+10+10
        script_str += "set_pot 0 0 " + str(pot)
    else:
        pot = 21*2+10+10+5
        script_str += "set_pot 0 0 " + str(pot)
    script_str += "\n"

    accuracy_frac = 0.0065
    script_str += "set_accuracy " + str(round(float(pot)*accuracy_frac,3)) + "\n"





    ## connection
    connection = Solver(solver=pio_path)


    ## load load script
    # load_script_status = connection.command(line=f"load_script_silent {temp_script_path}")


    # set_range [OOP/IP] lines
    [r_pio_range, cc_pio_range] = get_pio_ranges(stack,r_pos, cc_pos, board)



    r_script_range_arr = get_script_range(r_pio_range)
    cc_script_range_arr = get_script_range(cc_pio_range)

    r_script_range_str = ' '.join(str(e) for e in r_script_range_arr)
    cc_script_range_str = ' '.join(str(e) for e in cc_script_range_arr)

    #if rfi is OOP
    if (cc_pos == "BB" or cc_pos == "SB"):
        script_str += "set_range OOP " + cc_script_range_str + "\n"
        script_str += "set_range IP " + r_script_range_str + "\n"
    else:
        script_str += "set_range OOP " + r_script_range_str + "\n"
        script_str += "set_range IP " + cc_script_range_str + "\n"




    script_str += "clear_lines\n"



    # add_lines 
    script_str += get_add_lines(eff_stack, str(flop_betsizes))
    # build_tree 
    script_str += "build_tree\n"
    script_str += "estimate_tree\n"

    #gen cfr filename
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H%M")
    filename = str(stack) + "bb-" + r_pos + "-" + cc_pos + "-"+ board + "-" + date_time + ".cfr"
    script_str += 'skip_if_done "Saves\\' + filename + '" next\n'
    script_str += "go 6000 seconds\n"
    script_str += "wait_for_solver\n"
    script_str += 'dump_tree ' + '"Saves\\' + filename + '" no_rivers\n'
    script_str += 'LABEL: next\necho "DONE"\nsolver_time\necho "SCRIPT DONE SAVED IN "' + filename +'"'



    #save new script .txt file



    new_scripts_dir_path = "C:\\Users\\Teemu-amd\\Desktop\\PYTHON SCRIPTIT\\pio-script-builder-v2-git\\pio-cl-script-runner\\scripts-new\\"
    new_script_path = new_scripts_dir_path + filename[0:-4] + ".txt"
    #new_scripts_dir_path + filename[0:-4]
    f = open(new_script_path, "x")
    f.write(script_str)
    f.close()

   

    ## CALL PIO
    subprocess.call(["%s" % pio_path, new_script_path])








    #load script

    # new_script_path_fixed = '"C:\\Users\\Teemu-amd\\Desktop\\PYTHON SCRIPTIT\\pio-script-builder-v2-git\\pio-cl-script-runner\\scripts-new\\"' + filename[0:-4] + ".txt"
    # load_script_status = connection.command(line=f"load_script_silent {new_script_path_fixed}")





if __name__ == "__main__":



    # stack = "15"
    # r_pos = "UTG7"
    # cc_pos = "BB"
    # board = "ThJc3d"

    [stack, r_pos, cc_pos, board] = input("stack r_pos cc_pos board\n").split(" ")
    flop_betsizes = input("betsikoot: [ip-30, ip-30-70, 50, 30-70]\n")

    main(int(stack), r_pos, cc_pos, board, flop_betsizes)

