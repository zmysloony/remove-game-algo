from copy import deepcopy

from classes import *
import time

def algo_one(game_array):
    temp = deepcopy(game_array)
    res = 0
    while temp.left != 0:
        res += temp.remove_num(temp.get_max_gain())
        print("\n\n", temp.nums, "\n", temp.gains)
    return res


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
        ret.append(1)
    return ret


def main():
    #TODO cleanup shit
    i = GameArray([-15,	-28,	-69,	-2,	-33,	0,	21,	24,	96,	12,	55])
    #i = GameArray([54,	41,	0	,67	,36,	69,	90	,93	,165	,81,	124])
    DELETEmin = min(i.nums)
    # print(i.nums)
    i.preprocess(1)
    i.calculate_gains()
    # print("\n\n", i.nums,"\n", i.gains)
    # print(algo_one(game_array=i))
    a = find_max_sum(game_array=i)
    sum = 0

    for z in range(len(i.nums)):
        sum += (DELETEmin+i.nums[z])*a[z]
    # print (sum)
    #TODO make random data
    for t in range(100):

        startTime = time.perf_counter()
        stopTime = time.perf_counter()
        print("algo1 time", stopTime-startTime)

    return 0


if __name__ == "__main__":
    main()