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
### Summary
This solution implements a data structure to efficiently find the median from a data stream using two heaps:
- **`small`**: A max heap implemented as a min heap with negative values, storing the smaller half of the numbers.
- **`large`**: A min heap storing the larger half of the numbers.

When a new number is added via `addNum()`, it is pushed onto the `small` heap as a negative number. The code then balances the heaps to ensure the size difference is at most 1 and maintains the ordering such that all elements in `small` are ≤ all elements in `large`.

The `findMedian()` method returns the median:
- If one heap is larger, it returns the root of that heap.
- If both heaps are equal size, it returns the average of the roots of both heaps.

---

### Time Complexity
- `addNum(num)`: O(log n) — Insertion into a heap and balancing the heaps involves a few heap push/pop operations, each O(log n).
- `findMedian()`: O(1) — Median is found by peeking at top elements of the heaps.

### Space Complexity
- O(n) — The heaps together store all the inserted numbers (`n` is the number of elements added).

---

### Strengths
- Efficient median retrieval in O(1) time.
- Handles a dynamic stream of numbers incrementally.
- Balances heaps well to maintain median correctness.
- Uses a well-known and optimal approach with two heaps.

---

### Weaknesses
- The first `if` check inside `addNum` (`if self.small and self.large and ...`) can be simplified or integrated into a more clear heap balancing logic.
- The use of the first `heappush` always on `small` may cause unnecessary steps; typically, the number should be pushed on one heap or the other based on comparison rather than always on `small`.
- Some repeated code, like negation and heap operations, can be wrapped into helper functions for clarity.
- Lacks comments explaining the heap inversion and balancing strategy, which might be confusing.

---

### Suggestions for Improvement
1. **Explicit insertion logic**: Instead of always pushing on `small`, first decide which heap the number belongs to by comparing it to current medians, then push — this can reduce unnecessary element movement.
   
2. **Better balancing routine**: After insertion, just balance heaps by size difference only, rather than conditionally popping from heaps.

3. **Add comments** explaining the use of the negative values in `small` heap to represent a max heap.

4. **Code readability**: Introduce helper methods, e.g., `balance_heaps()` or `push_num(num)`.

5. **Edge cases**: explicitly handle the empty state in `findMedian()`, although LeetCode problem constraints may guarantee at least one number.

---

### Example of an improved `addNum` structure:

```python
def addNum(self, num: int) -> None:
    # Push to one of the heaps depending on num
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)

    # Balance heaps to ensure size difference <= 1
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

This approach removes the initial unconditional push to `small`, improving efficiency.

---

### Overall
This is a standard and efficient solution with some minor inefficiencies and clarity issues that can be improved. The time and space complexities are optimal for this problem.
'''