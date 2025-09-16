#include <iostream>
#include <vector>

void PrintVector(const std::vector<int>& vec) {
    for (const int& val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

int main(void){
    // init vector with 10 numbers, each number is 0
    std::vector<int> vec(10,0);
    // use push_back to add numbers to the end of vector
    std::cout << "vector size: " << vec.size() << std::endl;
    std::cout << "vector capacity: " << vec.capacity() << std::endl;
    vec.push_back(1);
    PrintVector(vec);
}