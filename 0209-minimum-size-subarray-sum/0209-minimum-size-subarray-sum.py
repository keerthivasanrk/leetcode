class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        r = 0
        sum = 0 
        mini = float('inf')

        while r<len(nums):
            sum+=nums[r]
            while sum>=target:
                mini =  min(mini,r-l+1)
                sum -= nums[l]
                l+=1
                
            r +=1
        return 0 if mini == float('inf') else mini