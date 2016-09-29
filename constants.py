# -*- coding: utf-8 -*-
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


###########
#	상수 설정
###########


#
### 그래픽 관련 설정
#

# 랜덤 툴패스 갯수 기본설정
CUTTING_LINE_COUNT = 5
CUTTING_ARC_COUNT = 5

# 윈호보간 나누는 해상도
ARC_RESOLUTION = 100

# 랜덤 툴패스 크기
MAX_LENGTH = 100
MAX_ARC = 50



#
### 지네틱 알고리즘 관련 설정
#

# 최초 유전자 풀 크기
POPULATION = 10

# 한 Generation 에서 부모세대의 생식 횟수( 한번의 생식에서 2개 자녀 생성)
BIRTHRATE = 10

# Generation 횟수
GENERATION = 2000

# 돌연변이 확률
MUTATION = 0.1




############
#   주의! 변경금지
############

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
MOVE = 2

CW = 0
CCW = 1

RESULT = 0
INITIAL_LENGTH = 1
FINAL_LENGTH = 2