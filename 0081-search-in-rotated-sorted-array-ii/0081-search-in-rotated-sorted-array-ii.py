class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        l, r = 0, len(nums) - 1
        
        while l <= r:
            m = (l + r) // 2
            
            if nums[m] == target:
                return True
                
            # The Critical Trick: Cannot determine which half is sorted
            if nums[l] == nums[m] == nums[r]:
                l += 1
                r -= 1
                continue
                
            # Case 1: Left half is sorted
            if nums[l] <= nums[m]:
                # Check if target is strictly within the sorted left half
                if nums[l] <= target < nums[m]:
                    r = m - 1
                else:
                    l = m + 1
                    
            # Case 2: Right half is sorted
            else:
                # Check if target is strictly within the sorted right half
                if nums[m] < target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
                    
        return False
