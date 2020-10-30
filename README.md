

<p align="center">
  <img width="50" src="img/wave.jpg">
</p>
<h1 align="center"> SWMM 断面参数提取程序 </h1>
<p align="center">
  <b >2020.10.29 目前仅支持圆管、矩形断面及非规则断面的参数计算</b>
  <br>
  <b >作者: torch</b>
  <br>
  <b > 邮箱: 947993284@qq.com</b>
</p>


## 描述

---

- 本程序可以识别SWMM模型中的inp文件，并将其中的**圆管**、**矩形断面**及**非规则断面**数据提取出来。

- 本程序可以计算**某个断面**在**指定水深**下的：

  > **平均水深**
  >
  > **水面宽度**
  >
  > **过水面积**
  >
  > **湿周**

* 本程序可以计算现状工况及设计工况下的**断面湿周率**。

---

## 使用方法

---

### 1. 我要提取INP中的断面

***

打开***main.py***:

```python
1 		from input_section import InpSection
2 		import pandas as pd
3 		from deal_data import deal
4 
5 
6 		sections = InpSection(path='data/XiaoXiHe.inp')  # 实例化断面形态
7 		raw_dict = pd.read_excel('data/XiaoXiHe-link.xlsx', None)  # 获取原始数据
8 		for key in raw_dict:
9 			raw_dict[key] = raw_dict[key].to_dict('list')
10
11
12		if __name__ == '__main__':
13			# 计算现状下断面形态参数
14			raw_result, raw_log = deal(sections=sections, excel_data=raw_dict['Sheet1'])
15
16			# 计算设计工况下断面形态参数
17			design_result, design_log = deal(sections=sections, excel_data=raw_dict['Sheet2'])
18
19			# 计算湿周率
20			wet_circle = []
21			for i in range(len(raw_result['湿周'])):
22				try:
23					wet_circle.append(raw_result['湿周'][i]/design_result['湿周'][i])
24				except ZeroDivisionError:
25					wet_circle.append(0)
26			raw_result['湿周率'] = wet_circle
27
28			# 输出结果
29			result_df = pd.DataFrame(raw_result)
30			for i in raw_log:
31				print(i)
32			result_df.to_excel('result/result.xlsx', index=False)
33			print('导出结果成功！')
34
```



其中第**6行为INP文件路径**，断点打在**第七行**，对程序进行***DEBUG***:

![图1.1](C:\Users\torch\Desktop\swmm_section\img\section_debug.png)



这样在***sections***对象的***sections***属性中，我们获得了**所有断面的信息**，每个断面数据以**断面名称**作为***key***，***value***包含***data***和***type***两部分，其中***type***的类型目前仅支持三种：

* 圆管:  ***data***为管道直径，***m***; ***type***为'***circle***'.

* 矩形断面: 

```python
data = {"width": float, "height": float}
```

​          矩形断面的***type***为'***rectangle***'

* 非规则断面: 

```python
data = {[0, 1, 2, 3, 4], [5, 4, 3, 4, 5]}
```

​		其中***data***中第一个**列表**表示起点距，第二个**列表**表示高程.

​		非规则断面的***type***为'***irregular***'.



### 2. 我要计算指定水深下的断面参数

---

本程序设计了**断面计算类**，内置了计算断面**平均水深**、**水面宽度**、**湿周**及**过水断面面积**的方法.

由于实例化断面是为了计算以上参数，因此在实例化断面的时候需要**指定水深**，***m***;

**实例化断面方法**：

```python
1		from input_section import InpSection
2		from section_feature import SectionFeature
4
5		sections = InpSection(path='data/XiaoXiHe.inp')  # 实例化断面形态
6		section = sections.sections['这里输入您要计算的断面名称']
7		section_feature = SectionFeature(data=section, depth='这里输入您指定的水深')
8
```

**计算断面的平均水深：**

```python
1		avg_water_depth = section_feature.avg_water_depth()
```

**计算断面的水面宽度：**

```python
1		water_width = section_feature.water_width()
```

**计算断面的过水面积：**

```python
1		water_area = section_feature.section_area()
```

**计算断面的湿周:**

```python
1		wet_length = section_feature.wet_circle()
```

如果您需要**遍历所有断面**并为不同断面分别指定水深，这里提供了一个**遍历断面的方法**：

```python
1		from input_section import InpSection
2		from section_feature import SectionFeature
4
5		sections = InpSection(path='data/XiaoXiHe.inp')  # 实例化断面形态
6		for section in sections:
7			# 这里的section就是所有断面其中之一，数据结构为{"data": XX, "type": "circle or rectangle or irregular"}
```



### 3. 我要计算湿周率

---

对于湿周率的计算，请参考源码中的***main.py***文件.



---

## 更新日志 2020.10.29

---

+ 修复了匹配不到断面程序终止运行的BUG.
+ 修复了断面数据除以0程序终止运行的BUG.
+ 修复了对于非规则断面程序无法匹配到所有起点距-高程数据的BUG.
+ 更正了过水断面面积计算算法的错误.