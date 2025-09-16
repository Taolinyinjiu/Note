#include <iostream>
#include <vector>

void PrintVector(const std::vector<int>& vec);

int main(void){
    // 利用五种方式构造vector
    // 1. 默认构造函数,构造数组为空，动态数组
    std::vector<int> vector_1;
    PrintVector(vector_1);
    // 2. 通过指定大小构造，构造指定大小的动态数组，元素值为默认值0
    std::vector<int> vector_2(10);
    PrintVector(vector_2);
    // 3. 通过指定大小和初始值构造，构造指定大小的动态数组，元素值为指定值
    std::vector<int> vector_3(10,5);
    PrintVector(vector_3);
    // 通过拷贝构造函数构造
    std::vector<int> vector_4(vector_3);
    PrintVector(vector_4);
    // 通过迭代器构造
    std::vector<int> vector_5(vector_3.begin()+5,vector_3.end());
    PrintVector(vector_5);
}

void PrintVector(const std::vector<int>& vec) {
    for (const int& val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}