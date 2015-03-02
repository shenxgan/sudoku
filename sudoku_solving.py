#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
作者：古怪
时间：2015-03-01
地址：http://www.qjwgg.com
'''

sudoku_candidate = [[]] * 81  #候选数

def check_candidate_unique(sudoku):  #检测候选值是否唯一
    '''
    1. 分别以行/列/3*3的小矩阵进行单位进行遍历，检测每一个单元格的候选数中的其中一个是否在此行/列/3*3的小矩阵其余单元格的候选数中唯一
    2. 若此单元格的其中一个候选数在此行/列/3*3的小矩阵的其余单元格的候选数中不存在，则此候选数即可确定为此单元格的值
    '''
    for i in range(len(sudoku)):  #以行为单位进行遍历
        row = i/9
        if len(sudoku_candidate[i]) != 1:  #if sudoku[i] != 0:
            for j in range(0,9):  #遍历行
                for value in sudoku_candidate[row*9 + j]:  #遍历元素的候选值
                    flag = False
                    for _j in range(0,9):  #在其余8个元素中进行比较
                        if _j != j:
                            if value in sudoku_candidate[row*9 + _j]:
                                flag = True  #若在其他候选数中已存在，则记标记flag为True
                                break
                    if flag is False:  #在其他候选数中不存在，则更新元素的值和其候选值
                        sudoku[row*9 + j] = value
                        candidate = [value]
                        sudoku_candidate[row*9 + j] = candidate[:]
                        break

    for col in range(0,9):  #以列为单位进行遍历
        for row in range(0,9):
            i = row*9 + col  #元素下标
            if sudoku[i] != 0:
                for j in range(0,9):  #列中9个元素
                    for value in sudoku_candidate[j*9 + col]:  #遍历元素的候选值
                        flag = False
                        for _j in range(0,9):  #在其余8个元素中进行比较
                            if _j != j:
                                if value in sudoku_candidate[_j*9 + col]:
                                    flag = True
                                    break
                        if flag is False:  #在其他候选数中不存在，则更新元素的值和其候选值
                            sudoku[j*9 + col] = value
                            candidate = [value]
                            sudoku_candidate[j*9 + col] = candidate[:]
                            break

    for i in range(len(sudoku)):  #以宫格为单位进行遍历
        row = i/9
        col = i%9
        if sudoku[i] != 0:
            for k in range(0,3):
                for t in range(0,3):
                    for value in sudoku_candidate[(row/3*3+k)*9 + col/3*3+t]:  #遍历元素的候选值
                        flag = 'False'
                        for _k in range(0,3):  #在其余8个元素中进行比较
                            for _t in range(0,3):
                                if _k != k or _t != t:
                                    if value in sudoku_candidate[(row/3*3+_k)*9 + col/3*3+_t]:
                                        flag = 'True'
                                        break
                            if flag == 'True':
                                break
                        if flag == 'False':
                            sudoku[(row/3*3+k)*9 + col/3*3+t] = value
                            candidate = [value]
                            sudoku_candidate[(row/3*3+k)*9 + col/3*3+t] = candidate[:]
                            break

def init_sudoku_candidate(sudoku):  #初始化候选值，0的候选值为candidate，非0的候选值为其本身（列表形式）
    '''
    初始化数独的候选值
    1. 单元格值为0的候选数为[1,2,3,4,5,6,7,8,9]
    2. 值为非0的候选数为其值本身（列表形式）
    '''
    for i in range(len(sudoku)):
        if sudoku[i] == 0:
            candidate = [1,2,3,4,5,6,7,8,9]
        else:
            candidate = [sudoku[i]]
        sudoku_candidate[i] = candidate[:]

def update_sudoku_row(sudoku):  #以行进行更行元素值和其候选值
    for i in range(len(sudoku)):
        row = i/9
        if sudoku[i] != 0:
            for j in range(0,9):  #遍历行
                if sudoku[i] in sudoku_candidate[row*9 + j] and len(sudoku_candidate[row*9 + j]) > 1:
                    sudoku_candidate[row*9 + j].remove(sudoku[i])  #在此行中从候选数中删除已经存在的值
        if len(sudoku_candidate[i]) == 1:  #候选数仅有1个的时候，即可认定此候选值即为其值
            sudoku[i] = sudoku_candidate[i][0]

def update_sudoku_col(sudoku):  #以列进行更行元素值和其候选值
    for col in range(0,9):
        for row in range(0,9):
            i = row*9 + col  #元素下标
            if sudoku[i] != 0:
                for j in range(0,9):  #遍历此列中9个元素
                    if sudoku[i] in sudoku_candidate[j*9 + col] and len(sudoku_candidate[j*9 + col]) > 1:
                        sudoku_candidate[j*9 + col].remove(sudoku[i])
            if len(sudoku_candidate[i]) == 1:
                sudoku[i] = sudoku_candidate[i][0]

def update_sudoku_grid(sudoku):  #以3*3宫格进行更行元素值和其候选值
    for i in range(len(sudoku)):
        row = i/9
        col = i%9
        if sudoku[i] != 0:
            for k in range(0,3):  #遍历此宫格中的9个元素
                for t in range(0,3):
                    if sudoku[i] in sudoku_candidate[(row/3*3+k)*9 + col/3*3+t] and len(sudoku_candidate[(row/3*3+k)*9 + col/3*3+t]) > 1:
                        sudoku_candidate[(row/3*3+k)*9 + col/3*3+t].remove(sudoku[i])
        if len(sudoku_candidate[i]) == 1:
            sudoku[i] = sudoku_candidate[i][0]

def out_sudoku(sudoku):
    for i in range(len(sudoku)):
        print sudoku[i],
        if (i+1)%9 == 0:
            print
    print '-'*50

def sudoku_solving(sudoku):
    '''
    根据数独的两个特性进行求解
    1. 单元格的候选值只有一个时，其值即为此候选值
    2. 单元格的其中一个候选值在此单元格所在的行/列/3*3的小矩阵中唯一时，此候选值即为此单元格的值
    '''
    init_sudoku_candidate(sudoku)
    i = 0
    ret = 0
    while True:  #直到已经完成求解才退出
        update_sudoku_row(sudoku)
        update_sudoku_col(sudoku)
        update_sudoku_grid(sudoku)
        check_candidate_unique(sudoku)
        if 0 not in sudoku:
            ret = 0
            break
        i += 1
        if i >= 5:  #最多进行5此循环
            ret = -1
            break
    # print i,'+'*10
    return ret

if __name__ == '__main__':
    sudoku = [
        0, 9, 0, 1, 0, 0, 3, 7, 8,
        0, 0, 0, 7, 0, 9, 0, 0, 0,
        0, 1, 0, 4, 0, 8, 0, 0, 6,
        0, 0, 0, 2, 0, 0, 6, 5, 9,
        0, 0, 0, 0, 4, 3, 0, 0, 0,
        0, 5, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 2, 3, 5, 1, 7, 0, 0,
        0, 6, 0, 8, 9, 0, 5, 0, 2,
        0, 0, 0, 0, 0, 2, 8, 0, 0
    ]

    # sudoku = [
        # 0,0,0,0,0,0,8,0,0,
        # 4,0,0,2,0,8,0,5,1,
        # 0,8,3,9,0,0,0,0,7,
        # 0,4,0,5,0,0,0,8,2,
        # 0,0,5,0,0,0,4,0,0,
        # 8,7,0,0,0,9,0,3,0,
        # 2,0,0,0,0,7,1,6,0,
        # 3,6,0,1,0,5,0,0,4,
        # 0,0,4,0,0,0,0,0,0
    # ]

    ret = sudoku_solving(sudoku)
    out_sudoku(sudoku)
