class Solution(object):
    def threeSum(self, nums):
        nums.sort()
        n = len(nums)
        l = [ ]
        for i in range(n - 2):
            if i>0 and nums[i]==nums[i-1]:
                continue
            L= i + 1
            R= n - 1
            while L < R:
                total = nums[i] + nums[L] + nums[R]
                if total == 0:
                    l.append([nums[i], nums[L], nums[R]])
                    while L < R and nums[L] == nums[L+1]:
                        L += 1
                    while L < R and nums[R] == nums[R-1]:
                        R -= 1
                    L += 1
                    R -= 1
                elif total < 0:
                    L += 1
                else:
                    R -= 1
        return l
                
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        