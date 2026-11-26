# 第 2 讲：UV 与纹理映射

## 1. 概念

UV Mapping 将三维表面映射到二维纹理坐标空间。U、V 是纹理平面坐标，不是世界坐标的 X、Y。UV 决定纹理如何贴到 Mesh 表面。

## 2. 原理

三维表面无法在不产生切缝、拉伸或重叠的条件下普遍无失真地展开到二维平面。需要选择 Seam，将表面切分为 UV Islands，再进行展开和 Packing。

UV 质量主要受：
- Stretching：面积或角度畸变。
- Overlap：非预期重叠。
- Texel Density：单位表面积对应的纹素密度。
- Padding：Island 间距，避免 Mipmap/过滤时串色。
- Resolution：纹理分辨率。
影响。

## 3. 数据结构

UV 通常是面角（Face Corner / Loop）属性，而不一定是每个几何顶点唯一一个 UV。一个几何顶点在 UV Seam 两侧可以对应不同 UV 坐标。

常见数据：
- UV Layer。
- UV Island。
- Face/Loop UV。
- Texture Image。
- UDIM Tile。
- Material Texture Binding。

## 4. 算法

典型流程：
1. 根据硬边、曲率、材质区或人工指定位置选择 Seam。
2. 展开 UV。
3. 计算角度/面积畸变。
4. 将 Islands 排布进 0–1 UV 空间或 UDIM。
5. 设置 Padding。
6. 检查重叠、拉伸和 Texel Density。
7. 烘焙纹理并检查接缝。

常见展开方法包括 Angle Based、Conformal 等；不同算法适合不同形状和目标。

## 5. 工程实现

Blender Python 可读取 UV：
```python
import bpy
obj = bpy.context.active_object
mesh = obj.data
if mesh.uv_layers:
    uv_layer = mesh.uv_layers.active
    print("UV layer:", uv_layer.name)
    for loop_uv in uv_layer.data:
        print(tuple(loop_uv.uv))
else:
    print("Missing UV")
```
注意 UV 数据按 loop 存储。重叠检测需要对 UV 三角形进行二维相交检测；拉伸检测需比较 3D 面与 UV 面的面积/角度关系。

## 6. 评价指标

- UV Coverage：UV 空间利用率。
- Stretch Metric：角度或面积畸变。
- Overlap Ratio：非预期重叠比例。
- Texel Density Variance：不同区域纹素密度差异。
- Padding：像素间距。
指标需区分允许重叠（镜像/重复部件）与错误重叠。

## 7. 实际案例

角色手臂与躯干 UV 密度差异过大，导致贴图细节不均；衣服接缝处出现串色，可能是 Padding 不足或 Mipmap 处理问题。不能仅凭 UV 岛数量判断质量。

## 8. 面试追问

- 为什么 UV 通常是 Loop/Face Corner 属性？
- UV Seam 与几何边界有什么区别？
- 如何检测 UV 拉伸？
- UV 重叠什么时候允许？
- Texel Density 为什么重要？

## 9. 小测

解释 UV Island、Seam、Padding、UDIM；设计批量 UV 检查报告，说明如何处理镜像重叠和多个材质集。
