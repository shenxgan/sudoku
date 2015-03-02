#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
作者：古怪
时间：2015-03-01
地址：http://www.qjwgg.com
'''

import random

from sudoku_solving import sudoku_solving


def get_random_num(sudoku,index):  # 从候选数中随机获取
    '''
    index 为单元格下标
    1. 首先根据此单元格所在的行、列和3*3的小矩阵，对此单元格的候选数进行更新
    2. 从更新后的候选数中随机选取一个作为此单元格的值
    '''
    candidate = [1,2,3,4,5,6,7,8,9]

    row = index/9
    col = index%9

    # 所在小矩阵第一个元素的坐标
    grid_x = row/3*3
    grid_y = col/3*3

    j = 0
    while j < col:
        if sudoku[row*9 + j] in candidate:
            candidate.remove(sudoku[row*9 + j])
        j += 1

    i = 0
    while i < row:
        if sudoku[i*9 + col] in candidate:
            candidate.remove(sudoku[i*9 + col])
        i += 1

    for _i in range(0,3):
        for _j in range(0,3):
            if sudoku[(grid_x+_i)*9 + grid_y+_j] in candidate:
                candidate.remove(sudoku[(grid_x+_i)*9 + grid_y+_j])

    if len(candidate) == 0: # 候选数都排除干净了，表示此次生成数独终盘失败，重新来过
        random_num = -1
    else:
        random_num = random.choice(candidate)  # 从候选数中随机获取一个作为此单元格的值

    return random_num

def sudoku_generate_backtracking(): # 生成数独终盘，顺序进行回溯，从下标0开始
    '''
    1. 初始化数独为长度为 81 ，初始值均为 0 的 list 类型
    2. 遍历整个数独，随机（从其候选值中进行随机）获取每个单元格的值
    3. 若能走到最后，则表示生成数独终盘成功，否则重新进行第2步直至成功
    '''
    sudoku = [0] * 81
    # for i in range(0,81):
    i = 0
    while i < 81:
        random_num = get_random_num(sudoku,i)  # 随机获取单元格的值，随机是在单元格此前候选数中的随机一个
        if random_num == -1:  # 随机值为 -1 表示生成失败，则重新进行生成
            sudoku = [0] * 81
            i = 0
        else:
            sudoku[i] = random_num
            i += 1
    return sudoku


def sudoku_puzzle_dibble(sudoku):  # “挖洞”生成一道数独
    '''
    基于挖洞思想的一个简单的实现
    1. 一次性挖取n个洞（n根据难度进行设定），表现即为随机将数独中的n个单元格的值置为0
    2. 挖取完毕后，进行求解，来判定挖取后的得到的数独难题的解是否唯一。
    3. 若能求解，则其解唯一，否则重新进行步骤1 2，直至能够求解成功，生成数独难题
    '''
    while True:
        sudoku_dibble = sudoku[:]
        i = 0
        while i < 50:  # 挖 N 个洞
            random_index = random.choice(range(0,81))  # 随机挖取的单元格下标
            if sudoku_dibble[random_index] != 0:
                sudoku_dibble[random_index] = 0
            else:  # 已经被挖，回退此次循环
                i -= 1
            i += 1
        sudoku_tmp = sudoku_dibble[:]
        ret = sudoku_solving(sudoku_tmp)  # 对生成的数独难题进行求解，若有解则表示解唯一，则挖洞成功，否则失败
        if ret != 0:  # 失败则重新进行挖洞
            continue
        if sudoku_tmp == sudoku:  # 成功则退出
            out_sudoku(sudoku)
            out_sudoku(sudoku_dibble)
            break

def out_sudoku(sudoku):
    for i in range(len(sudoku)):
        # print str(sudoku[i])+',',
        print sudoku[i],

        if (i+1)%9 == 0:
            print
    print '-'*50

if __name__ == '__main__':
    sudoku = sudoku_generate_backtracking()
    sudoku_puzzle_dibble(sudoku)
