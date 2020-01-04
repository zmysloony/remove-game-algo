from copy import copy, deepcopy
import numpy as np

debug = False


def add(*args):
    args = [a for a in args if a is not None]
    return 2*args[0] - sum(args) if args else None


class Sublist:
    alg_type = 0 # 1 - algo1; 0 - house robber
    nums = []
    left = 0
    gains = np.array

    def __init__(self, nums, alg_type):
        self.alg_type = alg_type
        self.nums = nums

        self.left = len(self.nums)
        self.gains = np.zeros((len(nums),))
        self.calculate_gains()
        self.print()

    def print(self):
        return ("robber: " if self.alg_type is 0 else "algo1: ") + str(self.nums) + ", "

    def append(self, n):
        # self.nums.append(n)
        np.append(self.nums, n)

    def calculate_gains(self):
        if len(self.nums) == 1:
            return
        for i in range(len(self.nums)):
            if i == 0:
                self.gains[i] = add(self.nums[i], self.nums[i+1])
            elif i == (len(self.nums)-1):
                self.gains[i] = add(self.nums[i], self.nums[i-1])
            else:
                self.gains[i] = add(self.nums[i], self.nums[i-1], self.nums[i+1])

    def get_max_gain(self):
        maxg = None
        maxi = 0
        for i in range(len(self.nums)):
            if self.nums[i] is not None and (maxg is None or self.gains[i] > maxg):
                maxg = self.gains[i]
                maxi = i
        return maxi

    def remove_num(self, i):
        ret = self.nums[i]
        self.left -= 1
        self.nums[i] = None
        if i > 1:
            self.gains[i - 2] = add(self.nums[i - 2], self.nums[i - 3] if i - 2 != 0 else 0)
        if i < len(self.nums) - 3:
            self.gains[i + 2] = add(self.nums[i + 2], self.nums[i + 3] if i + 3 != len(self.nums) else 0)
        if i > 0 and self.nums[i - 1] is not None:
            self.nums[i - 1] = None
            self.left -= 1
        if i < len(self.nums) - 1 and self.nums[i + 1] is not None:
            self.nums[i + 1] = None
            self.left -= 1
        return ret

    def max_score(self):
        printd("\narray:",self.nums)
        if self.alg_type == 0:
            return house_robber(self)
        elif self.nums[len(self.nums) - 1] > 0:
            scores = []
            # if zero is present - three ways to split negative and positive number
            # assuming t[i] is 0, then: 1. delete t[i], 2. delete t[i-1], 3. delete t[i+1]

            # pre-delete 0
            score = 0
            zero_i = 0
            while self.nums[zero_i] != 0:
                zero_i += 1
            printd(Sublist(self.nums[0:zero_i-1], 1).nums, Sublist(self.nums[zero_i+2:], 0).nums)
            score += algo_two(Sublist(self.nums[0:zero_i-1], 1), 0)
            score += house_robber(Sublist(self.nums[zero_i+2:], 0))
            scores.append(score)

            # pre-delete one before 0
            score = 0
            score += self.nums[zero_i-1]
            score += algo_two(Sublist(self.nums[0:zero_i-2], 1), 0)
            printd(Sublist(self.nums[0:zero_i-2], 1).nums, Sublist(self.nums[zero_i+1:], 0).nums)
            score += house_robber(Sublist(self.nums[zero_i+1:], 0))
            scores.append(score)

            #pre-delete
            score = 0
            score += self.nums[zero_i+1]
            printd(Sublist(self.nums[0:zero_i], 1).nums, Sublist(self.nums[zero_i+3:], 0).nums)
            score += algo_two(Sublist(self.nums[0:zero_i], 1), 0)
            score += house_robber(Sublist(self.nums[zero_i+3:], 0))
            scores.append(score)

            algo_one_score = algo_two(self, 0)
            printd("scores with zero split:", scores)
            printd("compared to normal", algo_one_score)
            if algo_one_score > max(scores):
                raise NameError("ZJEBANE split0: "+str(max(scores))+" normal: "+str(algo_one_score))
            return max(scores)
        else:
            self.calculate_gains()
            sc = algo_two(self, 0)
            printd("just algo1:", sc)
            return sc



class GameArray:
    nums = []
    sublists = []
    left = 0

    def __init__(self, _nums):
        self.nums = copy(_nums)

    def print(self):
        ret = "[ "
        for z in self.sublists:
            ret += z.print()
        print(ret + " ]")

    def preprocess(self, mode):
        if mode is 0:
            self.nums.sort()
            new_nums = []
            self.sublists = []
            prev = 1.5
            for i in self.nums:
                if i == prev:
                    new_nums[len(new_nums)-1] += i
                elif i == prev + 1:
                    prev = i
                    new_nums.append(i)
                else: # new subarray
                    if len(new_nums) is not 0: # decides which algo to use
                        self.sublists.append(Sublist(copy(new_nums), 1 if new_nums[0] <= 0 else 0))
                    new_nums.clear()
                    prev = i
                    new_nums.append(i)

            if len(new_nums) is not 0:  # decides which algo to use
                self.sublists.append(Sublist(copy(new_nums), 1 if new_nums[0] <= 0 else 0))
        # self.sublists = []
        # self.sublists.append(Sublist([-3, -2, -1, 0, 1, 2, 3, 4, 20, 24, 7, 8, 9], 1))
        self.left = len(self.nums)

    def calc_max_score(self):
        total = 0
        for l in self.sublists:
            total += l.max_score()
        return total


def printd(*x):
    if debug:
        print(*x)


def find_to_none(sublist):
    i = 0
    lens = len(sublist.nums)
    while sublist.nums[i] is None and i < lens:
        i += 1
    maxgain = sublist.gains[i]
    maxindices = []

    while i < lens and sublist.nums[i] is not None:
        if sublist.gains[i] > maxgain:
            maxgain = sublist.gains[i]
            maxindices = []
        if sublist.gains[i] == maxgain:
            maxindices.append(i)
        i += 1
    printd("findtonone:", maxindices)
    return maxindices


def algo_two(sublist, splitnr):
    printd("\n\nALGO_TWO ENGAGED")
    # temp = deepcopy(game_array)
    temp = Sublist.__new__(Sublist)
    temp.left = sublist.left
    temp.nums = copy(sublist.nums)
    temp.gains = copy(sublist.gains)
    res = 0

    while temp.left > 0:
        max_gain_index = temp.get_max_gain()
        m = temp.gains[max_gain_index]
        max_indices = find_to_none(temp)
        printd("\n", "\t"*splitnr, temp.nums)
        printd("\t"*splitnr,"gains:", temp.gains)
        printd("\t"*splitnr,"left:", temp.left)
        printd("\t"*splitnr,"max indices:", max_indices)
        if len(max_indices) > 1:   # split paths
            splitnr += 1
            path_scores = []
            for i in max_indices:   # for each best removal value, calculate the best path
                if temp.nums[i] is not None:
                    cp = Sublist.__new__(Sublist)
                    cp.nums = copy(temp.nums)
                    cp.gains = copy(temp.gains)
                    cp.left = copy(temp.left)
                    removed_num = cp.nums[i]

                    printd("\t" * splitnr, "[SPLITTING " + str(splitnr) + "] on " + str(i) + ": ")
                    printd("\t"*splitnr, "score after split", res + removed_num)

                    cp.remove_num(i)
                    # print("algo_one(cp)", algo_one(cp), "removed num", removed_num)
                    path_scores.append(removed_num + algo_two(cp, splitnr))
            stringmax = "return from split " + str(splitnr) + ": "
            for z in path_scores:
                stringmax += str(z) + " or "
            printd("\t"*(splitnr-1), stringmax)
            return res + max(path_scores)
        res += temp.remove_num(max_indices[0])
        printd("\t"*splitnr,"score", res)
        #print("\n\n", temp.nums, "\n", temp.gains)
    printd("\t"*splitnr,"return from normal", res)
    return res



def algo_one(sublist, splitnr):
    # temp = deepcopy(game_array)
    temp = Sublist.__new__(Sublist)
    temp.left = sublist.left
    temp.nums = copy(sublist.nums)
    temp.gains = copy(sublist.gains)
    res = 0

    while temp.left > 0:
        max_gain_index = temp.get_max_gain()
        m = temp.gains[max_gain_index]
        if m is not int:
            max_indices = [j for j, k in enumerate(temp.gains) if (k == m and temp.nums[j] is not None)]
        else:
            max_indices = max_gain_index
        printd("\n", "\t"*splitnr, temp.nums)
        printd("\t"*splitnr,"gains:", temp.gains)
        printd("\t"*splitnr,"left:", temp.left)
        printd("\t"*splitnr,"max indices:", max_indices)
        if len(max_indices) > 1:   # split paths
            splitnr += 1
            path_scores = []
            for i in max_indices:   # for each best removal value, calculate the best path
                if temp.nums[i] is not None:
                    cp = Sublist.__new__(Sublist)
                    cp.nums = copy(temp.nums)
                    cp.gains = copy(temp.gains)
                    cp.left = copy(temp.left)
                    removed_num = cp.nums[i]

                    printd("\t" * splitnr, "[SPLITTING " + str(splitnr) + "] on " + str(i) + ": ")
                    printd("\t"*splitnr, "score after split", res + removed_num)

                    cp.remove_num(i)
                    # print("algo_one(cp)", algo_one(cp), "removed num", removed_num)
                    path_scores.append(removed_num + algo_one(cp, splitnr))
            stringmax = "return from split " + str(splitnr) + ": "
            for z in path_scores:
                stringmax += str(z) + " or "
            printd("\t"*(splitnr-1), stringmax)
            return res + max(path_scores)
        res += temp.remove_num(temp.get_max_gain())
        printd("\t"*splitnr,"score", res)
        #print("\n\n", temp.nums, "\n", temp.gains)
    printd("\t"*splitnr,"return from normal", res)
    return res


def house_robber(game_array):
    arr = game_array.nums
    incl = 0
    excl = 0

    for i in arr:
        new_excl = excl if excl >= incl else incl
        # Current max including i
        incl = excl + i
        excl = new_excl
    # return max of incl and excl
    return excl if excl > incl else incl


