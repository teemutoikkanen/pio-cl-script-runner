import glob
from shutil import copyfile
import datetime

import os



def getRoundedStack(stackDepth):
    stacks_arr = [15,20,30,40,60,100]

    diff_arr = []

    for stack in stacks_arr:
        diff_arr.append(abs(stack-stackDepth))


    min_idx = diff_arr.index(min(diff_arr))

    return stacks_arr[min_idx]













def pathToPioRange(filePath, fname):

    with open(filePath + fname + ".rng", 'r') as file:
        data = file.read()
        #muokataan pio script muotoon

        dataList = data.split("\n")
        
        
        pioRange = ""
        #for every other line, get combo + weight, lisää stringin jatkeeksi
        for j in range(len(dataList)-1):
            if (j % 2 == 0):
                weight = dataList[j+1].split(";")[0]

                if (weight != "0.0"):
                    
                    if (weight == "1.0"):
                        pioRange += dataList[j] + ","

                    else:
                        comboAndWeight = dataList[j] + ":" + str(round(float(weight),2))
                        pioRange += comboAndWeight + ","
            
        pioRange = pioRange[:-1]

    return pioRange
# inits
positionList = ["UTG8","UTG7","LJ","HJ","CO","BTN","SB","BB"]


def get_pio_ranges(stackDepth, rfiPos, ccPos, board):

    stackDepth = getRoundedStack(stackDepth)

    # temp inputs
    ranges_path = "C:\\Users\\Teemu-amd\\Desktop\\PYTHON SCRIPTIT\\pio-script-builder-v2-git\\pio-cl-script-runner\\MTTranges\\"
    rngFilepath = ranges_path + str(stackDepth) + "bb/*.rng"
    filePath = ranges_path + str(stackDepth) + "bb/"



    # luodaan inputeista haluttu tiedostonimi
    ### esim 30bb CO R BTN C halutaan /30bb kansiosta 0.0.0.0.0.4xxx.1

    # etsitään tiedosto. tarkkoja reissukoot pitää ignoraa. eli otetana lista kaikista tiedostoista /30bb kansiosta
    # ja siitä otetaan tarkka fn






    #### RFI rangen haku
    rfiPosNum = positionList.index(rfiPos)

    #1.get tiedostonimilista 2. etsi sieltä str missä posNum:s alkaa 4:lla ja toka posNum alkaa 1? riittää SRP?

    files = glob.glob(rngFilepath)
    rfiFname = ""
    #loopataan range tiedostot
    for i in range(len(files)):
        fname = files[i].split("\\")[-1].strip(".rng")

        #etsiteään oikea tiedosto
        fnameAsLIst = fname.split('.')

        if (len(fnameAsLIst) == rfiPosNum+1):
            #haetaan RFI filu
            if (fnameAsLIst[rfiPosNum][0] == '4'):
                #jos kaikki edelliset 0, siis jos len(set) == 1 ja eka on 0
                if (len(set(fnameAsLIst[:rfiPosNum])) == 1 and fnameAsLIst[0] == '0'):

                    #luetaan oikea tiedosto
                    rfiPioRange = pathToPioRange(filePath, fname)
                    rfiFname = fname
                #erikoistapaus: eka UTG8 rfi eli ei ookkaan nollia alussa
                elif (len(fnameAsLIst) == 1):
                    rfiPioRange = pathToPioRange(filePath, fname)
                    rfiFname = fname




        # #erikoistapaus: jos ihan eka reissunode eli UTG8r listan pituus 1:
        # else:
        #     if (fnameAsLIst[0] =='4'):
        #         rfiPioRange = pathToPioRange(filePath, fname)
        #         rfiFname = fname
                


    #### cc-filu haku - lisätään vaan 0:t ja 1:t
    ccPosNum = positionList.index(ccPos)
    ccFname = rfiFname
    for i in range(ccPosNum-rfiPosNum-1):
        ccFname += ".0"

    ccFname += ".1"

    print(rfiFname)
    print(ccFname)
    ccPioRange = pathToPioRange(filePath, ccFname)


    return (rfiPioRange, ccPioRange)

