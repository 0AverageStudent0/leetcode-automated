# Problem Title: Top K Frequent Elements
# Language: python3
# Status: Accepted
# Runtime: 7
# Memory: 21.2
# Submission URL: https://leetcode.com/submissions/detail/1790654230/

# Azure OpenAI Analysis: **Summary:**  
# Azure OpenAI Analysis: The code finds the top k frequent elements from the input list `nums`. It uses a frequency map (`defaultdict(int)`) to count occurrences, then pushes all elements with their negative frequency onto a heap to simulate a max-heap. It then pops the heap k times to get the k most frequent elements.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Strengths:**  
# Azure OpenAI Analysis: 1. **Correctness:** The solution correctly identifies the top k frequent elements.  
# Azure OpenAI Analysis: 2. **Clarity:** The code is straightforward and easy to understand.  
# Azure OpenAI Analysis: 3. **Use of heapq:** Using a heap is an efficient approach to solve this problem in O(n log n) time approximately.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Weaknesses:**  
# Azure OpenAI Analysis: 1. **Imports not included:** The solution uses `defaultdict` and `heapq` but does not import these modules.  
# Azure OpenAI Analysis: 2. **Time complexity:** Pushing all elements into the heap takes O(n log n) time. This can be optimized, especially if k is much smaller than n.  
# Azure OpenAI Analysis: 3. **Negation for max heap:** This is common, but it could be more explicit or use `heapq.nlargest` for readability.  
# Azure OpenAI Analysis: 4. **Variable naming:** Mixing `num, cnt` and `cnt, num` when popping the heap can be confusing.  
# Azure OpenAI Analysis: 5. **Comments / Docstring:** The code lacks any comments or a docstring explaining the approach.  
# Azure OpenAI Analysis: 6. **Type hint missing imports:** `List[int]` is used but `List` is not imported from `typing`.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Suggestions for Improvement:**  
# Azure OpenAI Analysis: 1. **Add necessary imports:**  
# Azure OpenAI Analysis:    ```python
# Azure OpenAI Analysis:    from collections import defaultdict
# Azure OpenAI Analysis:    import heapq
# Azure OpenAI Analysis:    from typing import List
# Azure OpenAI Analysis:    ```  
# Azure OpenAI Analysis: 2. **Use `Counter` from collections:** It simplifies frequency counting:  
# Azure OpenAI Analysis:    ```python
# Azure OpenAI Analysis:    from collections import Counter
# Azure OpenAI Analysis:    ```  
# Azure OpenAI Analysis: 3. **Use `heapq.nlargest` for cleaner code:**  
# Azure OpenAI Analysis:    ```python
# Azure OpenAI Analysis:    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
# Azure OpenAI Analysis:        count = Counter(nums)
# Azure OpenAI Analysis:        return [item for item, freq in heapq.nlargest(k, count.items(), key=lambda x: x[1])]
# Azure OpenAI Analysis:    ```  
# Azure OpenAI Analysis:    This avoids the need to manually push and pop the heap.  
# Azure OpenAI Analysis: 4. **Add comments and a docstring:** Briefly explain the approach for clarity.  
# Azure OpenAI Analysis: 5. **Handle edge cases:** Though likely not necessary given constraints, adding a check for empty input or k=0 could improve robustness.  
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: **Revised Example:**
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ```python
# Azure OpenAI Analysis: from typing import List
# Azure OpenAI Analysis: from collections import Counter
# Azure OpenAI Analysis: import heapq
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: class Solution:
# Azure OpenAI Analysis:     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
# Azure OpenAI Analysis:         """
# Azure OpenAI Analysis:         Return the k most frequent elements in nums.
# Azure OpenAI Analysis:         Uses Counter to count frequencies and heapq.nlargest to get top k.
# Azure OpenAI Analysis:         """
# Azure OpenAI Analysis:         if not nums or k == 0:
# Azure OpenAI Analysis:             return []
# Azure OpenAI Analysis:         
# Azure OpenAI Analysis:         count = Counter(nums)
# Azure OpenAI Analysis:         # Get k elements with the highest frequency
# Azure OpenAI Analysis:         return [num for num, freq in heapq.nlargest(k, count.items(), key=lambda x: x[1])]
# Azure OpenAI Analysis: ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: This version is more concise, readable, and leverages Python's built-in utilities effectively.

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = defaultdict(int)
        for num in nums:
            count[num] += 1
        heap = []
        for num,cnt in count.items():
            heapq.heappush(heap,[-1 * cnt, num])
        res = []
        while len(res) < k:
            cnt,num = heapq.heappop(heap)
            res.append(num)
        return res