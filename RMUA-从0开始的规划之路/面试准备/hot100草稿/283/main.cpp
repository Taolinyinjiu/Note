#include <vector>

class Solution{
    public:
        void moveZeroes(std::vector<int>& nums)
        {
            int stack_size = 0;
            for(int i = 0; i < nums.size(); ++i)
            {
                if(nums[i] != 0)
                {
                    nums[stack_size++] = nums[i];       
                }
            }
            for(int i = stack_size; i < nums.size(); ++i)
            {
                nums[i] = 0;
            }
        }
};