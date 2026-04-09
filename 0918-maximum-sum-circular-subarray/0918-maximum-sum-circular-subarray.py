class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        psum = 0
        pms = 0
        fms = nums[0]
        fsum = nums[0]
        t = 0
        for i in nums:
            psum = max(i,psum+i)
            fsum = max(fsum,psum)
            pms = min(i,pms+i)
            fms = min(fms,pms)
            t+=i
        if fsum < 0:
            return fsum
        return max(fsum, t - fms)
        