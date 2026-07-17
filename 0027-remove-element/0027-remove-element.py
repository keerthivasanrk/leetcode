class Solution(object):
    def removeElement(self, nums, val):
        k=0
        for i in nums:
            if i==val:
                continue
            else:
                nums[k]=i
                k+=1
        return k
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        