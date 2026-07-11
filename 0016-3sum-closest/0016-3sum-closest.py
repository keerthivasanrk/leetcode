class Solution(object):
    def threeSumClosest(self, nums, target):
        nums.sort()
        n=len(nums)
        closest=nums[0] + nums[1] + nums[2]
        
        for i in range(n-2):
            L = i+1
            R = n-1
            while L<R:
                total=nums[i]+nums[L]+nums[R]
                if abs(total-target) < abs(closest-target):
                    closest=total
                elif total < target:
                    L += 1
                elif total > target:
                    R -= 1
                else:
                    return total
        return closest
                

        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        