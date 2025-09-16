class Solution {
public:
    int climbStairs(int n) {
        // 处理基础情况
        if (n <= 0) return 0;
        if (n == 1) return 1;
        if (n == 2) return 2;

        // a: 代表到达第 i-2 阶的方法数
        // b: 代表到达第 i-1 阶的方法数
        int a = 1; // ways(1)
        int b = 2; // ways(2)
        
        int current_ways;

        // 从第 3 阶开始循环，直到第 n 阶
        for (int i = 3; i <= n; ++i) {
            // 计算到达当前第 i 阶的方法数
            current_ways = a + b;
            
            // 更新 a 和 b，为下一次迭代做准备
            a = b;
            b = current_ways;
        }

        // 循环结束后，b 中存储的就是到达第 n 阶的方法数
        return b;
    }
};