from random import randrange

from classes import *
import argparse
import sys
import time
import matplotlib.pyplot as plot


def gen_random(size, min_num, max_num):
    # return [-3, -2, -2, -1, -1, -1, 0, 1, 2, 3]
    # return [-3, -4, -4, 0, 1, 4, 3, 16, 10, 6, 7]
    # return   [-3, -6, -4, 0, 2, 2, 15]
    # return [-3, -2, -1, 0, 1, 2, 3, 4, 20, 24, 7, 8, 9]

    r = []
    if evil_mode:
        z = min_num
        continue_chance = 40
        for i in range(size):
            r.append(z)
            if randrange(0, 100, 1) <= continue_chance: # don't increase the number (makes duplicates)
                z += 1
        # print(r)
        return r

    for i in range(size):
        r.append(randrange(min_num, max_num, 1))
    return r


def mode_one():    # parse lines into number arrays
    for line in sys.stdin:
        line = line.replace(',', '')
        strings = line.split()
        nums = []
        try:
            for st in strings:
                nums.append(int(st))
        except ValueError:
            print("Incorrect data (check for non-integers).")
            continue
        ga = GameArray(nums)
        start_time = time.perf_counter()
        ga.preprocess(0)
        s = ga.calc_max_score()
        t = time.perf_counter() - start_time
        if verbose_mode:
            print(nums)
            print("Max score:", s)
        else:
            print(s)
        if timer_mode:
            print("time sum:", t, "s")


def mode_two(l, n, min_num, max_num):
    if timer_mode:
        t = 0
        for i in range(n):
            rarray = GameArray(gen_random(l, min_num, max_num))
            start_time = time.perf_counter()
            rarray.preprocess(0)
            s = rarray.calc_max_score()
            t += time.perf_counter() - start_time

            if verbose_mode:
                print(rarray.nums)
                print("Max score:", s)
            else:
                print(s)
        if timer_mode:
            print("time sum:", t, "s")
    else:
        for i in range(n):
            rarray = GameArray(gen_random(l, min_num, max_num))
            rarray.preprocess(0)
            s = rarray.calc_max_score()
            if verbose_mode:
                print(rarray.nums)
                print("Max score:", s)
            else:
                print(s)


# l - starting list length, l_step - increments by that amount with each step, r - repeats for the same step
def mode_three(l, l_step, r, n, min_num, max_num, e, do_plot=True):
    times = []
    sizes = []
    for i in range(n):
        size = (l + i*l_step)*(e**i)
        t = 0
        for j in range(r):
            ga = GameArray(gen_random(size, min_num, max_num))
            start_time = time.perf_counter()
            ga.preprocess(0)
            ga.calc_max_score()
            t += time.perf_counter() - start_time
        print("Length:", size, "Time:", t/r, "s")
        sizes.append(size)
        times.append(t/r)
    if do_plot:
        plot.plot(sizes, times, label=str(min_num)+" to "+str(max_num))
        plot.xlabel("list size")
        plot.ylabel("time [s]")
        plot.legend()
        plot.show()
    return times, sizes


# mode three, but for selected min_num and max_num pairs
def mode_four(l, l_step, r, n, e, pairs):
    for pair in pairs:
        min_num, max_num = pair
        times, sizes = mode_three(l, l_step, r, n, min_num, max_num, e, do_plot=False)
        plot.plot(sizes, times, label=str(min_num)+" to "+str(max_num))

    plot.xlabel("list size")
    plot.ylabel("time [s]")
    plot.legend()
    plot.show()


def test():
    # tricky list to test score
    # z = GameArray([-1, -2, -1, 1, 2, 3, 0, 3, 3, 0])
    z = GameArray([-3, -2, -2, -1, -1, -1, 0, 1, 2, 3])
    z.preprocess(0)
    print(z.calc_max_score())

    return 0


verbose_mode = False
timer_mode = False
evil_mode = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove Game max score calculator.')
    parser.add_argument('-m', '--mode', help='Execution modes (1, 2, 3 or 4).', required=False, default='1')
    parser.add_argument('-l', '--length', help='List length.', required=False, default='10')
    parser.add_argument('-n', '--number', help='Number of lists.', required=False, default='1')
    parser.add_argument('-s', '--step', help='Step size.', required=False, default='100')
    parser.add_argument('-e', '--exponent', help='List grows <value> times bigger with each step.', required=False,
                        default=1)
    parser.add_argument('-r', '--repeats', help='Repeats per step.', required=False, default='10')
    parser.add_argument('--min', help='Minimum integer to generate.', required=False, default='-3')
    parser.add_argument('--max', help='Maximum integer to generate.', required=False, default='3')
    parser.add_argument('-v', '--verbose', help='More information.', required=False, action='store_true')
    parser.add_argument('-t', '--timer', help='Show time spent on main algorithm.', required=False, action='store_true')
    parser.add_argument('--evil', help='Random data generator stops being random and generates long lists of '
                                       'neighbouring numbers', required=False, action='store_true')
    # TODO more args
    args = parser.parse_args()

    if args.verbose:
        verbose_mode = True
    if args.timer:
        timer_mode = True
    if args.evil:
        evil_mode = True

    if args.mode is '1':    # nothing required, only stdin (can be used interactively)
        mode_one()
    elif args.mode is '2':  # optional: -l -m --min --max, default: -l10 -n1
        try:
            mode_two(int(args.length), int(args.number), int(args.min), int(args.max))
        except ValueError:
            print("Every argument value needs to be an integer!")
    elif args.mode is '3':
        try:
            mode_three(int(args.length), int(args.step), int(args.repeats), int(args.number), int(args.min),
                       int(args.max), int(args.exponent))
        except ValueError:
            print("Every argument value needs to be an integer!")
    elif args.mode is '4':
        val_pairs = []
        # try:
        #     for line in sys.stdin:
        #         strings = line.split()
        #         val_pairs.append((int(strings[0]), int(strings[1])))
        #
        #     mode_four(int(args.length), int(args.step), int(args.repeats), int(args.number), int(args.exponent),
        #               val_pairs)
        # except ValueError:
        #     print("Incorrect data (check for non-integers).")
        for line in sys.stdin:
            strings = line.split()
            val_pairs.append((int(strings[0]), int(strings[1])))

        mode_four(int(args.length), int(args.step), int(args.repeats), int(args.number), int(args.exponent),
                  val_pairs)
