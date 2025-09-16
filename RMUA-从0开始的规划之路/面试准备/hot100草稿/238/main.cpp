#include <iostream>
#include <vector>

class Solution {
public:
    std::vector<int>productExceptSelf(std::vector<int>& nums) {
        int n = nums.size();
        std::vector<int> result(n);

        // 第一次遍历，计算前缀，并存入result
        result[0] = 1;
        for(int index = 1;index < n;index++){
            result[index] = result[index - 1] * nums[index - 1];
        }
        // 第二次遍历，计算后缀，并乘入result
        int right = 1;
        for(int index = n - 1;index >= 0;index--){
            result[index] *= right;
            right *= nums[index];
        }
        return result;
    }
};

int main(void)
{
    Solution solution;
    std::vector<int> nums = {1, 2, 3, 4};
    std::vector<int> result = solution.productExceptSelf(nums);

    for (int num : result) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}