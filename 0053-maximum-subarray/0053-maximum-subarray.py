class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        psum = 0
        fans = nums[0]
        for i in nums:
            psum = max(i,psum+i)
            fans =  max(psum,fans)
        return fans