class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        sumi = sum(nums[:k])
        maxi = sumi
        for i in range(k,len(nums)):
            sumi+=nums[i]
            sumi-=nums[i-k]
            maxi = max (maxi,sumi)
        return maxi/k

            
