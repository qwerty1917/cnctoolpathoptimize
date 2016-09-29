#-*- coding: utf-8 -*-
__author__ = 'hyeongminpark'
""" Written by --
    __  __                                       _          ____             __
   / / / /_  _____  ____  ____  ____ _____ ___  (_)___     / __ \____ ______/ /__
  / /_/ / / / / _ \/ __ \/ __ \/ __ `/ __ `__ \/ / __ \   / /_/ / __ `/ ___/ //_/
 / __  / /_/ /  __/ /_/ / / / / /_/ / / / / / / / / / /  / ____/ /_/ / /  / ,<
/_/ /_/\__, /\___/\____/_/ /_/\__, /_/ /_/ /_/_/_/ /_/  /_/    \__,_/_/  /_/|_|
      /____/                 /____/

Date : May 21 2015
"""


import _makeLine, _drawLine, os, sys
from constants import *
import random
import math
import time

tmpLines = []

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def drawRandCuttingLines(linesCount, arcsCount):
    linesToDraw = _makeLine.generateRandCuttingLines(linesCount) + _makeLine.generateRandCuttingArcs(arcsCount)
    _drawLine.drawCuttingLines(linesToDraw)
    return linesToDraw


def drawDefinedCuttingLines(lines):
    _drawLine.drawCuttingLines(lines)
    return lines


def gcodeToList(dir):
    f = open(dir, 'r')
    gcodeLines=[]
    gcodeLinesSliced=[]
    print("======= file: " + dir + " =======")
    while True:
        line = f.readline()
        gcodeLines.append(line)
        if not line: break
        print(line, end='')
    print("\n======= file end =======")
    f.close()

    for line in gcodeLines:
        tmpSlicedLine = line.split()
        if len(tmpSlicedLine) > 0:
            gcodeLinesSliced.append(line.split())
        else:
            pass

    gcode = 'G00'
    xcode = 'X0'
    ycode = 'Y0'
    zcode = 'Z0'
    rcode = ''

    gcodeAugmented = []
    for lineList in gcodeLinesSliced:
        tmpLine = []
        isRcode = False
        isM00 = False
        for command in lineList:
            if command[0] in ['g', 'G']:
                if command[1:] in ['00', '01', '02', '03']:
                    gcode = command
            elif command[0] in ['x', 'X']:
                xcode = command
            elif command[0] in ['y', 'Y']:
                ycode = command
            elif command[0] in ['z', 'Z']:
                zcode = command
            elif command[0] in ['r', 'R']:
                rcode = command
                isRcode = True
            elif command in ['m00', 'M00']:
                isM00 = True

        if isRcode:
            tmpLine.extend([gcode, xcode, ycode, zcode, rcode])
        elif isM00:
            continue
        else:
            tmpLine.extend([gcode, xcode, ycode, zcode])
        gcodeAugmented.append(tmpLine)

    resultList = []
    lastPoint = [0,0,0]
    for line in gcodeAugmented:
        tmpEndX = 0
        tmpEndY = 0
        tmpEndZ = 0
        tmpR = 0
        Gcode = ''

        for code in line:
            if 'X' in code:
                tmpEndX = float(code.replace('X',''))
            elif 'Y' in code:
                tmpEndY = float(code.replace('Y',''))
            elif 'Z' in code:
                tmpEndZ = float(code.replace('Z',''))
            elif 'R' in code:
                tmpR = float(code.replace('R',''))
            elif 'G' in code:
                Gcode = code
            else:
                print("something else g, x, y, z, r detected : " + code)
        tmpEndPoint = [tmpEndX,tmpEndY,tmpEndZ]
        if Gcode == 'G01':
            resultList.append([lastPoint, tmpEndPoint, LINE])
        elif Gcode == 'G02':
            resultList.append([lastPoint, tmpEndPoint, ARC, tmpR, CW])
        elif Gcode == 'G03':
            resultList.append([lastPoint, tmpEndPoint, ARC, tmpR, CCW])
        elif Gcode == 'G00':
            resultList.append([lastPoint, tmpEndPoint, MOVE])
            pass

        lastPoint = tmpEndPoint

        #resultList로 변환한다.
        pass

    #### 테스트용 코드
    # for lineList in resultList:
    #     print(lineList)

    return resultList


def listToGcode(list):
    resultGcode = ''
    for line in list:
        if line[SHAPE] == MOVE:
            resultGcode += '\nG00' + ' X' + str(line[E][X]) + ' Y' + str(line[E][Y]) + ' Z' + str(line[E][Z])
        elif line[SHAPE] == LINE:
            resultGcode += '\nG01' + ' X' + str(line[E][X]) + ' Y' + str(line[E][Y]) + ' Z' + str(line[E][Z])
        elif line[SHAPE] == ARC:
            if line[DIR] == CW:
                resultGcode += '\nG02' + ' X' + str(line[E][X]) + ' Y' + str(line[E][Y]) + ' Z' + str(line[E][Z]) + ' R' + str(line[RAD])
            elif line[DIR] == CCW:
                resultGcode += '\nG03' + ' X' + str(line[E][X]) + ' Y' + str(line[E][Y]) + ' Z' + str(line[E][Z]) + ' R' + str(line[RAD])
            else: print('\n>>>> error: not CW or CCW')
        else: print('\n>>>> error: not in MOVE, LINE, ARC')

    return resultGcode


def getTotalMovingLength(lineList):
    result = 0
    for line in lineList:
        result += math.sqrt((line[S][X]-line[E][X])**2 +
                  (line[S][Y]-line[E][Y])**2 +
                  (line[S][Z]-line[E][Z])**2)
    return result

def getLineLenght(line):
    result = math.sqrt((line[S][X]-line[E][X])**2 +
                       (line[S][Y]-line[E][Y])**2 +
                       (line[S][Z]-line[E][Z])**2)

    return result

def uniqueList(list):
    result = [e for i, e in enumerate(list) if list.index(e) == i]
    return result


def addRandomMovingLines(lines):

    random.shuffle(lines)
    resultLines = []

    datumPoint = [0, 0, 0]
    startingPoint = datumPoint
    while lines:
        tmpCuttingLine = lines.pop()
        tmpMovingLine = [startingPoint, tmpCuttingLine[S], MOVE]

        resultLines.append(tmpMovingLine)
        resultLines.append(tmpCuttingLine)

        startingPoint = tmpCuttingLine[E]

    resultLines.append([startingPoint, datumPoint, MOVE])
    return resultLines

def evolveMovingLine(lines):

    toolbar_width = 40

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    # result = sorted(movingLinesPop, key=getTotalMovingLength)[0]

    initialLength = getTotalMovingLength(lines)

    cuttingLines = []
    movingLinesPop = []

    for line in lines:
        if line[SHAPE] in [LINE, ARC]:
            cuttingLines.append(line)

    # 랜덤한 개체 개체군 생성
    for i in range(POPULATION):
        datumPoint = [0, 0, 0]
        startingPoint = datumPoint

        random.shuffle(cuttingLines)
        randCuttingLines = cuttingLines[:]

        movingLinesEntity = []
        while randCuttingLines:
            tmpCuttingLine = randCuttingLines.pop()
            tmpMovingLine = [startingPoint, tmpCuttingLine[S], MOVE]

            movingLinesEntity.append(tmpMovingLine)
            movingLinesEntity.append(tmpCuttingLine)

            startingPoint = tmpCuttingLine[E]

        movingLinesEntity.append([startingPoint, datumPoint, MOVE])

        movingLinesPop.append(movingLinesEntity)

    progress = 0
    for i in range(GENERATION):

        parents = sorted(movingLinesPop, key=getTotalMovingLength)

        parent1 = parents[0]
        parent2 = parents[1]

        parent1Cutting = []
        for line in parent1:
            if line[SHAPE] in [LINE, ARC]:
                parent1Cutting.append(line)

        # print(len(parent1Cutting))

        parent2Cutting = []
        for line in parent2:
            if line[SHAPE] in [LINE, ARC]:
                parent2Cutting.append(line)

        # print(len(parent2Cutting))

        children1 = []
        children2 = []

        #### 새 알고리즘

        movingLinesPop = []

        for j in range(BIRTHRATE):

            # 교차 발생 코드
            cutPoint1 = 0
            cutPoint2 = 0

            cutPoint1 = cutPoint2 = random.randrange(0, len(parent1Cutting))
            while(cutPoint1 == cutPoint2):
                cutPoint2 = random.randrange(0, len(parent2Cutting))

            if cutPoint2 < cutPoint1:
                tmp = cutPoint1
                cutPoint1 = cutPoint2
                cutPoint2 = tmp

            latterLength = len(parent1Cutting) - cutPoint2

            prt1Mid = parent1Cutting[cutPoint1:cutPoint2]
            prt2Mid = parent2Cutting[cutPoint1:cutPoint2]

            prt1Reordered = parent1Cutting[cutPoint2:] + parent1Cutting[:cutPoint2]
            prt2Reordered = parent2Cutting[cutPoint2:] + parent2Cutting[:cutPoint2]

            prt1ReordFiltered = list(filter(lambda x: x not in prt2Mid, prt1Reordered))
            prt2ReordFiltered = list(filter(lambda x: x not in prt1Mid, prt2Reordered))

            child1 = prt2ReordFiltered[-cutPoint1:] + prt1Mid + prt2ReordFiltered[:latterLength]
            child2 = prt1ReordFiltered[-cutPoint1:] + prt2Mid + prt1ReordFiltered[:latterLength]


            # 돌연변이 발생 코드
            for index, child in enumerate([child1, child2]):
                if random.random() < MUTATION:
                    cutPoint1 = 0
                    cutPoint2 = 0

                    cutPoint1 = cutPoint2 = random.randrange(0, len(child))
                    while(cutPoint1 == cutPoint2):
                        cutPoint2 = random.randrange(0, len(child))

                    front = child[:cutPoint1]
                    mid = child[cutPoint1:cutPoint2]
                    rear = child[cutPoint2:]

                    random.shuffle(mid)

                    if index == 0:
                        tmp = front + mid + rear
                        if len(tmp) == len(child):
                            child1 = tmp
                    elif index == 1:
                        tmp = front + mid + rear
                        if len(tmp) == len(child):
                            child2 = tmp

            datumPoint = [0, 0, 0]

            children = []
            for child in [child1, child2]:
                startingPoint = datumPoint
                movingLinesEntity = []
                while child:
                    tmpCuttingLine = child.pop()
                    tmpMovingLine = [startingPoint, tmpCuttingLine[S], MOVE]

                    movingLinesEntity.append(tmpMovingLine)
                    movingLinesEntity.append(tmpCuttingLine)

                    startingPoint = tmpCuttingLine[E]

                movingLinesEntity.append([startingPoint, datumPoint, MOVE])
                movingLinesPop.append(movingLinesEntity)

        ### 새 알고리즘 이까지
        if progress != math.floor((i/GENERATION) * toolbar_width):
            sys.stdout.write(">>>> Evolve progress: %d%% " % (5*progress/2) + "[[" + "#"*progress + " "*(toolbar_width-progress) + "]]\r")
            sys.stdout.flush()
        progress = math.floor((i/GENERATION) * toolbar_width)
    progress = toolbar_width
    sys.stdout.write(">>>> Evolve progress: %d%% " % (5*progress/2) + "[[" + "#"*progress + " "*(toolbar_width-progress) + "]]\r")
    sys.stdout.write("\n")
    result = sorted(movingLinesPop, key=getTotalMovingLength)[0]
    finalLength = getTotalMovingLength(result)

    return [result, initialLength, finalLength]

def printEfficiency(result):
    print("============== Efficiency ==============")
    print("*** initial total length: "+ str(round(result[INITIAL_LENGTH], 2)))
    print("*** final total length: "+ str(round(result[FINAL_LENGTH], 2)))
    print("*** path length reduction : "+ str(round((1-result[FINAL_LENGTH]/result[INITIAL_LENGTH])*100, 2)) + " %")
    print("========================================")

def storeGcode(result):
    while True:
        tmpInput = input('\n>>>> Do you want to store the path in G-code? [ Y, N ]\n>>>> input: ')
        if tmpInput in ['Y', 'y']:
            fileName = input('\n>>>> Input file name you want to store. \n>>>> input: ')
            path = './outPutFiles/' + fileName + '.txt'
            strToWrite = listToGcode(result[RESULT])

            newFile = open(path, 'w')
            newFile.write(strToWrite)
            newFile.close()
            print("======= file: ./outPutFiles/" + fileName + ".txt =======")
            print(strToWrite)
            print("======= file end =======")
            break
        elif tmpInput in ['N', 'n']:
            break
        else:
            print('\n>>>> wrong input.')



def whenRandom():
    while(True):
        defaultCountOrNotInput = input('\n>>>> Do you want to use default number of line and arcs? [ Y, N ]\n'
                                       + ' the default number of lines is '+ str(CUTTING_LINE_COUNT)+' and '
                                       + 'the default number of arcs is '+ str(CUTTING_ARC_COUNT)+'.'+'\ninput: ')
        if defaultCountOrNotInput in ['y', 'Y']:
            tmpLines = drawRandCuttingLines(CUTTING_LINE_COUNT, CUTTING_ARC_COUNT)
            tmpLines = addRandomMovingLines(tmpLines)
            drawDefinedCuttingLines(tmpLines)
            result = evolveMovingLine(tmpLines)
            drawDefinedCuttingLines(result[RESULT])
            printEfficiency(result)
            storeGcode(result)
            break
        elif defaultCountOrNotInput in ['n', 'N']:
            numberOfLines = input('\n>>>> input number of lines\ninput: ')
            numberOfArcs = input('\n>>>> input number of arcs\ninput: ')

            tmpLines = drawRandCuttingLines(int(numberOfLines), int(numberOfArcs))
            tmpLines = addRandomMovingLines(tmpLines)
            drawDefinedCuttingLines(tmpLines)
            result = evolveMovingLine(tmpLines)
            drawDefinedCuttingLines(result[RESULT])
            printEfficiency(result)
            storeGcode(result)
            break
        else:
            print('\n>>>> wrong input.')


def whenNotRandom():

    # 파일로 G code 입력 받아 gcodeToList()로 변환
    fileList = []
    print('\n>>>> you have files printed below. choose one.' +
          '\n====================')
    for root, dirs, files in os.walk('./pathFile/'):
        for index, file in enumerate(files):
            print(str(index+1) + " " + file)
            fileList.append(file)
    print('====================')

    while(True):
        fileIndexToOpenStr = input('\n>>>> input file index: ')
        if RepresentsInt(fileIndexToOpenStr):
            fileIndexToOpen = int(fileIndexToOpenStr)
            if fileIndexToOpen-1 in range(len(fileList)):
                cuttingLines = gcodeToList('./pathFile/'+fileList[fileIndexToOpen-1])
                drawDefinedCuttingLines(cuttingLines)

                if input("\n>>>> input Y to generate and evolve MOVING LINES. if you don't want, input any key except Y. [ Y, * ] \ninput: ") in ['y', 'Y']:
                    cuttingLines = addRandomMovingLines(cuttingLines)
                    drawDefinedCuttingLines(cuttingLines)
                    result = evolveMovingLine(cuttingLines)
                    drawDefinedCuttingLines(result[RESULT])
                    printEfficiency(result)
                    storeGcode(result)

                break
            else:
                if len(fileList) >= 2:
                    print('\n>>>> wrong input. please input between 1 and ' + str(len(fileList)) + '.')
                else:
                    print('\n>>>> wrong input. there is only one file and you can use file 1 only.')
        else:
            print('\n>>>> wrong input. your input is not integer.')

name = """
 _   _                                        _        ______          _
| | | |                                      (_)       | ___ \        | |
| |_| |_   _  ___  ___  _ __   __ _ _ __ ___  _ _ __   | |_/ /_ _ _ __| | __
|  _  | | | |/ _ \/ _ \| '_ \ / _` | '_ ` _ \| | '_ \  |  __/ _` | '__| |/ /
| | | | |_| |  __/ (_) | | | | (_| | | | | | | | | | | | | | (_| | |  |   <
\_| |_/\__, |\___|\___/|_| |_|\__, |_| |_| |_|_|_| |_| \_|  \__,_|_|  |_|\_\\
        __/ |                  __/ |
       |___/                  |___/                                         """
def interface():
    print(name)
    while(True):
        RorNRinput = input('\n>>>> input "R" if you want random cutting lines or input "NR" [ R, NR ]\n>>>> to quit program, input "Q". [ Q ]\ninput: ')
        if RorNRinput in ['r', 'R']:
            whenRandom()
        elif RorNRinput in ['nr', 'NR']:
            whenNotRandom()
        elif RorNRinput in ['q', 'Q']:
            break
        else:
            print('\n>>>> wrong input.')

# print('aaa')
# import prototype
interface()