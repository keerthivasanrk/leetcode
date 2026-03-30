class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        
        mc = 0
        curr = 0 
        for i in nums:
            if i == 1:
                curr +=1
                mc = max(mc,curr)
            else:
                curr =0
        return mc