class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        f={}
        for i in nums:
            f[i]=f.get(i,0)+1
        return max(f,key=f.get)
