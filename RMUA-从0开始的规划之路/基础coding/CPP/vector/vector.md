# Vector

## 什么是vector?

vector 通常被翻译为向量，vector是一个封装了动态大小数组的顺序容器(Sequence Container)。跟其他任意类型的容器一样，它能够存放各种类型的对象。可以简单地认为，vector是一个能够存放任意类型的动态数组。

vector与array不同，array被称为c风格的数组，主要特点在于array在编译时便确定好了数组的大小，无法被更改。同时，内存通常在栈上分配，生命周期由其作用域决定。

而array与std::array也不相同，std::array是C++11中引入的C风格数组的类，它同样是固定大小的，但是提供了更好地接口，比如`size()`,`begin()`,`end()`等等，并且不会发生越界访问时未定义行为，而是抛出异常。同样地，内存通常在栈上分配，生命周期由其作用域决定。

## vector特性

1. 顺序特性
    顺序容器中的元素严格按照线性顺序排序，可以通过元素在序列中的位置来访问对应的元素。
2. 动态数组
    支持对序列中的任意元素进行快速直接访问，甚至可以通过指针进行该操作。提供了在序列末尾相对快速的添加/删除元素的操作
3. 能够感知内存分配器的(Allocator-aware)
    容器使用一个内存分配器对象来动态的处理它的存储需求。

## 基本函数

### 构造函数

```cpp
vector() // 创建一个空的向量
vector(int nSize) // 创建一个元素个数为nSize的向量
vector(int nSize, const t& t) // 创建一个元素个数为nSize的向量,且元素值均为t
vector(const vector&) //复制构造函数
vector(begin，end) // 复制[begin，end]区间内的另一个向量的元素到创建的向量中
```

### 增加函数

```cpp
void push_back(const T& x) //在向量的尾部增加一个元素x
iterator insert(iterator it,const T& x) // 向量中迭代器指向元素前添加一个元素x
iterator insert(iterator it,int n,const T& x) //向量中迭代器指向元素前添加n个相同的元素x
iterator insert(iterator it,const_iterator first,const_iterator last) // 向量中迭代器指向元素前插入另一个相同类型向量的[first,last)间的数据

```

### 删除函数

```cpp
iterator erase(iterator it) // 删除向量中迭代器指向元素
iterator erase(iterator first,iterator last) //删除向量中[first，last)中元素
void pop_back() //删除向量中最后一个元素
void clear() // 清空向量
```

### 遍历函数

```cpp
reference at(int pos) // 返回pos位置元素的引用
reference front() // 返回首元素的引用
reference back() // 返回尾元素的引用
inerator begin() //返回向量头指针，指向第一个元素
inerator end() //返回向量尾指针，指向最后一个元素的下一个位置
reverste_inerator rbegin() // 反向迭代器，指向最后一个元素
reverste_inerator rend() // 反向迭代器，指向第一个元素之前的位置
```

### 判断函数
```cpp
bool empty() //判断向量是否为空，若为空，则向量中无元素存在

```

### 大小函数
```cpp
int size() //返回向量中元素个数
int capacity() // 返回当前向量能容纳的最大元素值
int max_size() // 返回最大可允许的vector元素数量值

```

### 其他函数

```cpp
void swap(vector&) // 交换两个同类型的向量的数据
void assign(int n ,const T& t) // 设置向量中前n个元素的值为x
void assign(const_iterator first,const_iterator last) //向量中[first,last)中元素设置成当前向量元素

```

## 笔记

### Cpp中的数组

在Cpp中，数组拥有三种方式来创建
1. c风格的数组
```cpp
int array[100]; // 创建一个长度为100的数组，存储的数据类型为int
```
2. std::array()，在c++11中提供的一个仿c风格数组的类，在编译时分配固定的大小，但是提供了越界访问时抛出异常，以及一些成员函数
```cpp
std::array<int> array(10);
```
3. std::vector 

### 迭代器


