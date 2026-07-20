class Solution(object):
    def maxProfit(self, prices):
        profit=0
        for i in range(1,len(prices)):
            if prices[i]>prices[i-1]:
                val=prices[i]-prices[i-1]
                profit+=val
            else:
                continue
        return profit
        """
        :type prices: List[int]
        :rtype: int
        """
        