#include<iostream>
// #include<iterator>
#include<vector>

int main(void){
    std::vector<int> vec{1,2,3,4,5};;
    // for(auto it = vec.begin(); it != vec.end(); ++it){
    //     std::cout << *it << std::endl;
    // }

    for(int num : vec){
        std::cout << num << std::endl;
    }   

}


