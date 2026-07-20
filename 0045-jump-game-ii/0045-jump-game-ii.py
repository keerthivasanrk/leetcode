class Solution(object):
    def jump(self, nums):
        jump=0
        curr_end=0
        farthest=0
        for i in range(len(nums)-1):
            farthest=max(farthest,i+nums[i])
            if i==curr_end:
                jump+=1
                curr_end=farthest
            if curr_end>=len(nums)-1:
                return jump
        return jump
        
        """
        :type nums: List[int]
        :rtype: int
        """
        