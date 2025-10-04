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
Certainly! Here's a thorough analysis of the provided solution for the "Find Median from Data Stream" problem:

---

### Summary of the Code

The `MedianFinder` class maintains two heaps to efficiently find the median of a stream of numbers:
- `self.small`: a max heap implemented by pushing negated numbers (to use Python's min heap), which stores the smaller half of the numbers.
- `self.large`: a min heap, which stores the larger half of the numbers.

When a new number is added using `addNum`:
1. The number is first pushed onto `self.small` (after negation).
2. The code ensures the order property by moving elements between the two heaps if the max of `small` is greater than the min of `large`.
3. The heaps are balanced to ensure that their lengths differ by at most 1.

The median is found in:
- `findMedian()` by returning the root element of the larger heap if heaps are uneven,
- or the average of the roots of both heaps if they have equal length.

---

### Time Complexity

- `addNum`: Operations primarily involve `heapq.heappush` and `heapq.heappop` on heaps of size roughly `n/2` each. Each push/pop operation takes `O(log n)` time. Balancing heaps and comparisons are `O(1)`.
  
  Hence, the time complexity of `addNum` is **O(log n)** per insertion.

- `findMedian`: Accessing the heap root is `O(1)`, so median retrieval is **O(1)**.

---

### Space Complexity

- The data structure uses two heaps that collectively store all numbers added so far.
- Space complexity is **O(n)** where `n` is the total number of elements processed.

---

### Strengths

- **Efficient median retrieval:** `findMedian` is constant time, which is optimal.
- **Balanced heaps approach:** Classic, proven, efficient approach to median maintenance ensuring balanced partitions.
- **Simple and clean code:** Clear separation between adding numbers and finding median.
- **Correct balancing checks** ensure heaps' sizes differ by no more than 1.

---

### Weaknesses

- In `addNum` method, the first step *always* pushes into `self.small`. This might not be optimal; for some inputs, the number could belong to `self.large` instead. Although later balancing fixes this, initially pushing into the wrong heap could cause unnecessary moves between heaps.
- There is a repeated check for balancing and rebalancing heaps that could be combined or made clearer.
- The conditional `if self.small and self.large and (-1 * self.small[0] > self.large[0]):` only executes if both heaps are non-empty, but pushing directly into `self.small` every time means `self.large` might be empty initially, so the first few pushes might not put the number in the right heap immediately.
- The handling of the balancing logic can be more intuitive, making the code easier to read and maintain.

---

### Suggestions for Improvement

1. **Decide heap based on the number to be added:**
   - Instead of pushing every element to `self.small` by default, compare the new number with the current medians or roots to decide which heap it should go to. For example:
     ```python
     if not self.small or num <= -self.small[0]:
         heapq.heappush(self.small, -num)
     else:
         heapq.heappush(self.large, num)
     ```
   This reduces unnecessary heap operations.

2. **Simplify balancing logic:**
   - After pushing the element to a proper heap, ensure heaps differ by at most 1 element by moving items from the larger heap to the smaller heap if needed.

3. **Add comments or docstrings** to improve code readability and maintainability.

4. **Edge case handling:** The current code handles empty states well, but explicit comments can clarify the logic.

---

### Example Refactored `addNum` method (for clarity):

```python
def addNum(self, num: int) -> None:
    # Decide which heap to push onto
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)
    
    # Rebalance heaps so length difference <= 1
    if len(self.small) > len(self.large) + 1:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    elif len(self.large) > len(self.small) + 1:
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

This can improve efficiency by reducing the number of elements moved between the heaps.

---

### Final remarks

Overall, the code implements a well-known and effective approach to the problem. With minor improvements to heap insertion logic and added comments, it can be made more efficient and readable.

---

Let me know if you'd like me to suggest complete refactored code!
'''