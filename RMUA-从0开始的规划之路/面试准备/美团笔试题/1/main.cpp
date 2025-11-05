#include <functional>
#include <iostream>
#include <type_traits>
#include <vector>
using namespace std;

void function_answer(int x, int m, const std::vector<int>& a_input);

// 给定长度为n的输入数组 a_i 和一个整数m，回答q次询问，每次询问给定一个x
// 初始化 a = 0 b = 0 c = 0 
// 遍历输入序列，每次遍历将a_i 累加到a  b  c中任意一个值上
// 保证a b c至少要被累加一次

// 输入的a_i 是固定的3 m和q不为固定，q是每次询问时给出的x值，非负数，需要用cin读取

// 构造一元二次函数f = ax^2 + bx + c    
// 对于每次询问，输出最大的f(x) mod m 

int main(void){
    // 得到输入的n m q
    int n = 0, m = 0, q = 0;
    cin >> n >> m >> q;
    // 读取输入序列     
    std::vector<int> a_input(n);
    for(int i = 0; i < n; i++){
        cin >> a_input[i];
    }
    // 读取询问时输入的x
    std::vector<int> query_input(q);
    for(int i = 0; i < q; i++){
        cin >> query_input[i];
    }
    for(int i = 0; i < q; i++)
        function_answer(query_input[i], m, a_input);
    cout << endl; 
}

void function_answer(int x, int m, const std::vector<int>& a_input){
    // 定义一个lambda表达式，计算f(x) mod m
    auto f = [m](int a, int b, int c, int x) -> int {
        long long res = (1LL * a * x % m * x % m + 1LL * b * x % m + c) % m;
        return static_cast<int>(res);
    };

    int n = a_input.size();
    int max_value = -1;

    // 三重循环，枚举a b c的所有可能分配
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            if(j == i) continue;
            for(int k = 0; k < n; k++){
                if(k == i || k == j) continue;
                int a = a_input[i];
                int b = a_input[j];
                int c = a_input[k];
                int current_value = f(a, b, c, x);
                if(current_value > max_value){
                    max_value = current_value;
                }
            }
        }
    }

    cout << max_value << " ";
}