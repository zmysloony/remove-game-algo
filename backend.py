from copy import deepcopy
from random import randrange

from classes import *
import time


def find_max_sum(game_array):
    arr = game_array.nums
    minfound = min(arr)
    for i in range(len(arr)):
        arr[i] -= minfound
    ret = []
    incl = 0
    excl = 0
    last = True
    for i in range(len(arr)):
        # Current max excluding i (No ternary in
        # Python)
        new_excl = excl if excl > incl else incl
        if (excl > incl and last is True and i is not len(arr)-1) or (last is False):
            ret.append(0)
            last = True
        else:
            ret.append(1)
            last = False

        incl = excl + arr[i]
        excl = new_excl

        # return max of incl and excl
    # if excl > incl and last is True or last is False:
    #     ret.append(0)
    #     last = True
    # else:
    #     ret.append(1)
    #     last = False
    if excl <= incl:
        ret[len(arr)-1] = 0
        ret.append(1)
    else:
        ret.append(0)
    ret.pop(0)
    return ret


def find_max_sum2(game_array):
    arr = game_array.nums
    minfound = min(arr)
    for i in range(len(arr)):
        arr[i] -= minfound-1
    incl = 0
    excl = 0
    last = False
    howmany = 0
    retarray = []
    for i in arr:
        # Current max excluding i (No ternary in
        # Python)
        new_excl = excl if excl >= incl else incl
        if incl >= excl and not last:
            howmany += 1
            retarray.append(1)
            last = True
        elif excl > incl:
            retarray.append(0)
            last = False
        else:
            retarray.append(0)
            last = False
        # Current max including i
        incl = excl + i
        excl = new_excl
        #  CO SIE DZIEJE DLA TYCH SAMYCH BILANSOW USUNIECA!!!!!!!!!!!!!!
        # unprocessed: [-1, -2, -1, 1, 2, 3, 0, 3, 3, 0]
        # radomgamearray
        # preprocessed: [-2, -2, 0, 1, 2, 9]
        # randomgamearray2
        # preprocessed: [-2, -2, 0, 1, 2, 9]
        # [14, 2]
        # robber: 10
        # algo1: 7
    print(retarray)
        # return max of incl and excl
    return [(excl if excl > incl else incl), howmany]

def gen_random(size, min, max):
    r = []
    for i in range(size):
        r.append(randrange(min, max, 1))
    return r


def main():
    #TODO cleanup shit
    i = GameArray([-15,	-28, -28, -29,	-69,	-2,	-33,	0,	21,	24,	96,	12,	12, 13, 14, 14,55])
    #i = GameArray([54,	41,	0	,67	,36,	69,	90	,93	,165	,81,	124])
    DELETEmin = min(i.nums)
    # print(i.nums)
    i.preprocess(0)
    print(i.nums)
    i.print()
    print(i.calc_max_score())
    # print("\n\n", i.nums,"\n", i.gains)
    # print(algo_one(game_array=i))
    #a = find_max_sum(game_array=i)

    # print (sum)
    time_sum = 0
    wrong = 0
    # for t in range(100):
    #     randomarray = gen_random(10,-2,5)
    #     # randomarray = [-1, 4, -2, 0, 3, -2, 4, 3, -2, 4]
    #
    #     print("unprocessed: ", randomarray)
    #     randomgamearray = GameArray(randomarray)
    #     randomgamearray2 = GameArray(copy(randomarray))
    #     startTime = time.perf_counter()
    #     randomgamearray.preprocess(0)
    #     randomgamearray.calculate_gains()
    #
    #     DELETEmin = min(randomgamearray.nums)
    #     print("radomgamearray preprocessed: ", randomgamearray.nums)
    #     randomgamearray2.preprocess(0)
    #     randomgamearray2.calculate_gains()
    #     result = find_max_sum2(randomgamearray)
    #     sum, how = result
    #     sum = sum + (DELETEmin-1)*how
    #     print("randomgamearray2 preprocessed: ", randomgamearray2.nums)
    #     sumalgo1 = algo_one(randomgamearray2)
    #     stopTime = time.perf_counter()
    #     print(result, "\n", "robber: ", sum, "algo1: ", sumalgo1, "\n")
    #     time_sum += stopTime-startTime
    #     if sum != sumalgo1:
    #         wrong += 1
    # print(time_sum)
    # print("wrong: ", wrong)
    return 0


if __name__ == "__main__":
    main()