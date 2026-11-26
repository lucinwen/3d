# 第 1 讲：Mesh、Geometry、Topology

## 1. 概念

Geometry 描述形状与空间属性；Topology 描述连接关系；Mesh 是用离散顶点、边、面表达表面的数据结构。三者相关但不等价。两个模型可以几何外形相近，却具有完全不同的拓扑。

## 2. 原理

最常见的 Polygon Mesh 由：
- Vertex：顶点位置及可选属性。
- Edge：顶点之间的连接。
- Face：由有序边界围成的面。
- Normal：表面方向。
- Attribute：颜色、UV、权重等。

Indexed Mesh 通常用顶点数组和索引数组表示。顶点可复用，面索引指向顶点数组。三角面常表示为三个索引。

拓扑关键概念：
- Manifold：局部邻域类似平面或半平面的流形结构。
- Boundary Edge：只连接一个面的边。
- Non-manifold Edge：连接面数或局部结构不符合流形要求。
- Degenerate Face：面积接近零的退化面。
- Isolated Vertex：没有连接边的孤立顶点。
- Self-intersection：表面与自身相交。
- Normal Orientation：法线方向一致性。

注意：开放边界对薄片、衣服单层面可能是设计允许的；不能把所有 Boundary Edge 都判为错误。质量判断必须结合资产用途。

## 3. 数据结构

示意：
```python
vertices = [(x0,y0,z0), ...]
faces = [(0,1,2), (0,2,3), ...]
```
实际格式还可能包含 UV corner attributes、材质槽、顶点组、骨骼权重和多层法线。

Half-edge 结构通过有向半边记录 next、twin、face、vertex 等关系，便于邻接遍历、边折叠和拓扑操作。

## 4. 算法

常见检查：
1. 遍历顶点/边/面数量与边界范围。
2. 计算面面积，识别退化面。
3. 统计边连接面数量，检测非流形边。
4. 检查孤立顶点和重复顶点。
5. 使用 BVH/空间索引做三角形相交检测。
6. 检查法线一致性和组件连通性。

Chamfer Distance 衡量点集几何接近程度，不衡量拓扑是否适合动画。几何准确与拓扑可用必须分开验收。

## 5. 工程实现

Blender Python 可用 bmesh 检查基础拓扑：
```python
import bpy, bmesh
obj = bpy.context.active_object
bm = bmesh.new()
bm.from_mesh(obj.data)
bm.normal_update()
report = {
  "vertices": len(bm.verts),
  "edges": len(bm.edges),
  "faces": len(bm.faces),
  "boundary_edges": sum(e.is_boundary for e in bm.edges),
  "non_manifold_edges": sum(not e.is_manifold for e in bm.edges),
  "degenerate_faces": sum(f.calc_area() < 1e-10 for f in bm.faces)
}
bm.free()
print(report)
```
此示例检查当前活动 Mesh；阈值需按模型单位和尺度调整。复杂自相交检测需要额外空间结构和三角形相交算法。

## 6. 评价指标

- Vertex/Face Count：规模与预算，不代表质量本身。
- Non-manifold Count：非流形边数量。
- Degenerate Face Count：退化面数量。
- Boundary Edge Count：开放边界数量，需结合用途。
- Connected Components：连通组件数。
- Chamfer Distance：几何差异，需统一坐标、尺度和采样协议。
- Hausdorff Distance：最坏局部偏差，对离群点敏感。

## 7. 实际案例

AI 生成角色正面渲染漂亮，但肘部拓扑没有合理边流，弯曲时发生塌陷。问题不是单纯“模型不好看”，而是拓扑不满足目标动画用途。应先定义动作测试，再检查关节周围边流、权重和变形。

## 8. 面试追问

- Geometry 和 Topology 的区别？
- 为什么两个外形相同的 Mesh 可能具有不同生产价值？
- Non-manifold 一定是错误吗？
- Chamfer Distance 能否证明拓扑合格？为什么？
- 如何用 Blender Python 批量检测 3D 资产？

回答要点：用途先行；几何、拓扑、动画可用性分层；指标不能越权解释。

## 9. 小测

1. Mesh 的基本组成是什么？
2. Boundary Edge 与 Non-manifold Edge 有何区别？
3. 为什么退化面会影响后续处理？
4. Half-edge 相比简单索引结构有什么优势？
5. 为什么 Chamfer Distance 不能替代拓扑检查？

开放题：设计一个面向可动画角色的 Mesh 自动检查器，列出输入、规则、报告字段和人工复核边界。
