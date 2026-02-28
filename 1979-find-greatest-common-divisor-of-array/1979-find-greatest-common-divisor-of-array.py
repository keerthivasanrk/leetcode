class Solution:
    def findGCD(self, nums: List[int]) -> int:
        a=max(nums)
        b=min(nums)
        while b!=0:
            a,b=b,a%b
        return a