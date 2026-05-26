class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        def count_less_or_equal(target: int) -> int:
            count = 0
            for i in range(1, m + 1):
                # Count how many numbers in row i are <= target
                count += min(target // i, n)
            return count

        # Binary search over the value range [1, m * n]
        low, high = 1, m * n
        result = high

        while low <= high:
            mid = (low + high) // 2
            if count_less_or_equal(mid) >= k:
                result = mid
                high = mid - 1  # Try to find a smaller valid number
            else:
                low = mid + 1   # Increase the target value

        return result
