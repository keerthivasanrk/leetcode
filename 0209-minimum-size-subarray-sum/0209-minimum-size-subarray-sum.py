class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l=0
        mini = float('inf')
        cs=0
        for r in range(len(nums)):
            cs+=nums[r]
            while cs>=target:
                mini = min(mini,r-l+1)
                cs-=nums[l]
                l+=1
        return mini if mini!=float('inf') else 0
        
