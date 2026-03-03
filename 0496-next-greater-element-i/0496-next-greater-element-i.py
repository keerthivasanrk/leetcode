from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        ans = []

        for i in nums1:
            found = False

            # Find index of i in nums2
            for j in range(len(nums2)):
                if nums2[j] == i:
                    
                    # Search to the right of j
                    for k in range(j + 1, len(nums2)):
                        if nums2[k] > i:
                            ans.append(nums2[k])
                            found = True
                            break
                    
                    if not found:
                        ans.append(-1)
                    
                    break   # break after handling this i

        return ans