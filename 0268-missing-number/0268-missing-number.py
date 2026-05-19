class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n=len(nums)
        s=0
        for i in nums:
            s+=i
        res = (n*(n+1))//2 - s
        return res