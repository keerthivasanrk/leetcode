class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def canEatAll(speed: int) -> bool:
            hours_spent = 0
            for pile in piles:
                # Calculate ceiling division: ceil(pile / speed)
                hours_spent += (pile + speed - 1) // speed
                if hours_spent > h:
                    return False
            return True

        # Binary Search Range
        low = 1
        high = max(piles)
        ans = high

        while low <= high:
            mid = (low + high) // 2
            if canEatAll(mid):
                ans = mid       # Record valid speed
                high = mid - 1  # Try to find a slower speed
            else:
                low = mid + 1   # Need to eat faster
                
        return ans
