class Solution(object):
    def findPeakElement(self, nums):
        if len(nums)==1:
            return 0
        if nums[0]>nums[1]:
            return 0
        if nums[len(nums)-1]>nums[len(nums)-2]:
            return len(nums)-1
        l,h=1,len(nums)-1
        while l<=h:
            mid=(l+h)//2
            if nums[mid-1]<nums[mid] and nums[mid]>nums[mid+1]:
                return mid
            elif nums[mid]>nums[mid-1]:
                l=mid+1
            else:
                h=mid-1
        """
        :type nums: List[int]
        :rtype: int
        """
        