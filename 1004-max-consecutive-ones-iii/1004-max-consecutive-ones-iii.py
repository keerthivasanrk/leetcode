class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        z = 0
        l = 0
        maxi = 0
        for r in range(len(nums)):
            if nums[r]==0:
                z+=1
            while z>k:
                if nums[l]==0:
                    z -=1
                l+=1
            maxi = max(maxi,r-l+1)
        return maxi

