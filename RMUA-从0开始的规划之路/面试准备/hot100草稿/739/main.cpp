#include <iostream>
#include <vector>
#include <stack>


class Solution {
    public:
        std::vector<int> dailyTemperatures(std::vector<int>& temperatures) {
            // 首先得到队列长度
            int n = temperatures.size();
            // 创建一个结果数组并初始化为0
            std::vector<int> result(n, 0);      
            // 创建一个单调栈来存储索引
            std::stack<int> stack_index;
            // 遍历当前温度数组
            for(int index = 0; index < n ; index++){
                // 当栈不为空时，且当前温度大于栈顶索引温度时
                while(!stack_index.empty() && temperatures[index] > temperatures[stack_index.top()]){
                    // 
                    int top_index = stack_index.top();
                    // 
                    stack_index.pop();
                    // 
                    result[top_index] = index - top_index;
                }
                stack_index.push(index);
            
            }
            return result;
        }
};


int main() {
    Solution sol;
    std::vector<int> temperatures = {73, 74, 75, 71, 69, 72, 76, 73};
    std::vector<int> result = sol.dailyTemperatures(temperatures);

    for (int days : result) {
        std::cout << days << " ";
    }
    std::cout << std::endl;

    return 0;
}