class Solution:
    def maxArea(self, height: List[int]) -> int:
        search_len = len(height)
        start_idx = 0
        end_idx = search_len - 1
        improved = True
        max_area = 0

        while start_idx < end_idx:
            new_area = (end_idx - start_idx) * min(height[start_idx], height[end_idx])
            max_area = new_area if new_area > max_area else max_area

            if height[start_idx] < height[end_idx]:
                start_idx += 1
            else:
                end_idx -= 1

        return max_area
            