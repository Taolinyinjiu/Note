#include <iostream>
#include <vector>
#include <numeric> // 用于 std::accumulate

// 1. 分割数组的函数（与之前相同）
std::vector<std::vector<int>> splitArray(const std::vector<int>& nums) {
    std::vector<std::vector<int>> result;
    std::vector<int> current_segment;
    
    for (int num : nums) {
        if (num > 0) {
            current_segment.push_back(num);
        } else {
            if (!current_segment.empty()) {
                result.push_back(current_segment);
                current_segment.clear();
            }
        }
    }
    
    if (!current_segment.empty()) {
        result.push_back(current_segment);
    }
    
    return result;
}

// 2. 获取每个片段的乘积
void getSegmentProducts(const std::vector<std::vector<int>>& segments) {
    std::cout << "---" << std::endl;
    std::cout << "每个片段的元素乘积：" << std::endl;
    
    // 遍历每一个片段
    for (size_t i = 0; i < segments.size(); ++i) {
        const auto& segment = segments[i]; // 获取当前片段
        
        // 确保片段不为空
        if (segment.empty()) {
            continue;
        }

        // 使用 for 循环计算乘积
        long long product = 1;
        for (int num : segment) {
            product *= num;
        }

        // 使用 std::accumulate 计算乘积（更简洁的方式）
        // long long product = std::accumulate(segment.begin(), segment.end(), 1LL, std::multiplies<long long>());

        std::cout << "第 " << i + 1 << " 个片段 { ";
        for (int num : segment) {
            std::cout << num << " ";
        }
        std::cout << "} 的乘积是: " << product << std::endl;
    }
}

// 主函数用于测试
int main() {
    std::vector<int> nums = {1, 2, -1, 3, 4, 5, 0, 6, -2, 7};
    
    // 分割数组
    std::vector<std::vector<int>> segments = splitArray(nums);
    
    // 打印原始数组和分割后的片段
    std::cout << "原始数组: ";
    for (int num : nums) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    std::cout << "分割出的片段: " << std::endl;
    for (const auto& segment : segments) {
        std::cout << "{ ";
        for (int num : segment) {
            std::cout << num << " ";
        }
        std::cout << "}" << std::endl;
    }
    
    // 计算并打印每个片段的乘积
    getSegmentProducts(segments);
    
    return 0;
}