class Solution:
    def subarraySum(self, nums, k):

        prefix = 0
        count = 0
        seen = {0:1}

        for num in nums:

            prefix += num

            if prefix - k in seen:
                count += seen[prefix-k]

            if prefix in seen:
                seen[prefix] += 1
            else:
                seen[prefix] = 1

        return count