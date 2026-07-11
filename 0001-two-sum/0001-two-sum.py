class Solution(object):
    def twoSum(self, nums, target):
        d={}
        i=0
        while i<len(nums):
            need=target-nums[i]
            if need in d:
                return [d[need],i]
            d[nums[i]]=i  
            i+=1  

        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        