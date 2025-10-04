# Problem Title: Find Median from Data Stream
# Language: python3
# Status: Accepted
# Runtime: 208
# Memory: 40.2
# Submission URL: https://leetcode.com/submissions/detail/1790654417/

class MedianFinder:

    def __init__(self):
        self.small = []
        self.large = []
    def addNum(self, num: int) -> None:
        heapq.heappush(self.small,-1 * num)

        if self.small and self.large and (-1 * self.small[0] > self.large[0]):
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large,val)
        
        if len(self.small) > len(self.large) + 1:
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large,val)
        
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -1 * val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -1 * self.small[0]
        
        if len(self.large) > len(self.small):
            return self.large[0]
        
        else:
            val = (-1 * self.small[0]) + self.large[0]
            return val/2

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()

# Azure OpenAI Analysis
'''
### Summary of the Code
This Python solution implements a `MedianFinder` class to find the median of a data stream efficiently. It uses two heaps:
- `small`: a max-heap (simulated using negative values in a min-heap) to hold the smaller half of the numbers.
- `large`: a min-heap to hold the larger half of the numbers.

Numbers are added to one of the heaps; then the heaps are balanced so that their size difference is at most one. The median can be obtained by either the root of one heap (when count is odd) or the average of both roots (when count is even).

### Time Complexity
- `addNum(num)`: The main operations are heap insertions and removals. Each heap operation (`heappush`/`heappop`) is **O(log n)**. Balancing steps involve a constant number of these operations, so overall **O(log n)** per insertion.
- `findMedian()`: This just accesses the top elements of the heaps, which is **O(1)**.

### Space Complexity
- The space used is proportional to the number of elements inserted, distributed between the two heaps. Hence, **O(n)** space where *n* is the count of numbers added so far.

### Strengths
- Uses a well-known two-heap approach that is optimal for streaming median calculation.
- Balancing conditions ensure the heaps maintain size difference of at most one, which allows correct median calculation.
- Efficient median retrieval in constant time.

### Weaknesses
- The balancing condition `if self.small and self.large and (-1 * self.small[0] > self.large[0]):` may miss some edge cases and cause some unnecessary heap swapping if more careful insertion order management is employed.
- The balancing conditions could be simplified.
- The code could benefit from more descriptive comments for readability.
- There is a minor inefficiency in checking `self.small and self.large` before comparing their root values in `addNum()` when pushing into heaps; insertion logic could be optimized.
- The readability of negative number trick for max-heap could be improved through clearer naming or helper functions.

### Suggestions for Improvement
1. **Simplify the insertion logic**: Instead of always pushing into `small` first and then balancing, consider pushing the new number into the appropriate heap directly:
   - Push into `small` if empty or number is less than or equal to the max of `small`.
   - Otherwise, push into `large`.
   
   Then balance the heaps—this can reduce the number of unnecessary heap operations.

2. **Add clear comments** to describe the role of each heap and the balancing steps.

3. **Use helper methods** to encapsulate logic such as balancing heaps or pushing elements, improving code readability.

4. **Refactor median calculation** to explicitly handle odd or even counts to improve clarity.

5. **Edge case handling**: Although current code likely works for all cases, adding unit tests or assertions would ensure robustness.

---

### Example improved insertion sketch (not full code):

```python
def addNum(self, num: int) -> None:
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)
    
    # Balance heaps
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

This approach reduces the conditional complexity inside `addNum`.

---

Overall, the code implements a canonical solution to the problem with optimal time and space complexity but could benefit from minor restructuring and improved readability.
'''