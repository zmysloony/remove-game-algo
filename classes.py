from copy import copy, deepcopy


def add(*args):
    args = [a for a in args if not a is None]
    return 2*args[0] - sum(args) if args else None


class Sublist:
    alg_type = 0 # 1 - algo1; 0 - house robber
    nums = []
    left = 0
    gains = []

    def __init__(self, nums, alg_type):
        self.alg_type = alg_type
        self.nums = nums
        self.left = len(self.nums)
        self.gains = [0] * len(self.nums)
        self.calculate_gains()

    def print(self):
        return ("robber: " if self.alg_type is 0 else "algo1: ") + str(self.nums) + ", "

    def append(self, n):
        self.nums.append(n)

    def calculate_gains(self):
        if len(self.nums) == 1:
            return
        for i in range(len(self.nums)):
            if i is 0:
                self.gains[i] = add(self.nums[i], self.nums[i+1])
            elif i is len(self.nums)-1:
                self.gains[i] = add(self.nums[i], self.nums[i-1])
            else:
                self.gains[i] = add(self.nums[i], self.nums[i-1], self.nums[i+1])

    def get_max_gain(self):
        maxg = None
        maxi = None
        for i in range(len(self.nums)):
            if self.nums[i] is None:
                continue
            elif maxg is None or self.gains[i] > maxg:
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


class GameArray:
    nums = []
    sublists = []
    left = 0

    def __init__(self, _nums):
        self.nums = copy(_nums)


    def print(self):
        ret = "[ "
        for i in self.sublists:
            ret += i.print()
        print(ret + " ]")


    def preprocess(self, mode):
        if mode is 0:
            self.nums.sort()
            new_nums = []
            prev = 1.5
            for i in self.nums:
                print(new_nums)
                if i == prev:
                    new_nums[len(new_nums)-1] += i
                elif i == prev + 1:
                    prev = i
                    new_nums.append(i)
                else: #new subarray
                    if len(new_nums) is not 0: # decides which algo to use
                        self.sublists.append(Sublist(copy(new_nums), 1 if new_nums[0] <= 0 else 0))
                    new_nums.clear()
                    prev = i
                    new_nums.append(i)
            self.nums = new_nums
        self.left = len(self.nums)

    def calc_max_score(self):
        total = 0
        for i in self.sublists:
            if i.alg_type == 0:
                total += house_robber(i)
            else:
                total += algo_one(i)
        return total


def algo_one(game_array):
    temp = deepcopy(game_array)
    res = 0
    while temp.left != 0:
        res += temp.remove_num(temp.get_max_gain())
        #print("\n\n", temp.nums, "\n", temp.gains)
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

