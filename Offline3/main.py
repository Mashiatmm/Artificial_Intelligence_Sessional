from cell import Cell
import numpy as np
# Take input from file

f = open("input.txt", "r")

n, m, k = f.readline().split(" ")
n = int(n)
m = int(m)
k = int(k)

def initialize(n, m, k):
    # initialize the cells
    cells = np.empty([n, m], dtype = object)
    for i in range(n):
        for j in range(m):
            cells[i][j] = Cell(n, m, k)
            if i == 0 or i == n-1 or j == 0 or j == m-1:
                if i-1 < 0 or j - 1 < 0:
                    cells[i][j].corner -= 1
                if i - 1 < 0:
                    cells[i][j].edge -= 1
                if i-1 < 0 or j + 1 > m-1:
                    cells[i][j].corner -= 1

                if j - 1 < 0:
                    cells[i][j].edge -= 1
                if j + 1 > m-1:
                    cells[i][j].edge -= 1

                if i+1 > n-1 or j - 1 < 0:
                    cells[i][j].corner -= 1
                if i + 1 > n-1:
                    cells[i][j].edge -= 1
                if i + 1 > n-1 or j + 1 > m-1:
                    cells[i][j].corner -= 1


    # deduct the obstacle edges
    for i in range(k):
        row, column = f.readline().split(" ")
        row = int(row)
        column = int(column)
        # set self probability to zero
        cells[row][column].prob = 0
        cells[row][column].obstacle = True
        # decrease edge of neighbours
        if column - 1 >= 0 :
            cells[row][column-1].edge -= 1
        if column + 1 < m :
            cells[row][column+1].edge -= 1
        # decrease corner of neighbours
        if row - 1 >= 0 :
            cells[row - 1][column].edge -= 1
            if column - 1 >= 0:
                cells[row-1][column-1].corner -= 1
            if column + 1 < m:
                cells[row - 1][column + 1].corner -= 1
        if row + 1 < n :
            cells[row + 1][column].edge -= 1
            if column - 1 >= 0:
                cells[row + 1][column - 1].corner -= 1
            if column + 1 < m:
                cells[row + 1][column + 1].corner -= 1
    return cells

def evidence(cells, rn, rm , evid):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if rn + i >= 0 and rn + i < n and rm + j >= 0 and rm + j < m:
                if cells[rn+i][rm+j].obstacle == False:
                    cells[rn+i][rm+j].prob = cells[rn+i][rm+j].prob*evid
                    cells[rn+i][rm+j].sensed = True

    not_evidence = 1 - evid

    for i in range(n):
        for j in range(m):
            if cells[i][j].sensed == True:
                cells[i][j].sensed = False
                continue
            if cells[i][j].obstacle == False and cells[i][j].sensed == False:
                cells[i][j].prob = cells[i][j].prob * not_evidence

    return cells

def normalize(cells, n, m):
    total = 0
    for i in range(n):
        for j in range(m):
            if cells[i][j].obstacle == False:
                total += cells[i][j].prob
    for i in range(n):
        for j in range(m):
            cells[i][j].prob = cells[i][j].prob / total

    return cells

def partial_belief(cells, n, m):
    cell_copy = np.empty([n, m], dtype = object)
    # making a copy of cells with probability 0
    for i in range(n):
        for j in range(m):
            cell_copy[i][j] = Cell(n, m, k)
            cell_copy[i][j].edge = cells[i][j].edge
            cell_copy[i][j].corner = cells[i][j].corner
            cell_copy[i][j].prob = 0
            cell_copy[i][j].obstacle = cells[i][j].obstacle


    # calculating partial belief
    for i in range(n):
        for j in range(m):
            if cells[i][j].obstacle == True:
                continue
            corner_weights = cells[i][j].prob * cells[i][j].get_corner_prob()
            edge_weights = cells[i][j].prob * cells[i][j].get_edge_prob()
            # print(i, j, cells[i][j].prob, cells[i][j].corner, cells[i][j].edge)
            # print(i, j, corner_weights, edge_weights)
            # add corner weight to itself
            cell_copy[i][j].prob += corner_weights
            # add partial beliefs to edges
            if i-1 >= 0:
                if cells[i-1][j].obstacle == False:
                    cell_copy[i-1][j].prob += edge_weights
                # add corner weights to corner edges
                if j-1 >= 0:
                    if cells[i-1][j-1].obstacle == False:
                        cell_copy[i-1][j-1].prob += corner_weights
                if j + 1 < m:
                    if cells[i-1][j + 1].obstacle == False:
                        cell_copy[i-1][j + 1].prob += corner_weights
            if i+1 < n:
                if cells[i+1][j].obstacle == False:
                    cell_copy[i+1][j].prob += edge_weights
                # add corner weights to corner edges
                if j - 1 >= 0:
                    if cells[i + 1][j - 1].obstacle == False:
                        cell_copy[i + 1][j - 1].prob += corner_weights
                if j + 1 < m:
                    if cells[i + 1][j + 1].obstacle == False:
                        cell_copy[i + 1][j + 1].prob += corner_weights
            if j-1 >= 0:
                if cells[i][j-1].obstacle == False:
                    cell_copy[i][j-1].prob += edge_weights
            if j+1 < m:
                if cells[i][j+1].obstacle == False:
                    cell_copy[i][j+1].prob += edge_weights
            # print("Print Cells : after setting partial beliefs of ", i, j)
            # for i in range(n):
            #     for j in range(m):
            #         print(format(cell_copy[i][j].prob, ".4f"), end=" ")
            #     print()
            # print()

    # set the partial beliefs
    return cell_copy


def get_max_indices(cells):
    max = 0
    x, y = -1, -1
    for i in range(n):
        for j in range(m):
            if cells[i][j].prob > max:
                max = cells[i][j].prob
                x = i
                y = j
    return x, y


def print_cells(cells, n, m):
    for i in range(n):
        for j in range(m):
            print(format(cells[i][j].prob, ".4f"), end=" ")
        print()
    print()



cells = initialize(n, m, k)

print("Initial Cells")
print_cells(cells, n, m)



for x in f:
    # read line by line
    if x.startswith("R"):
        R, rn, rm, sense = x.split(" ")
        rn = int(rn)
        rm = int(rm)
        sense = int(sense)

        cells = partial_belief(cells, n, m)

        evid = 0.85
        if sense == 0:
            evid = 0.15
        # multiply by evidence
        cells = evidence(cells, rn, rm, evid)

        cells = normalize(cells, n, m)
        print("Print Cells")
        print_cells(cells, n, m)
    elif x.startswith("C"):
        x, y = get_max_indices(cells)
        print("Probable Position")
        print(x, y)

    elif x.startswith("Q"):
        print("Bye Casper")
        f.close()
        exit()

