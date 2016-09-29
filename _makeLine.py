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

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import math
from constants import *


###########
#	data 정의
###########

def minR(pointS,pointE):
	return (math.sqrt((pointS[X]-pointE[X])**2 + (pointS[Y]-pointE[Y])**2))/2


def generateRandCuttingLines(count):
    # print('generateRandCuttingLines')

    # [[sX, sY, sZ], [eX, eY, eZ], SHAPE]

    resultList = []

    for i in range(count):
        tmpCuttingLine = []
        tmpCuttingLineS = []
        tmpCuttingLineE = []

        tmpCuttingLineS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingLineS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 y좌표 추가
        tmpCuttingLineS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 z좌표 추가

        tmpCuttingLineE.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingLineE.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 y좌표 추가
        tmpCuttingLineE.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 z좌표 추가

        tmpCuttingLine.extend((tmpCuttingLineS, tmpCuttingLineE, LINE))

        resultList.append(tmpCuttingLine)

    # print('line: ' + str(len(resultList)))
    return resultList


def generateRandCuttingArcs(count):
    # print('generateRandCuttingArcs')

    # [[sX, sY, sZ], [eX, eY, eZ], SHAPE, RAD, DIR]

    resultList = []

    for i in range(count):
        tmpCuttingArc = []
        tmpCuttingArcS = []
        tmpCuttingArcE = []
        tmpCuttingArcR = 0
        tmpCuttingArcD = CW

        tmpCuttingArcS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingArcS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 y좌표 추가
        tmpCuttingArcS.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 z좌표 추가

        tmpCuttingArcE.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingArcE.append(rnd.randrange(0, MAX_LENGTH)) # 시작점 y좌표 추가
        tmpCuttingArcE.append(tmpCuttingArcS[Z]) # 시작점 z좌표 추가

        minimumR = minR(tmpCuttingArcS, tmpCuttingArcE)
        maximumR = rnd.randrange(0, MAX_ARC)

        if (math.ceil(maximumR) > minimumR):
            tmpCuttingArcR = rnd.randrange(math.ceil(minimumR), maximumR+1)
        else:
            tmpCuttingArcR = rnd.randrange(math.ceil(minimumR), math.ceil(minimumR)+maximumR+1)

        tmpCuttingArcD = rnd.choice([CW, CCW])

        # tmpCuttingArcD = CCW

        tmpCuttingArc.extend((tmpCuttingArcS, tmpCuttingArcE, ARC, tmpCuttingArcR, tmpCuttingArcD))

        resultList.append(tmpCuttingArc)

    # print('arc: ' + str(len(resultList)))
    return resultList