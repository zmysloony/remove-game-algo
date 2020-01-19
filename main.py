from random import randrange

from classes import *
import argparse
import sys
import time
import matplotlib.pyplot as plot


def gen_random(size, min_num, max_num):
    r = []
    if evil_mode:
        z = min_num
        for i in range(size):
            r.append(z)
            if randrange(0, 100, 1) <= 40:  # don't increase the number (makes duplicates)
                z += 1
        # print(r)
        return r

    for i in range(size):
        r.append(randrange(min_num, max_num, 1))
    return r


def mode_one():    # parse lines into number arrays
    for fl in sys.stdin:
        fl = fl.replace(',', '')
        fls = fl.split()
        nums = []
        try:
            for st in fls:
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


def mode_two(ls, n, min_num, max_num):
    if timer_mode:
        t = 0
        for i in range(n):
            rarray = GameArray(gen_random(ls, min_num, max_num))
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
            rarray = GameArray(gen_random(ls, min_num, max_num))
            rarray.preprocess(0)
            s = rarray.calc_max_score()
            if verbose_mode:
                print(rarray.nums)
                print("Max score:", s)
            else:
                print(s)


# ls - starting list length, l_step - increments by that amount with each step, r - repeats for the same step
def mode_three(ls, l_step, r, n, min_num, max_num, e, do_plot=True):
    times = []
    sizes = []
    raw_times = []
    raw_sizes = []
    try:
        for i in range(n):
            size = (ls + i*l_step)*(e**i)
            t = 0
            for j in range(r):
                rand = gen_random(size, min_num, max_num)
                start_time = time.perf_counter()
                ga = GameArray(rand)
                ga.preprocess(0)
                ga.calc_max_score()
                nt = time.perf_counter() - start_time
                raw_times.append(nt)
                raw_sizes.append(size)
                t += nt
            if verbose_mode:
                print("Length:", size, "Time:", t/r, "s")
            sizes.append(size)
            times.append(t/r)
    except KeyboardInterrupt:
        return times, sizes, raw_times, raw_sizes
    if do_plot:
        plot.plot(sizes, times, label=str(min_num)+" to "+str(max_num), marker='o', linestyle='-')
        plot.xlabel("list size")
        plot.ylabel("time [s]")
        plot.legend()
        plot.show()
    return times, sizes, raw_times, raw_sizes


# mode three, but for selected min_num and max_num pairs
def mode_four(ls, l_step, r, n, e, pairs):
    ax = plot.gca()
    for pair in pairs:
        min_num, max_num = pair
        if verbose_mode:
            print("min:", min_num, "\tmax:", max_num)
        times, sizes, rawt, raws = mode_three(ls, l_step, r, n, min_num, max_num, e, do_plot=False)
        c = next(ax._get_lines.prop_cycler)['color']
        plot.plot(sizes, times, label=str(min_num)+" to "+str(max_num), linestyle='-', lw=2, color=c)
        plot.plot(raws, rawt, marker='+', ms=4, linestyle='', color=c)

    plot.title(str(r) + " samples per point" + (" [single chain]" if evil_mode else ""))
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
