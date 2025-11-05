#include <iostream>
#include <vector>

void mini_cost(long long x, long long y, long long a, long long b, long long c);

int main(void){
    // 首先得到数据组数量t
    long t = 0;
    std::cin >> t;
    // 每组数据包含 x y a b c
    std::vector<long long> x(t), y(t), a(t), b(t), c(t);
    // 输入数据
    for(long i = 0; i < t; ++i){
        std::cin >> x[i] >> y[i] >> a[i] >> b[i] >> c[i];
    }
    // 处理数据
    for(long i = 0; i < t; ++i){
        // 轮询每一轮的最小花费
        mini_cost(x[i], y[i], a[i], b[i], c[i]);
    }
    return 0;
}   

void mini_cost(long long x, long long y, long long a, long long b, long long c)
{
    // 计算将 x y变为 0 0 的最小花费
    // a代表将 x或y任意一个增加或减少1的花费
    // b代表将 x和y同时增加或减少1的花费
    // c代表将 x和y反向增加1的花费,可以看出 c的作用等价于 b+2a
    
    // 分三类进行讨论，1，两者均小于0，2，两者均大于0，3，一正一负
    if(x < 0 && y < 0){
        // 两者均小于0
        x = -x;
        y = -y;
        if(a*2 <= b){
            // 说明单独操作更划算
            std::cout << 1LL*(x+y)*a << std::endl;
        }else{
            // 说明联合操作更划算
            if(x < y){
                std::cout << 1LL*x*b +  1LL*(y-x)*a << std::endl;
            }else{
                std::cout << 1LL*y*b +  1LL*(x-y)*a << std::endl;
            }
        }
    }else if(x > 0 && y > 0){
        // 两者均大于0
        if(a*2 <= b){
            // 说明单独操作更划算
            std::cout << 1LL*(x+y)*a << std::endl;
        }else{
            // 说明联合操作更划算
            if(x < y){
                std::cout << 1LL*x*b +  1LL*(y-x)*a << std::endl;
            }else{
                std::cout << 1LL*y*b +  1LL*(x-y)*a << std::endl;
            }
        }
    }else if(x == 0 && y == 0) 
    {
        // 两者均为0
        std::cout << 0 << std::endl;    
    }
    // 一正一负需要多思考
    else 
    {
        // 一正一负时，需要考虑反向券是否比单步券更加划算
        if(a*2 <= c){
            // 说明单独操作更划算
            std::cout << 1LL*(x>0?x:-x)*a +  1LL*(y>0?y:-y)*a << std::endl;
        }else{
            // 说明反向操作更划算
            if(x > 0){
                // x为正
                if(x > -y){
                    // x的绝对值更大
                    std::cout << 1LL*-y*c +  1LL*(x+y)*a << std::endl;
                }else{
                    // y的绝对值更大
                    std::cout << 1LL*x*c +  1LL*(-y-x)*a << std::endl;   
                }
            }
            else{
                // y为正
                if(-x < y){
                    // y的绝对值更大
                    std::cout << 1LL*-x*c +  1LL*(y+x)*a << std::endl;
                }else{
                    // x的绝对值更大
                    std::cout << 1LL*y*c +  1LL*(-x-y)*a << std::endl;   
                }
            }
            
        }
    }
}