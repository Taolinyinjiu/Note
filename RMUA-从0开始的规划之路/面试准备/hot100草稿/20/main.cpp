#include <iostream>
#include <stack>
#include <string>   

class Solution {
public:
    bool isValid(std::string s) {
        // 栈中应该存储 char 类型
        std::stack<char> string_stack;
        
        for (char ch : s) {
            // 如果是开括号，压入栈中
            if (ch == '(' || ch == '{' || ch == '[') {
                string_stack.push(ch);
            } 
            // 如果是闭括号
            else {
                // 关键修正 1: 必须先检查栈是否为空
                if (string_stack.empty()) {
                    return false; // 遇到闭括号但栈是空的，无效
                }

                char topChar = string_stack.top();
                
                // 关键修正 2: 使用明确的条件判断来匹配括号
                if ((ch == ')' && topChar == '(') ||
                    (ch == '}' && topChar == '{') ||
                    (ch == ']' && topChar == '[')) {
                    // 匹配成功，弹出栈顶的开括号
                    string_stack.pop();
                } else {
                    // 栈顶的开括号与当前闭括号不匹配，无效
                    return false;
                }
            }
        }

        // 循环结束后，如果栈为空则说明所有括号都匹配了
        return string_stack.empty();
    }
};
