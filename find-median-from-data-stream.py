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
### Summary:
The given code implements a **MedianFinder** class that finds the median from a stream of numbers. It uses two heaps:  
- `small` (a max-heap simulated by pushing negative values in a min-heap) to store the smaller half of the numbers  
- `large` (a min-heap) to store the larger half of the numbers  

The median can be derived from the top elements of these two heaps (either the root of one heap if heaps are unequal in size, or the average of the roots if heaps have equal size).

### Time Complexity:
- `addNum`: Each insertion and balancing operation involves heap pushes/pops, which are O(log n).  
- `findMedian`: O(1), as it just reads the top of the heaps.

**Overall:**  
- `addNum`: O(log n) per insertion  
- `findMedian`: O(1) per query

### Space Complexity:
- O(n), where n is the number of elements added because all elements are stored in the two heaps.

### Strengths:
- Efficiently supports dynamic data insertion and median retrieval.
- Balances two heaps to keep track of median efficiently.
- `findMedian` runs in constant time.
- Uses heaps well to maintain running median without sorting.

### Weaknesses:
- Some conditions in `addNum` are redundant or incorrectly ordered, leading to subtle bugs:
  - The first balancing condition only runs if both heaps are non-empty (`if self.small and self.large and ...`), but ideally, the balancing should always be ensured.
  - This could cause the heaps to violate the invariant where all values in `small` are less or equal to those in `large`.
- The balancing logic is split into multiple if statements; this can sometimes cause unnecessary heap operations or overlooked balancing cases.
- Negative multiplication for max-heap simulation can be error-prone and harder to read.

### Suggestions for Improvement:
1. **Fix invariant checking and balancing order:**  
   Perform push into one heap first (small max-heap), then always push the top element from `small` to `large` if the max of small is greater than min of large. Then rebalance the sizes carefully.

2. **Use clearer heap balancing approach:**  
   A common pattern is:  
   - Always push new element into `small`  
   - Move the largest element from `small` to `large`  
   - Rebalance heaps if sizes differ by more than 1 by moving elements between heaps
   
3. **Code clarity:**  
   Add comments and possibly helper functions for balancing the heaps.

4. **Edge cases & testing:**  
   Run edge cases where heaps start empty, or where all inserted numbers are the same, etc. to validate correctness.

5. **Optional:** Use a Python wrapper or `heapq` utilities to make code more expressive or consider `bisect` for a sorted list approach if acceptable.

### Example improved addNum method snippet:

```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)
    # Move the largest of small to large.
    if self.small and self.large and (-self.small[0] > self.large[0]):
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    # Balance the sizes
    if len(self.small) > len(self.large) + 1:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    elif len(self.large) > len(self.small) + 1:
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

or the more standard approach:

```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)
    val = -heapq.heappop(self.small)
    heapq.heappush(self.large, val)

    if len(self.large) > len(self.small):
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

### Final summary:
The solution is efficient and correctly uses two heaps to achieve O(log n) insertion and O(1) median lookups. However, the balancing logic can be refined for clarity and correctness to avoid subtle bugs. Improving the invariant enforcement and adding comments can enhance maintainability and robustness.
'''