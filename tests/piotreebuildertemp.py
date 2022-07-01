import glob
from shutil import copyfile
import datetime

import os



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


def get_ranges(stackDepth, rfiPos, ccPos, board):
    # temp inputs
    rngFilepath = "./MTTranges/" + str(stackDepth) + "bb/*.rng"
    filePath = "./MTTranges/" + str(stackDepth) + "bb/"



    # luodaan inputeista haluttu tiedostonimi
    ### esim 30bb CO R BTN C halutaan /30bb kansiosta 0.0.0.0.0.4xxx.1

    # etsitään tiedosto. tarkkoja reissukoot pitää ignoraa. eli otetana lista kaikista tiedostoista /30bb kansiosta
    # ja siitä otetaan tarkka fn



    #### RFI rangen haku
    rfiPosNum = positionList.index(rfiPos)

    #TODO 1.get tiedostonimilista 2. etsi sieltä str missä posNum:s alkaa 4:lla ja toka posNum alkaa 1? riittää SRP?

    files = glob.glob(rngFilepath)
    rfiFname = ""
    #loopataan range tiedostot
    for i in range(len(files)):
        fname = files[i].split("\\")[1].strip(".rng")

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
        #         print("HEPHEP")
        #         rfiPioRange = pathToPioRange(filePath, fname)
        #         rfiFname = fname
                


    #### cc-filu haku - lisätään vaan 0:t ja 1:t
    ccPosNum = positionList.index(ccPos)
    ccFname = rfiFname
    for i in range(ccPosNum-rfiPosNum-1):
        ccFname += ".0"

    ccFname += ".1"
    print("RFI file name:",rfiFname)
    print("CC file name:", ccFname)

    ccPioRange = pathToPioRange(filePath, ccFname)



    #PIO SCRIPTIN LUONTI

    #avataan pohja ja muokataan

    with open('./pio-script-template.txt', 'r') as file:
        data = file.read()

        pioScriptFileList = data.split("\n")

        if (ccPos == "SB" or ccPos == "BB"):
            pioScriptFileList[1] = "#Range0#" + ccPioRange
            pioScriptFileList[2] = "#Range1#" + rfiPioRange

            pioScriptFileList[4] = "#Pot#" + str(21+21+5+10)
            pioScriptFileList[5] = "#EffectiveStacks#" + str(stackDepth*10-21)

        else:
            pioScriptFileList[1] = "#Range0#" + rfiPioRange
            pioScriptFileList[2] = "#Range1#" + ccPioRange

            pioScriptFileList[4] = "#Pot#" + str(21+21+5+10+10)
            pioScriptFileList[5] = "#EffectiveStacks#" + str(stackDepth*10-21)

        pioScriptFileList[3] = "#Board#" + board

        
        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H%M") #strftime("%d-%m-%Y %H%M")
        path1 = ".\\PioTreefiles\\"
        fname3 =  dateTime + " Pio Tree File " + rfiPos + " vs " + ccPos + " " + str(stackDepth) + "bb " + board + ".txt"
        with open(path1 + fname3, "w") as file2:
            for line in pioScriptFileList:
                file2.write("%s\n" % line)
        
        print("Saved to", path1+fname3)
        

        path_pio = "C:\\PioSOLVER2edge\\TreeBuilding\\PYTHON SCRIPT\\"
        copyfile(path1+fname3,path_pio+fname3 )




    

if (__name__ == "__main__"):

    # stackDepth = int(input("Stack Depth (15,20,30,40,60,100): "))
    # rfiPos = input("RFI position (UTG8, ... , BB): ")
    # ccPos = input("CC position (UTG8, ... , BB): ")
    # board = input("Flop (Jh 8h 7d): ")

    [stackDepth, rfiPos, ccPos, board] = input("[Stack] [rfi pos] [cc pos] [board] ---- eg. ""60 BTN BB JhTh7s"" ---- (15,20,30,40,60, UTG8..BB)\n").split(" ")

   
    try: 
        get_ranges(int(stackDepth), rfiPos, ccPos, board)
    except Exception as e:
        print(e)

    os.system("pause")

    input("Press enter to exit")













    