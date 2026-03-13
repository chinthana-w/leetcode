class Solution:
    def maxArea(self, height: List[int]) -> int:
        search_len = len(height)
        start_idx = 0
        end_idx = search_len - 1
        improved = True
        max_area = 0

        while start_idx < end_idx:
            max_area = max(
                max_area, 
                (end_idx - start_idx) * min(height[start_idx], height[end_idx])
            )

            if height[start_idx] < height[end_idx]:
                start_idx += 1
            else:
                end_idx -= 1

        return max_area
            