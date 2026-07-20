class Solution(object):
    def canJump(self, nums):
        farthest=0
        for i in range(len(nums)):
            if i>farthest:
                return False
            farthest=max(farthest, i+nums[i])
            if farthest >= len(nums)-1:
                return True
        """
        :type nums: List[int]
        :rtype: bool
        """
        