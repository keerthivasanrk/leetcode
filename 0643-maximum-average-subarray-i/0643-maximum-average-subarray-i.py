class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        cs = sum(nums[:k])
        maxi=cs
        for r in range(k,len(nums)):
            cs+= nums[r]-nums[r-k]
            maxi = max(maxi,cs)
        return float(maxi)/k