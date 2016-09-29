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

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_aspect('equal')

# 그래프의 범위를 지정. 내부 모형이 이것을 벗어나지 않아야 비율이 유지됨
MAX = 200
for direction in (-1, 1):
    for point in np.diag(direction * MAX * np.array([1,1,1])):
        ax.plot([point[0]], [point[1]], [point[2]], 'w')


###########
#	상수 정의
###########

CUTTING_LINE_COUNT = 5
CUTTING_ARC_COUNT = 5

S = 0
E = 1
SHAPE = 2
RAD = 3
DIR = 4

X = 0
Y = 1
Z = 2

LINE = 0
ARC = 1

CW = 0
CCW = 1

ARC_RESOLUTION = 30

MAX_LENGTH = 100
MAX_ARC = 50

###########
#	data 정의
###########

cuttingLineList = []

def minR(pointS,pointE):
	return (math.sqrt((pointS[X]-pointE[X])**2 + (pointS[Y]-pointE[Y])**2))/2


def generateRandCuttingLines():
	for i in range(CUTTING_LINE_COUNT):
		tmpCuttingLine = []
		tmpCuttingLineS = []
		tmpCuttingLineE = []

		tmpCuttingLineS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 x좌표 추가
		tmpCuttingLineS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 y좌표 추가
		tmpCuttingLineS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 z좌표 추가

		tmpCuttingLineE.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 x좌표 추가
		tmpCuttingLineE.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 y좌표 추가
		tmpCuttingLineE.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 z좌표 추가

		tmpCuttingLine.extend((tmpCuttingLineS, tmpCuttingLineE, LINE))

		cuttingLineList.append(tmpCuttingLine)


def generateRandCuttingArc():
    for i in range(CUTTING_ARC_COUNT):
        tmpCuttingArc = []
        tmpCuttingArcS = []
        tmpCuttingArcE = []
        tmpCuttingArcR = 0
        tmpCuttingArcD = CW

        tmpCuttingArcS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingArcS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 y좌표 추가
        tmpCuttingArcS.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 z좌표 추가

        tmpCuttingArcE.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 x좌표 추가
        tmpCuttingArcE.append(rnd.randrange(-MAX_LENGTH, MAX_LENGTH)) # 시작점 y좌표 추가
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

        cuttingLineList.append(tmpCuttingArc)


###########
#	plot 그리는 부분
###########

def getAngle(vector):
    x = [1,0]
    if vector[Y] > 0:
        return np.arccos(np.dot(vector, x) / (vectLenght(vector) * vectLenght(x)))
    elif vector[Y] < 0:
        return 2 * np.pi - np.arccos(np.dot(vector, x) / (vectLenght(vector) * vectLenght(x)))
    elif vector[Y] == 0 and vector[X] > 0:
        return 0
    elif vector[Y] == 0 and vector[X] < 0:
        return np.pi

def getVect(sX, sY, eX, eY):
    return [eX-sX, eY-sY]

def vectLenght(list):
    return math.sqrt(list[X]**2 + list[Y]**2)

def generateArcPath(arcInfo):
	pass

def drawCuttingLines():
    for count, cuttingLine in enumerate(cuttingLineList):
        if cuttingLine[SHAPE] is LINE:
            x = np.array([cuttingLine[S][X], cuttingLine[E][X]])
            y = np.array([cuttingLine[S][Y], cuttingLine[E][Y]])
            z = np.array([cuttingLine[S][Z], cuttingLine[E][Z]])

            ax.plot(x, y, z, label='Line'+str(count+1))
        elif cuttingLine[SHAPE] is ARC:

            # Arc의 시점과 끝점 있는 선
            x = np.array([cuttingLine[S][X], cuttingLine[E][X]])
            y = np.array([cuttingLine[S][Y], cuttingLine[E][Y]])
            z = np.array([cuttingLine[S][Z], cuttingLine[E][Z]])

            # ax.plot(x, y, z, label='Line(Arc)'+str(count+1))

            # midpoint : 시점과 끝점 사이의 중점이다
            midPoint = [(cuttingLine[S][X] + cuttingLine[E][X])/2,
                        (cuttingLine[S][Y] + cuttingLine[E][Y])/2,
                        (cuttingLine[S][Z] + cuttingLine[E][Z])/2]

            # alpha : 중점과 시점 사이의 거리이다. 즉, 시점과 끝점 사이 거리의 절반이다.
            alpha = math.sqrt((midPoint[X] - cuttingLine[S][X]) ** 2 +
                              (midPoint[Y] - cuttingLine[S][Y]) ** 2)

            # beta : midPoint와 원호의 중점 사이의 거리이다.
            beta = math.sqrt(cuttingLine[RAD] ** 2 - alpha ** 2)

            # uVect : 시점 -> 끝점 벡터이다.
            uVect = [cuttingLine[E][X] - cuttingLine[S][X], cuttingLine[E][Y] - cuttingLine[S][Y]]

            # vVect : uVect와 수직인 단위 벡터이다. 양쪽 방향으로 존재하므로 vVect1, vVect2 두개를 정의한다.
            vVect = [1, 0]

            if uVect[Y] is not 0:
                vVect[Y] = - uVect[X] / uVect[Y]
            else:
                vVect[Y] = 1
                vVect[X] = 0

            lamda1 = math.sqrt(1 / (1 + vVect[Y] ** 2))
            lamda2 = -lamda1

            vVect1 = [i * lamda1 for i in vVect]
            vVect2 = [i * lamda2 for i in vVect]

            # center1 : 첫번째 후보 원호중심
            center1 = [midPoint[X] + beta * vVect1[X],
                       midPoint[Y] + beta * vVect1[Y],
                       midPoint[Z]]

            # center2 : 두번째 후보 원호중심
            center2 = [midPoint[X] + beta * vVect2[X],
                       midPoint[Y] + beta * vVect2[Y],
                       midPoint[Z]]

            x = np.array([center1[X], center2[X]])
            y = np.array([center1[Y], center2[Y]])
            z = np.array([center1[Z], center2[Z]])

            # ax.plot(x, y, z, label='centerLine' + str(count+1))

            if beta is not 0:
                theta = np.arctan(alpha/beta)
            else:
                theta = np.pi/2

            c1ToS = [cuttingLine[S][X]-center1[X], cuttingLine[S][Y]-center1[Y]]
            c2ToS = [cuttingLine[S][X]-center2[X], cuttingLine[S][Y]-center2[Y]]
            xVect = [1,0]

            startR1 = np.arccos(np.dot(c1ToS,xVect)/(vectLenght(c1ToS)*vectLenght(xVect)))
            startR2 = -np.arccos(np.dot(c2ToS,xVect)/(vectLenght(c2ToS)*vectLenght(xVect)))

            sign = 0

            if cuttingLine[DIR] is CW:
                sign = -1
            else:
                sign = 1

            sVect = getVect(center1[X], center1[Y], cuttingLine[E][X], cuttingLine[E][Y])

            r = np.linspace(getAngle(sVect), getAngle(sVect)+sign*2*theta, 100)
            x = cuttingLine[RAD] * np.cos(r) + center1[X]
            y = cuttingLine[RAD] * np.sin(r) + center1[Y]
            z = r*0 + cuttingLine[S][Z]


            if vectLenght([midPoint[X]-x[-1], midPoint[Y]-y[-1]]) + vectLenght([midPoint[X]-x[0], midPoint[Y]-y[0]]) < 2*alpha+0.3:
                ax.plot(x, y, z, label='Arc ' + str(count+1))

            # x = x + 2*(midPoint[X]-x)
            # y = y + 2*(midPoint[Y]-y)
            #
            # if vectLenght([midPoint[X]-x[-1], midPoint[Y]-y[-1]]) + vectLenght([midPoint[X]-x[0], midPoint[Y]-y[0]]) < 2*alpha+1:
            #     ax.plot(x, y, z, label='circle1 ' + str(count+1))


            sVect = getVect(center2[X], center2[Y], cuttingLine[E][X], cuttingLine[E][Y])

            r = np.linspace(getAngle(sVect), getAngle(sVect)+sign*2*theta, 100)
            x = cuttingLine[RAD] * np.cos(r) + center2[X]
            y = cuttingLine[RAD] * np.sin(r) + center2[Y]
            z = r*0 + cuttingLine[S][Z]

            if vectLenght([midPoint[X]-x[-1], midPoint[Y]-y[-1]]) + vectLenght([midPoint[X]-x[0], midPoint[Y]-y[0]]) < 2*alpha+0.3:
                ax.plot(x, y, z, label='Arc ' + str(count+1))

            # x = x + 2*(midPoint[X]-x)
            # y = y + 2*(midPoint[Y]-y)
            #
            # if vectLenght([midPoint[X]-x[-1], midPoint[Y]-y[-1]]) + vectLenght([midPoint[X]-x[0], midPoint[Y]-y[0]]) < 2*alpha+1:
            #     ax.plot(x, y, z, label='circle1 ' + str(count+1))

            pass
        else:
            print('Crap! it seems object SHAPE label is not either LINE or ARC! : ' + str(cuttingLine[SHAPE]))


###########
#	실행 부분
###########

generateRandCuttingLines()
generateRandCuttingArc()
drawCuttingLines()

ax.legend()
plt.show()
