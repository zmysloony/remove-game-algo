from random import randrange

from classes import *
import time


def gen_random(size, min_num, max_num):
    r = []
    for i in range(size):
        r.append(randrange(min_num, max_num, 1))
    return r


def main():
    z = GameArray([-1, -2, -1, 1, 2, 3, 0, 3, 3, 0])
    z.preprocess(0)
    print(z.calc_max_score())
    time_sum = 0

    for t in range(20000):
        randomgamearray = GameArray(gen_random(10, 1, 5))
        start_time = time.perf_counter()
        randomgamearray.preprocess(0)
        randomgamearray.calc_max_score()
        time_sum += time.perf_counter() - start_time
    print("time sum:", time_sum, "s")
    return 0


if __name__ == "__main__":
    main()
