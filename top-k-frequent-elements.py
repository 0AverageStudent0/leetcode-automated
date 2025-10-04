# Problem Title: Top K Frequent Elements
# Language: python3
# Status: Accepted
# Runtime: 7
# Memory: 21.2
# Submission URL: https://leetcode.com/submissions/detail/1790654230/

# Azure OpenAI Analysis: Let's analyze the provided solution for the "Top K Frequent Elements" problem.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ```python
# Azure OpenAI Analysis: class Solution:
# Azure OpenAI Analysis:     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
# Azure OpenAI Analysis:         count = defaultdict(int)
# Azure OpenAI Analysis:         for num in nums:
# Azure OpenAI Analysis:             count[num] += 1
# Azure OpenAI Analysis:         heap = []
# Azure OpenAI Analysis:         for num,cnt in count.items():
# Azure OpenAI Analysis:             heapq.heappush(heap,[-1 * cnt, num])
# Azure OpenAI Analysis:         res = []
# Azure OpenAI Analysis:         while len(res) < k:
# Azure OpenAI Analysis:             cnt,num = heapq.heappop(heap)
# Azure OpenAI Analysis:             res.append(num)
# Azure OpenAI Analysis:         return res
# Azure OpenAI Analysis: ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Summary:
# Azure OpenAI Analysis: The solution counts the frequency of each number using a hash map (`defaultdict`). It then pushes each (frequency, number) pair into a max-heap (implemented as a min-heap with negative counts). Finally, it pops the top k elements from the heap to form the result list.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Time Complexity:
# Azure OpenAI Analysis: - Counting frequencies: O(n), where n is the length of `nums`
# Azure OpenAI Analysis: - Building the heap with unique elements: O(m log m), where m is the number of unique elements
# Azure OpenAI Analysis: - Extracting k elements from the heap: O(k log m)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: Overall, the time complexity is:  
# Azure OpenAI Analysis: **O(n + m log m + k log m)**  
# Azure OpenAI Analysis: Since m ≤ n, this can be simplified to:  
# Azure OpenAI Analysis: **O(n log n)** in the worst case where all elements are unique.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Space Complexity:
# Azure OpenAI Analysis: - Frequency dictionary: O(m)
# Azure OpenAI Analysis: - Heap: O(m)
# Azure OpenAI Analysis: - Result list: O(k)
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: Overall, **O(m + k)** extra space is used, with m ≤ n.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Strengths:
# Azure OpenAI Analysis: - Correctly solves the problem as described.
# Azure OpenAI Analysis: - Uses a max-heap to efficiently retrieve the top k frequent elements.
# Azure OpenAI Analysis: - Simple and easy-to-understand approach.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Weaknesses:
# Azure OpenAI Analysis: - Uses a max-heap containing all unique elements, which can be inefficient if many unique elements.
# Azure OpenAI Analysis: - Pushes all unique elements onto the heap, even though we only need the top k. This can be improved by using a min-heap of size k to keep track of the top k frequencies.
# Azure OpenAI Analysis: - The code does negative frequency multiplication manually instead of using Python's `heapq` capabilities for max heap alternatives or other libraries.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Suggestions for Improvement:
# Azure OpenAI Analysis: 1. **Use a min-heap of size k:**  
# Azure OpenAI Analysis:    Instead of pushing all elements, maintain a min-heap of size k. This reduces time to O(n log k) instead of O(n log n), which is more efficient when k << n.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: 2. **Use `collections.Counter` from Python stdlib:**  
# Azure OpenAI Analysis:    This removes the need for a manual counting loop and makes code more concise.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: 3. **Avoid `-1 * cnt`:**  
# Azure OpenAI Analysis:    If you want a max-heap effect, you can use a min-heap with negative counts, but naming or using `heapq.nlargest` might simplify as well.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: 4. **Alternative using `heapq.nlargest`:**  
# Azure OpenAI Analysis:    Use `heapq.nlargest` with key function on dictionary items for cleaner code.
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Example improved code snippet using `heapq.nlargest`:
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ```python
# Azure OpenAI Analysis: from collections import Counter
# Azure OpenAI Analysis: import heapq
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: class Solution:
# Azure OpenAI Analysis:     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
# Azure OpenAI Analysis:         count = Counter(nums)
# Azure OpenAI Analysis:         return [item for freq, item in heapq.nlargest(k, [(freq, num) for num, freq in count.items()])]
# Azure OpenAI Analysis: ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: Or with a min-heap of size k:
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ```python
# Azure OpenAI Analysis: from collections import Counter
# Azure OpenAI Analysis: import heapq
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: class Solution:
# Azure OpenAI Analysis:     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
# Azure OpenAI Analysis:         count = Counter(nums)
# Azure OpenAI Analysis:         min_heap = []
# Azure OpenAI Analysis:         for num, freq in count.items():
# Azure OpenAI Analysis:             if len(min_heap) < k:
# Azure OpenAI Analysis:                 heapq.heappush(min_heap, (freq, num))
# Azure OpenAI Analysis:             else:
# Azure OpenAI Analysis:                 if freq > min_heap[0][0]:
# Azure OpenAI Analysis:                     heapq.heappushpop(min_heap, (freq, num))
# Azure OpenAI Analysis:         return [num for freq, num in min_heap]
# Azure OpenAI Analysis: ```
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ---
# Azure OpenAI Analysis: 
# Azure OpenAI Analysis: ### Summary:
# Azure OpenAI Analysis: - The original solution is straightforward and correct.
# Azure OpenAI Analysis: - It's not the most efficient or concise approach.
# Azure OpenAI Analysis: - Using Python standard libraries (Counter, heapq.nlargest) and a size-limited heap can improve time complexity and readability.

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