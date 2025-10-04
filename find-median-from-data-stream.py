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
Here is the analysis of the provided Python3 solution for the "Find Median from Data Stream" problem:

---

### Summary

The code implements a `MedianFinder` class which maintains running median from a data stream. It uses two heaps:
- `self.small`: a max-heap implemented by pushing negative values into Python’s min-heap, which stores the smaller half of the numbers.
- `self.large`: a min-heap, which stores the larger half of the numbers.

In `addNum()`, the number is added to the `small` heap by default (as a negative), then the heaps are balanced by moving elements between them if necessary to maintain size constraints and ordering. The `findMedian()` method returns the median based on the size of the heaps:
- If one heap has more elements, the median is the root element of that heap.
- If both heaps have equal size, the median is the average of the roots of both heaps.

---

### Time Complexity

- `addNum(num)`:
  - Inserting an element into a heap: O(log n)
  - Balancing heaps involves at most one or two heap push/pop operations: O(log n)
  - So, total time complexity per `addNum` call: **O(log n)**

- `findMedian()`:
  - Accessing the top element of heaps: O(1)
  - Simple arithmetic operations: O(1)
  - So, total time complexity per `findMedian` call: **O(1)**

---

### Space Complexity

- Two heaps collectively store all inserted numbers:
- Each inserted number is stored once either in `small` or `large`.
- So, space complexity is **O(n)** where n is the number of elements inserted.

---

### Strengths

- Uses the optimal and commonly accepted approach of two heaps to maintain balance.
- Efficient both in time and space.
- Clear and straightforward balancing of two heaps after adding a number.
- `findMedian()` runs in constant time, which is ideal for median queries.
- Correctly handles both odd and even number of elements.

---

### Weaknesses

- The balancing logic between heaps in `addNum` is somewhat repetitive and can be simplified.
- The condition `if self.small and self.large and (-1 * self.small[0] > self.large[0]):` might cause unnecessary work if not followed carefully (pushing and popping more than needed).
- The code pushes the number always initially to `small` heap; some implementations push to the correct heap depending on the element value to reduce balancing steps.
- The code always does 3 separate if conditions to balance the heaps. In some edge cases, the balancing can be done more cleanly.
- No import statement for `heapq`. It is implied, but for standalone completeness, it should be included.

---

### Suggestions for Improvement

1. **Add import statement** for `heapq` at the top to ensure the code runs standalone:
   ```python
   import heapq
   ```

2. **Improve readability and balance logic:**

   Instead of pushing always to `small`, push conditionally:
   ```python
   if not self.small or num <= -self.small[0]:
       heapq.heappush(self.small, -num)
   else:
       heapq.heappush(self.large, num)
   ```

   Then balance heaps sizes to ensure size difference is at most 1:
   ```python
   if len(self.small) > len(self.large) + 1:
       heapq.heappush(self.large, -heapq.heappop(self.small))
   elif len(self.large) > len(self.small) + 1:
       heapq.heappush(self.small, -heapq.heappop(self.large))
   ```

3. **Optional:** Add comments for clarity to each major step.

4. If desired, wrap the heap balancing in a method to keep `addNum` cleaner.

---

### Example of Improved `addNum` Method

```python
def addNum(self, num: int) -> None:
    if not self.small or num <= -self.small[0]:
        heapq.heappush(self.small, -num)
    else:
        heapq.heappush(self.large, num)
    
    # Balance the heaps so that the size difference is at most 1
    if len(self.small) > len(self.large) + 1:
        heapq.heappush(self.large, -heapq.heappop(self.small))
    elif len(self.large) > len(self.small) + 1:
        heapq.heappush(self.small, -heapq.heappop(self.large))
```

This logic ensures fewer moves between heaps and is easier to understand.

---

# Summary of complexities:

| Operation   | Time Complexity | Space Complexity |
|-------------|-----------------|------------------|
| addNum      | O(log n)        | O(n)             |
| findMedian  | O(1)            | O(n)             |

---

This code is a sound, efficient solution for the median from data stream problem with minor improvements possible in code clarity and heap balancing logic.
'''