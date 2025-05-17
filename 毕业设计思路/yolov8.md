# YOLO V8 Model Return Analyse

当我们在使用YOLO时，我们总是会好奇，它到底返回了些什么数据呢？

通常，YOLO会返回一个包含检测到物体信息的列表或者时类似的数据结构，这个返回类型会因为使用的YOLO的版本以及具体的实现库不同而不同，但核心信息通常包含有：
- 边界框 Bounding Box
- 置信度 Confidence Score or Objectness Score
- 类别标签 Class Label
- 类别概率 Class Probabilities 

总的来说，当我们传入一张图像给YOLO模型后，会得到一个列表，列表中的每个元素对应一个检测到的物体，每个元素会包含这个物体的边界框坐标，置信度分数，以及识别出的类别标签
