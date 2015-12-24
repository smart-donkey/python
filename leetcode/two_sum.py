__author__ = 'roger'

import numpy as np
import random
import timeit


class feasible_solution:
    def __init__(self, lows, highs):
        self.has_low = False
        self.has_high = False
        self.lows = []
        self.highs = []

class Solution(object):
    def match_one(self, nums, k, target):
        for i in range(len(nums)):
            if k + nums[i] == target:
                return True, i

        return False, -1

    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if len(nums) == 0:
            return 0 == target, 0, 0

        if len(nums) == 1:
            return nums[0] == target, 0, nums[0]

        if len(nums) == 2:
            return nums[0] + nums[1] == target, nums[0], nums[1]

        mid = len(nums) / 2

        # match mid to left array
        match, i = self.match_one(nums[mid + 1:], nums[mid], target)
        if match:
            return True, nums[i], nums[mid]

        # match mid to right array
        match, i = self.match_one(nums[:mid], nums[mid], target)
        if match:
            return True, nums[i], nums[mid]

        # solve the right sub problem
        ret, a, b = self.twoSum(nums[:mid], target)
        if ret:
            return ret, a, b

        # solve the left sub problem
        return self.twoSum(nums[mid:], target)

    def twoSum_simple(self, nums, target):
        if len(nums) == 0:
            return False, -1, -1

        if len(nums) == 1:
            return nums[0] == target, 0, nums[0]

        if len(nums) == 2:
            return nums[0] == nums[1], nums[0], nums[1]

        for i in range(len(nums)):
            k = nums[-1]
            match, i = self.match_one(nums[:-1], k, target)
            if match:
                return True, nums[i], nums[-1]
            return self.twoSum_simple(nums[:-1], target)

    def twoSum_dp(self, nums, target):
        table = []
        for i in range(target/2 + 1):
            f = feasible_solution([],[])
            table.append(f)

        for index in range(len(nums)):
            i = nums[index]
            if i <= (target / 2):
                # print i
                # print 'table len', len(table)
                table[i].has_low = True
                table[i].lows.append(index)
                if table[i].has_high:
                    return [index, table[i].highs[0]]
            elif i > (target / 2) and i <= target:
                # print i
                table[target - i].has_high = True
                table[target - i].highs.append(index)
                if table[target - i].has_low:
                    return [table[target - i].lows[0] , index]

        return [-1, -1]


    def twoSum_sort(self, nums, target):
        if len(nums) <= 1:
            return [-1, -1]

        data = [(v, index) for index, v in enumerate(nums)]
        data = sorted(data)
        for i in range(len(data) - 1):
            key = data[i][0]
            remaining = target - key
            find = Solution.binary_search(data[i + 1:], remaining)
            if find >= 0:
                return sorted([data[i][1], data[find + i + 1][1]])

    @staticmethod
    def binary_search(a, key):
        if len(a) == 0:
            return -1

        if len(a) == 1:
            if a[0][0] == key:
                return 0
            else:
                return -1

        mid = len(a) / 2
        if a[mid][0] == key:
            return mid
        elif a[mid][0] < key:
            i = Solution.binary_search(a[mid:], key)
            if i > 0:
                return mid + i
            else:
                return -1
        else:
            return Solution.binary_search(a[:mid], key)


def test_speed1(nums, target):
    s = Solution()
    s.twoSum_simple(nums, target)


def test_speed2(nums, target):
    s = Solution()
    print s.twoSum(nums, target)


def test_speed3(nums, target):
    s = Solution()
    print s.twoSum_dp(nums, target)

if __name__ == '__main__':
    # c = 10
    # t = random.randint(0, c * 3)
    # n = np.random.randint(0, c * 2, c)
    # n = [2, 3, 4]
    # t = 6
    # print n, t
    # test_speed3(n, t)
    # print t
    n = [3,2,4]
    s = Solution()
    print s.twoSum_sort(n, 6)
    # print Solution.binary_search(n, 26)
    # print n