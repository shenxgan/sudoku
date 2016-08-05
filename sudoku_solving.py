#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict


sudoku_candidate = [[]] * 81  # 候选数
solution_cnts = defaultdict(int)


def check_candidate_unique(sudoku):  # 检测候选值是否唯一
    '''
    1. 分别以行/列/3*3的小矩阵为单位进行遍历，检测每一个单元格的候选数中的其中一个是否在此行/列/3*3的小矩阵其余单元格的候选数中唯一
    2. 若此单元格的其中一个候选数在此行/列/3*3的小矩阵的其余单元格的候选数中不存在，则此候选数即可确定为此单元格的值
    '''
    for i in range(len(sudoku)):  # 以行为单位进行遍历
        row = i / 9
        if len(sudoku_candidate[i]) != 1:  # if sudoku[i] != 0:
            for j in range(0, 9):  # 遍历行
                for value in sudoku_candidate[row * 9 + j]:  # 遍历元素的候选值
                    flag = False
                    for _j in range(0, 9):  # 在其余8个元素中进行比较
                        if _j != j:
                            if value in sudoku_candidate[row * 9 + _j]:
                                flag = True  # 若在其他候选数中已存在，则记标记flag为True
                                break
                    if flag is False:  # 在其他候选数中不存在，则更新元素的值和其候选值
                        sudoku[row * 9 + j] = value
                        candidate = [value]
                        sudoku_candidate[row * 9 + j] = candidate[:]
                        break

    for col in range(0, 9):  # 以列为单位进行遍历
        for row in range(0, 9):
            i = row * 9 + col  # 元素下标
            if sudoku[i] != 0:
                for j in range(0, 9):  # 列中9个元素
                    for value in sudoku_candidate[j * 9 + col]:  # 遍历元素的候选值
                        flag = False
                        for _j in range(0, 9):  # 在其余8个元素中进行比较
                            if _j != j:
                                if value in sudoku_candidate[_j * 9 + col]:
                                    flag = True
                                    break
                        if flag is False:  # 在其他候选数中不存在，则更新元素的值和其候选值
                            sudoku[j * 9 + col] = value
                            candidate = [value]
                            sudoku_candidate[j * 9 + col] = candidate[:]
                            break

    for i in range(len(sudoku)):  # 以宫格为单位进行遍历
        row = i / 9
        col = i % 9
        if sudoku[i] != 0:
            for k in range(0, 3):
                for t in range(0, 3):
                    x, y = (row / 3 * 3 + k) * 9, col / 3 * 3 + t
                    loc = x + y
                    for value in sudoku_candidate[loc]:  # 遍历元素的候选值
                        flag = False
                        for _k in range(0, 3):  # 在其余8个元素中进行比较
                            for _t in range(0, 3):
                                if _k != k or _t != t:
                                    if value in sudoku_candidate[(row / 3 * 3 + _k) * 9 + col / 3 * 3 + _t]:
                                        flag = True
                                        break
                            if flag:
                                break
                        if not flag:
                            sudoku[loc] = value
                            candidate = [value]
                            sudoku_candidate[loc] = candidate[:]
                            break


def init_sudoku_candidate(sudoku):
    '''
    初始化数独的候选值
    1. 单元格值为0的候选数为[1,2,3,4,5,6,7,8,9]
    2. 值为非0的候选数为其值本身（列表形式）
    '''
    for i in range(len(sudoku)):
        if sudoku[i] == 0:
            # candidate = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            candidate = range(1, 10)
        else:
            candidate = [sudoku[i]]
        sudoku_candidate[i] = candidate[:]


def update_sudoku_row(sudoku):  # 以行进行更行元素值和其候选值
    for i in range(len(sudoku)):
        row = i / 9
        row_list = []
        if sudoku[i] != 0:
            for j in range(0, 9):  # 遍历行
                loc = row * 9 + j
                if sudoku[i] in sudoku_candidate[loc] and len(sudoku_candidate[loc]) > 1:
                    sudoku_candidate[loc].remove(sudoku[i])  # 在此行中从候选数中删除已经存在的值
                row_list.append(sudoku[loc])
        if len(sudoku_candidate[i]) == 1:  # 候选数仅有1个的时候，即可认定此候选值即为其值
            sudoku[i] = sudoku_candidate[i][0]
            if row_list.count(sudoku[i]) > 1:
                raise Exception('row %d error!' % row)


def update_sudoku_col(sudoku):  # 以列进行更行元素值和其候选值
    for col in range(0, 9):
        for row in range(0, 9):
            i = row * 9 + col  # 元素下标
            col_list = []
            if sudoku[i] != 0:
                for j in range(0, 9):  # 遍历此列中9个元素
                    loc = j * 9 + col
                    if sudoku[i] in sudoku_candidate[loc] and len(sudoku_candidate[loc]) > 1:
                        sudoku_candidate[loc].remove(sudoku[i])
                    col_list.append(sudoku[loc])
            if len(sudoku_candidate[i]) == 1:
                sudoku[i] = sudoku_candidate[i][0]
                if col_list.count(sudoku[i]) > 1:
                    raise Exception('col %d error!' % col)


def update_sudoku_grid(sudoku):  # 以3*3宫格进行更行元素值和其候选值
    for i in range(len(sudoku)):
        row = i / 9
        col = i % 9
        grid_list = []
        if sudoku[i] != 0:
            for k in range(0, 3):  # 遍历此宫格中的9个元素
                for t in range(0, 3):
                    x, y = (row / 3 * 3 + k) * 9, col / 3 * 3 + t
                    loc = x + y
                    if sudoku[i] in sudoku_candidate[loc] and len(sudoku_candidate[loc]) > 1:
                        sudoku_candidate[loc].remove(sudoku[i])
                    grid_list.append(sudoku[loc])
        if len(sudoku_candidate[i]) == 1:
            sudoku[i] = sudoku_candidate[i][0]
            if grid_list.count(sudoku[i]) > 1:
                raise Exception('grid (row: %d, col: %d) error!' % (row, col))


def out_sudoku(sudoku):
    for i in range(len(sudoku)):
        print sudoku[i],
        if (i + 1) % 9 == 0:
            print
        elif (i + 1) % 3 == 0:
            print '|',
        if (i + 1) % 27 == 0 and (i + 1) % 81 != 0:
            print '------+-------+------'


def out_candidate(sudoku_candidate):
    sudoku = [''.join(map(str, s)) for s in sudoku_candidate]
    for i in range(len(sudoku)):
        print '%9s' % sudoku[i],
        if (i + 1) % 9 == 0:
            print
        elif (i + 1) % 3 == 0:
            print '|',
        if (i + 1) % 27 == 0 and (i + 1) % 81 != 0:
            print '------------------------------+-------------------------------+------------------------------'


def sudoku_solving(sudoku, flag=0):
    '''
    根据数独的两个特性进行求解
    1. 单元格的候选值只有一个时，其值即为此候选值
    2. 单元格的其中一个候选值在此单元格所在的行/列/3*3的小矩阵中唯一时，此候选值即为此单元格的值
    '''
    ret = 0
    init_sudoku_candidate(sudoku)
    while True:  # 直到已经完成求解才退出
        sudoku_candidate_old = sudoku_candidate[::]
        try:
            update_sudoku_row(sudoku)
            check_candidate_unique(sudoku)

            update_sudoku_col(sudoku)
            check_candidate_unique(sudoku)

            update_sudoku_grid(sudoku)
            check_candidate_unique(sudoku)
        # except Exception, e:
        except:
            ret = -2
            break
        if 0 not in sudoku:
            # print 'success!!!'
            # out_sudoku(sudoku)
            solution_cnts[flag] += 1
            ret = solution_cnts[flag]
            break
        if sudoku_candidate == sudoku_candidate_old:
            # 前后两次候选数没有变化，表示已经处理到最简了
            ret = -1
            break

    if ret == -1:
        first0 = sudoku.index(0)
        candidates = sudoku_candidate[first0]
        # 对候选值进行遍历，猜测数独解
        for v in candidates:
            # print v, candidates
            sudoku2 = sudoku[::]
            sudoku2[first0] = v
            sudoku_candidate[first0] = [v]
            ret = sudoku_solving(sudoku2, flag)
            if solution_cnts[flag] > 2:
                # 多个解
                break

    # 唯一解
    if solution_cnts[flag] == 1:
        ret = 0
    return ret


if __name__ == '__main__':
    sudoku1 = [
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

    sudoku2 = [
        0, 0, 0, 0, 0, 0, 8, 0, 0,
        4, 0, 0, 2, 0, 8, 0, 5, 1,
        0, 8, 3, 9, 0, 0, 0, 0, 7,
        0, 4, 0, 5, 0, 0, 0, 8, 2,
        0, 0, 5, 0, 0, 0, 4, 0, 0,
        8, 7, 0, 0, 0, 9, 0, 3, 0,
        2, 0, 0, 0, 0, 7, 1, 6, 0,
        3, 6, 0, 1, 0, 5, 0, 0, 4,
        0, 0, 4, 0, 0, 0, 0, 0, 0
    ]

    sudoku3 = [
        0, 8, 2, 0, 9, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 5,
        0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 3, 2, 0,
        7, 0, 0, 5, 0, 6, 0, 0, 0,
        0, 0, 0, 7, 0, 0, 0, 0, 0,
        0, 3, 0, 9, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 2, 0, 0, 8, 0,
        5, 0, 0, 0, 0, 0, 0, 0, 6
    ]

    sudoku4 = [
        7, 2, 3, 1, 9, 8, 6, 4, 5,
        5, 4, 1, 2, 6, 3, 9, 7, 8,
        0, 0, 8, 0, 5, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 4,
        0, 7, 0, 8, 0, 0, 0, 3, 0,
        4, 0, 0, 0, 3, 5, 0, 0, 7,
        1, 0, 0, 0, 0, 0, 0, 0, 2,
        0, 0, 0, 0, 0, 4, 0, 1, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0
    ]
    sudoku5 = [1, 4, 7, 9, 3, 8, 2, 5, 0, 2, 5, 9, 6, 1, 7, 4, 8, 3, 3, 8, 6, 2, 0, 5, 9, 7, 1, 6, 7, 5, 8, 9, 4, 1, 3, 2, 9, 3, 4, 7, 2, 1, 5, 6, 8, 8, 1, 2, 3, 5, 6, 7, 9, 4, 4, 9, 3, 5, 6, 2, 8, 1, 7, 7, 6, 1, 4, 8, 9, 3, 2, 5, 5, 2, 8, 1, 7, 3, 6, 4, 9]
    sudoku6 = [0, 0, 0, 0, 1, 0, 0, 0, 9, 0, 8, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 9, 7, 4, 0, 0, 2, 0, 4, 0, 0, 0, 5, 6, 0, 0, 0, 0, 0, 5, 1, 0, 4, 0, 0, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 5, 0]
    sudoku7 = [0, 0, 0, 0, 0, 4, 6, 0, 0, 6, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 3, 6, 1, 0, 4, 5, 0, 0, 0, 0, 9, 0, 0, 6, 4, 7, 0, 4, 0, 3, 0, 0, 0, 9, 3, 0, 0, 5, 0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 2, 0, 6, 1, 0, 4, 0, 0, 4, 0, 0, 8, 5, 0, 9, 1, 0]
    sudoku8 = [4, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 9, 0, 5, 0, 3, 2, 9, 0, 0, 7, 0, 0, 0, 7, 5, 0, 0, 0, 0, 0, 0, 0, 6, 8, 4, 0, 0, 0, 0, 0, 8, 2, 0, 7, 3, 5, 1, 0, 0, 9, 0, 4, 0, 0, 1, 0, 3, 8, 0, 0, 0, 1, 0, 7, 0, 0, 0, 6, 0, 0, 8, 7, 0, 0, 0]
    sudoku9 = [0, 0, 6, 7, 0, 5, 0, 0, 0, 0, 5, 2, 8, 0, 0, 0, 1, 0, 7, 4, 3, 1, 6, 2, 5, 8, 9, 3, 0, 0, 9, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 9, 0, 0, 0, 6, 9, 0, 0, 0, 0, 0, 5, 0, 7, 0, 0, 1, 0, 8, 0, 3, 0, 3, 0, 0, 0, 8, 2, 0, 0, 0, 9, 8, 0, 7, 0, 0, 0, 0]
    sudoku9 = [1, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 0, 0, 0, 4, 0, 0, 0, 8, 4, 9, 0, 0, 3, 0, 0, 1, 7, 0, 0, 0, 4, 0, 2, 9, 8, 0, 0, 0, 0, 0, 0, 5, 4, 7, 0, 0, 4, 7, 0, 0, 0, 0, 6, 4, 7, 3, 0, 2, 5, 0, 0, 9, 9, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 6, 0, 0, 8, 4, 7, 0]

    sudoku = sudoku9
    out_sudoku(sudoku)
    ret = sudoku_solving(sudoku)
    print ret
