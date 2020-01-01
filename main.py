from copy import deepcopy
from random import randrange

from classes import *
import time


def gen_random(size, min, max):
    r = []
    for i in range(size):
        r.append(randrange(min, max, 1))
    return r


def main():
    #TODO cleanup shit
    # i = GameArray([-15,	-28, -28, -29, -29,	-69,	-2,	-33,	0,	21,	24,	96,	12,	12, 13, 14, 14,55])
    z = GameArray([-1, -2, -1, 1, 2, 3, 0, 3, 3, 0])
    z= GameArray([1, 1, 3, 1, 1, 1, 3, 4, 4, 3])
    #i = GameArray([54,	41,	0	,67	,36,	69,	90	,93	,165	,81,	124])
    # print(i.nums)
    z.preprocess(0)
    # print(i.nums)
    z.print()
    print(z.calc_max_score())
    # print("\n\n", i.nums,"\n", i.gains)
    # print(algo_one(game_array=i))
    #a = find_max_sum(game_array=i)

    # print (sum)
    time_sum = 0
    wrong = 0
    for t in range(20000):
        kek = gen_random(10,1,5)
        # print("kek",kek)
        randomgamearray = GameArray(kek)
        # print(randomgamearray.nums)
        startTime = time.perf_counter()
        randomgamearray.preprocess(0)
        # randomgamearray.print()
        randomgamearray.calc_max_score()
        time_sum += time.perf_counter() - startTime
    print("time sum:", time_sum, "s")
    return 0


if __name__ == "__main__":
    main()
