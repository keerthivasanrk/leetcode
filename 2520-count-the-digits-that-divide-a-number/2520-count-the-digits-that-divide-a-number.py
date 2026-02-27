class Solution:
    def countDigits(self, num: int) -> int:
        original = num
        count = 0
        
        while num > 0:
            digit = num % 10
            
            if digit != 0 and original % digit == 0:
                count += 1
                
            num //= 10
        
        return count