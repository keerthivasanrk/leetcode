class Solution(object):
    def twoSum(self, nums, target):
        d={}
        for i,x in enumerate(nums):
            need = target - x
            if need in d:
                return [d[need],i]
            d[x] = i
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        