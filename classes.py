from copy import copy


def add(*args):
    args = [a for a in args if not a is None]
    return 2*args[0] - sum(args) if args else None



class GameArray:
    nums = []
    gains = []
    left = 0

    def __init__(self, _nums):
        self.nums = copy(_nums)

    def preprocess(self, mode):
        if mode is 0:
            self.nums.sort()
            new_nums = []
            prev = None
            for i in self.nums:
                if i == prev:
                    new_nums[len(new_nums)-1] += i
                else:
                    prev = i
                    new_nums.append(i)
            self.nums = new_nums
        self.gains = [0] * len(self.nums)
        self.left = len(self.nums)

    def calculate_gains(self):
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
            self.gains[i-2] = add(self.nums[i-2], self.nums[i-3] if i-2 != 0 else 0)
        if i < len(self.nums)-3:
            self.gains[i+2] = add(self.nums[i+2], self.nums[i+3] if i+3 != len(self.nums) else 0)
        if i > 0 and self.nums[i-1] is not None:
            self.nums[i-1] = None
            self.left -= 1
        if i < len(self.nums)-1 and self.nums[i+1] is not None:
            self.nums[i+1] = None
            self.left -= 1
        return ret
