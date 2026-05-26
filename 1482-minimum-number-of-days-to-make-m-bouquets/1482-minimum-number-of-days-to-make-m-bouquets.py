class Solution:
    def is_valid(self, mid: int, bloomDay: list[int], m: int, k: int) -> bool:
        bouquets = 0
        consecutive_flowers = 0
        
        for day in bloomDay:
            if day <= mid:
                consecutive_flowers += 1
                # We found enough adjacent flowers to make 1 bouquet
                if consecutive_flowers == k:
                    bouquets += 1
                    consecutive_flowers = 0  # Reset for the next bouquet
            else:
                # The streak is broken because this flower hasn't bloomed yet
                consecutive_flowers = 0
                
        # Return True if we managed to make at least m bouquets
        return bouquets >= m

    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        n = len(bloomDay)
        if m * k > n:
            return -1
            
        l = min(bloomDay)
        h = max(bloomDay)
        ans = -1
        
        while l <= h:
            mid = (l + h) // 2
            # Pass bloomDay, m, and k into the helper function
            if self.is_valid(mid, bloomDay, m, k):
                ans = mid      # mid is a possible answer
                h = mid - 1    # Try to find a smaller (earlier) day
            else:
                l = mid + 1    # Need more days for flowers to bloom
                
        return ans
