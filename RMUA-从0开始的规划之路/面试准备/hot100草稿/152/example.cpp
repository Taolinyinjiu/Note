#include <iostream>
#include <vector>
#include <algorithm>
#include <limits> // 用于 std::numeric_limits

class Solution {
public:
    int maxProduct(const std::vector<int>& nums) {
        // 判断传入数组是否为空
        if (nums.empty()) {
            return 0;
        }
        // 记录以当前元素结尾的子数组的最大乘积
        int max_so_far = nums[0];
        // 记录以当前元素结尾的子数组的最小乘积
        int min_so_far = nums[0];
        // 全局最大子数组乘积
        int result = nums[0];
        // 从第二个元素开始 遍历数组，更新最大和最小乘积
        for (size_t i = 1; i < nums.size(); ++i) {
            // 获取当前遍历的数组元素
            int current_num = nums[i];
            
            // 如果当前的元素为负数，则交换最大最小乘积
            if (current_num < 0) {
                std::swap(max_so_far, min_so_far);
            }
            // 更新最大乘积，其要么是当前元素本身，要么是当前元素乘以前面的最大乘积
            max_so_far = std::max(current_num, max_so_far * current_num);
            // 更新最小乘积，其要么是当前元素本身，要么是当前元素乘以前面的最小乘积
            min_so_far = std::min(current_num, min_so_far * current_num);
            // 更新全局最大乘积
            result = std::max(result, max_so_far);
        }
        // 返回最终结果
        return result;
    }
};

int main() {
    // 实例化 Solution 类
    Solution solution;

    // 定义各种测试用例
    std::vector<std::vector<int>> test_cases = {
        {2, 3, -2, 4},       // 基本正数数组
        {-2, 0, -1},         // 包含零
        {-2, -3, -4},        // 全负数
        {1, 2, -1, 3, 4},    // 正负数交替
        {5},                 // 单个元素
        {0, 0, 0},           // 全零
        {-1, 2, 3, -1, 4},   // 多段负数
        {1, -1, -1, 1, -1},  // 包含1和-1
        {6, -3, -10, 0, 2}   // 综合测试
    };

    // 循环测试每个用例并打印结果
    for (const auto& nums : test_cases) {
        std::cout << "输入: [";
        for (size_t i = 0; i < nums.size(); ++i) {
            std::cout << nums[i] << (i == nums.size() - 1 ? "" : ", ");
        }
        std::cout << "]" << std::endl;

        int product = solution.maxProduct(nums);
        std::cout << "最大乘积: " << product << std::endl;
        std::cout << "--------------------" << std::endl;
    }

    return 0;
}