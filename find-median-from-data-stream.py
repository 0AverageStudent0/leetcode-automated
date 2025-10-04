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
Certainly! Here's the analysis of the given code for the "Find Median from Data Stream" problem:

---

### Brief Summary
The code implements a `MedianFinder` class that maintains a data structure to store a stream of numbers and efficiently find the median at any point. It uses two heaps:
- A max-heap (`self.small`) to store the smaller half of the numbers (implemented using a min-heap with negated values).
- A min-heap (`self.large`) to store the larger half of the numbers.

By balancing both heaps such that their sizes differ by no more than 1, it can quickly determine the median either as the top of one heap or the average of the tops of both heaps.

---

### Time Complexity
- `addNum(num)`: Each insertion involves a heap push and at most one or two heap pops/pushes. Each heap operation is **O(log n)**.
- `findMedian()`: Accessing the top element(s) of heaps is **O(1)**.

**Overall:**  
- `addNum`: O(log n)  
- `findMedian`: O(1)

---

### Space Complexity
- Both heaps together store all elements added so far, so space used is **O(n)**, where n is the number of elements processed.

---

### Strengths
- Efficient time complexity for insertion and median retrieval suitable for a streaming scenario.
- Uses a well-known and optimal approach with two heaps.
- The logic to balance heaps and maintain the size property is correct.
- Clean and straightforward implementation.

---

### Weaknesses
- The first conditional in `addNum`:
  ```python
  if self.small and self.large and (-1 * self.small[0] > self.large[0]):
  ```
  This check is redundant or slightly misplaced because immediately after pushing into `self.small`, if top of `self.small` is greater than the top of `self.large`, elements should be moved between heaps to maintain ordering — but this condition only swaps one element and does not guarantee heaps are balanced afterward.
  
- The balancing conditions after that are:
  ```python
  if len(self.small) > len(self.large) + 1:
      ...
  if len(self.large) > len(self.small) + 1:
      ...
  ```
  These ensure size balance but do not explicitly restore the order property between heaps except the first if-statement tries to do it.

- There could be an unnecessary movement of elements when both heaps are empty, for example at the first insertion into an empty structure.

- The code could use comments to improve readability.
  
- Import of `heapq` is missing (assuming it’s done outside snippet or it will cause a NameError).

---

### Suggestions for Improvement
1. **Combine ordering and balancing in a clearer way:**
   When inserting a number:
   - Push into `self.small` (max-heap) by default.
   - Then move the top element of `self.small` to `self.large` to ensure order property (`small` max ≤ `large` min).
   - Then rebalance if the size difference is greater than 1.

   This approach is simpler and recommended in the common solutions to this problem.
   
2. **Add import statement:**
   ```python
   import heapq
   ```
   
3. **Add comments to clarify each step**.
   
4. **Consider moving the negation logic into helper functions or comments to make intent clearer.**
   
5. **Add some validation or assertion tests within methods** (optional) for debugging.

---

### Example of Improved `addNum` (pseudocode):
```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)  # Push onto max heap with negation
    # Move largest of small to large to maintain order property
    if self.small and self.large and (-self.small[0] > self.large[0]):
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)

    # Rebalance sizes to ensure difference ≤ 1
    if len(self.small) > len(self.large) + 1:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    elif len(self.large) > len(self.small) + 1:
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

Or alternatively, a common idiom is:

```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)
    # Balance the largest from small to large to maintain order
    if self.small:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)

    # Rebalance sizes
    if len(self.large) > len(self.small) + 1:
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

---

### Final Summary

| Aspect            | Analysis                                  |
|-------------------|-------------------------------------------|
| Time Complexity   | O(log n) per insertion, O(1) median query |
| Space Complexity  | O(n) total elements stored                |
| Strengths         | Efficient two-heap approach, clean logic  |
| Weaknesses        | Slightly confusing ordering logic, missing import, lacks comments |
| Suggestions       | Refactor insertion logic for clarity, add imports and comments |

---

I hope this detailed review helps improve your solution! Let me know if you'd like me to provide an improved full code version.
'''