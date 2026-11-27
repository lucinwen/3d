# 第十八讲：Data Cleaning & Deduplication
## 三维数据清洗、异常检测、几何去重、近重复检测与数据筛选

> 课程 3：3D 数据生产与质量管理  
> 状态：教学稿已归档；小测与实践尚未验收。  
> 本讲定位：腾讯混元 3D AI Data 专项。  
> 归档说明：本文件是本讲结构化教学稿；聊天中展示的图片查询不等于原始图片二进制文件，图片主题另列于文末。

## 学习目标

建立一套可扩展、可追溯、可回滚的 3D 数据清洗与去重系统。掌握文件级、几何级、拓扑级、点云级、外观级和语义级异常检测；掌握 SHA256、Canonicalization、Geometry Fingerprint、Chamfer、ICP、ANN、Duplicate Graph；理解 Precision/Recall、阈值校准、非破坏性清洗和百万级 Pipeline。

## 1. 概念

### 1.1 Data Cleaning
数据清洗是识别原始数据中的错误、异常、不一致、缺失和无效信息，并按数据用途进行修复、标准化、隔离或剔除。对象包括几何、拓扑、坐标、尺度、法线、材质、UV、纹理、语义标签、元数据和来源。

### 1.2 Data Deduplication
数据去重是识别重复或高度相似样本，并控制重复数据对训练和评测的影响。

三类重复：
- Exact Duplicate：字节内容完全一致。
- Geometric Duplicate：几何相同或近似，但格式、顶点顺序、网格密度或导出方式不同。
- Semantic Near-duplicate：设计/语义高度相似但仍有真实几何差异。

几何相似不等于应该删除。高模/低模、不同材质版本和不同设计变体可能都具有任务价值。

### 1.3 Outlier
异常样本可以是几何、统计、语义、尺度或质量异常。异常候选不等于坏数据；需要结合类别、来源和任务判断。

### 1.4 Cleaning vs Filtering
- Cleaning：修复和处理数据问题。
- Filtering：按类别、质量、用途选择目标子集。

### 1.5 四种处置策略
- Pass：直接通过。
- Repair：修复后重新验证。
- Review：低置信度交人工审核。
- Quarantine/Reject：隔离或拒收。

异常不意味着必须删除。开放曲面、多组件装配、特殊比例和有意重叠可能是合法结构。

## 2. 异常分类

### 2.1 Geometry Anomaly
- Invalid Coordinates：NaN、+Inf、-Inf。
- Degenerate Face：面积为零或接近零。
- Self-intersection：表面自相交。
- Missing Geometry：局部结构缺失。
- Scale Anomaly：单位或尺度异常。
- Floating/Disconnected Geometry：悬浮或意外断开的几何碎片。

三角形面积：
[
A=\frac12\|(v_2-v_1)\times(v_3-v_1)\|
]
若 A 接近 0，可能是退化面；阈值必须按单位、归一化尺度和精度校准。

### 2.2 Topology Anomaly
- Non-manifold Edge / Vertex。
- Duplicate Face。
- Inconsistent Winding。
- Boundary Edge。
- Isolated Vertex。
- Connected Components 异常。

闭合二流形三角网格的内部边通常由两个面共享；只被一个面使用的边通常是边界边。开放曲面可以合法存在边界。多组件也不必然是错误。

### 2.3 Point Cloud Anomaly
Outlier、Duplicate Points、Non-uniform Density、Missing Regions、Registration Artifacts、Background Contamination、Floating Clusters。

### 2.4 Appearance Anomaly
Missing Texture、Broken Material Reference、UV Stretching、UV Seam、Texture Corruption、Incorrect Color Space、Inconsistent Material Assignment。

### 2.5 Semantic Anomaly
类别错误、部件标签错误、文本与模型不匹配、材质描述错误、左右部件混淆、实例关系错误。需要结合规则、视觉/3D 模型和人工审核。

### 2.6 五层验证体系
1. File-level：能否读取、格式、依赖、损坏。
2. Geometry-level：坐标、面片面积、尺度、Bounding Box、自相交。
3. Topology-level：连通性、边界、非流形、重复面、法线/绕序。
4. Semantic-level：类别、部件、文本、材质、空间关系。
5. Task-level：是否符合具体训练目标。

## 3. 统计异常检测

### 3.1 Bounding Box
对顶点集合 V：
[
L_x=x_{max}-x_{min},\
L_y=y_{max}-y_{min},\
L_z=z_{max}-z_{min}
]
AABB 与坐标轴对齐；OBB 可旋转以贴近物体主方向。可以用尺寸和比例筛查异常，但不能仅凭 Bounding Box 删除样本。

### 3.2 Z-score
[
z_i=\frac{x_i-\mu}{\sigma}
]
例如 |z|>3 可标记异常候选。均值和标准差会受极端值影响。

### 3.3 MAD / Robust Z-score
[
m=Median(x),\
MAD=Median(|x_i-m|),\
z_{robust}=\frac{0.6745(x_i-m)}{MAD}
]
MAD 对极端值较稳健；MAD=0 时需考虑 IQR、类别分位数或专门规则。

### 3.4 IQR
[
IQR=Q_3-Q_1
]
常见候选区间：
[
x<Q_1-1.5IQR\quad\text{或}\quad x>Q_3+1.5IQR
]

### 3.5 多变量异常
Mahalanobis Distance：
[
D_M(x)=\sqrt{(x-\mu)^T\Sigma^{-1}(x-\mu)}
]
考虑特征间相关性，但高维协方差估计和非椭球分布可能带来问题。

Isolation Forest：异常点通常更容易被随机切分隔离。可用面数、顶点数、尺寸、体积、表面积和几何描述子。

LOF：比较样本与局部邻居的密度差异，适合发现局部异常。以上方法只发现特征空间异常，不理解语义是否合理。

## 4. 几何去重

### 4.1 第一层：File Hash
[
h_i=SHA256(file_i)
]
相同哈希意味着字节内容完全一致。无法发现格式转换、顶点重排、重新导出或几何相同但文件不同的情况。

### 4.2 第二层：Canonicalization
中心化：
[
c=\frac1N\sum_i v_i,\quad v_i'=v_i-c
]
尺度归一化：
[
s=max(L_x,L_y,L_z),\quad v_i''=v_i'/s
]
方向统一可用已知姿态、PCA 主轴、特征配准或旋转不变描述子。PCA 对称物体可能主轴不稳定或有符号歧义，不能保证唯一姿态。再使用统一表面采样（Area-weighted、Poisson-disk、Farthest Point Sampling），避免原始顶点分布偏差。

### 4.3 第三层：Geometry Fingerprint
可组合：
- Bounding Box：尺寸、比例、主方向、OBB。
- Surface Area / Volume / A/V（开放曲面体积可能无定义）。
- D2 Distance Histogram。
- FPFH、SHOT 等局部描述子。
- Learned Embeddings。

不同描述子有不同适用场景，不能视为完全等价。

### 4.4 第四层：Chamfer Distance
[
CD(P,Q)=\frac1N\sum_{p\in P}\min_{q\in Q}\|p-q\|^2+
\frac1M\sum_{q\in Q}\min_{p\in P}\|q-p\|^2
]
CD 适合几何相似性比较，但不能单独决定删除；相似设计可能有很低 CD。

### 4.5 第五层：ICP Alignment
[
P'=RP+t
]
先对齐再计算 CD。ICP 对初始值敏感，可能受对称结构、重复部件和大差异影响，不能保证全局最优。

### 4.6 第六层：Multi-view Render Similarity
渲染 Front、Back、Left、Right、Top、Perspective 等视图，使用 pHash、SSIM、LPIPS、CLIP Embedding 辅助召回。受相机、材质、光照、遮挡影响，不能单独作为几何重复最终判据。

### 4.7 完整六层架构
1. File Hash。
2. Canonicalization。
3. Geometry Fingerprint。
4. Candidate Retrieval。
5. Fine-grained Geometry Matching。
6. Duplicate Decision。

Candidate Retrieval 与 Final Verification 必须区分：前者尽量召回候选，后者减少误删。

## 5. 近重复检测与判定

### 5.1 阈值
[
D(A,B)=CD(P_A,P_B),\
D(A,B)<\tau
]
可标记为相似候选。没有适用于所有类别的固定阈值。需按归一化方法、采样、平方/非平方距离、类别、任务和人工标签校准。

### 5.2 Precision / Recall
[
Precision=\frac{TP}{TP+FP},\
Recall=\frac{TP}{TP+FN},\
F1=2\frac{Precision\cdot Recall}{Precision+Recall}
]
Precision 低会误删有效设计；Recall 低会漏掉重复。还应关注类别级 Precision/Recall、稀有样本误删率、人工审核成本和有效数据保留率。

### 5.3 Duplicate Graph
[
G=(V,E)
]
节点是模型，边表示重复或近重复关系。可用 Connected Components、Union-Find 或 Clustering 组织资产家族。

相似关系不一定传递：A~B、B~C 不保证 A~C。高风险删除需进行组内成对验证、代表样本比较、Complete-linkage 等约束或人工审核。

### 5.4 重复组保留策略
不要默认每组只留一个文件。原始扫描、高模、低模、带 UV 版本、带材质 GLB 可能对不同任务有价值。建立 Asset Family，保留派生关系，按任务选择合适版本。

### 5.5 ANN
百万规模两两比较需要约 N(N-1)/2 次比较，成本过高。将模型编码为向量 z∈R^d，使用 FAISS、HNSW、ScaNN、Annoy 等进行 Top-K 候选召回，再做精确几何验证。ANN 近邻不是重复事实。

## 6. 清洗策略与非破坏性处理

### 6.1 自动修复候选
- NaN/Inf：删除或隔离关联数据，不盲目补坐标。
- Duplicate Vertices：Merge Vertices，注意 UV、法线和材质边界。
- Duplicate Faces：Remove Duplicate Faces，确认非有意重叠。
- Degenerate Faces：删除并检查局部损伤。
- Inconsistent Normals：重算法线，开放表面需方向参考。
- Isolated Vertices：清理未引用顶点，确认特殊属性用途。
- Point Cloud Outliers：统计/半径过滤，避免误删细长结构。
- Noise：平滑或去噪，注意细节损失。

几何位置相同的顶点不一定属性相同；UV、法线、材质边界可能要求保留分裂顶点。

### 6.2 Non-destructive Cleaning
保留 Raw、Staging、Processed、Approved、Quarantine。每次处理记录：
- 原始文件和哈希。
- 处理版本与参数。
- 检测问题。
- 实际执行操作。
- 修复前后指标。
- 删除/修改元素。
- 人工审核。
- 回滚信息。

不要覆盖原始数据。

## 7. 工程实现

环境：
```bash
pip install numpy scipy trimesh open3d scikit-learn
```

### 7.1 扫描文件
```python
from pathlib import Path
ROOT = Path("data/raw")
SUPPORTED = {".obj", ".ply", ".stl", ".glb", ".gltf"}
files = [p for p in ROOT.rglob("*")
         if p.is_file() and p.suffix.lower() in SUPPORTED]
print("Total assets:", len(files))
```
实际工程应按 Asset Manifest 管理多文件资产；OBJ 可能依赖 MTL/纹理，GLB 可能包含多个 Mesh。

### 7.2 SHA256
```python
import hashlib
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def find_exact_duplicates(files):
    seen, duplicates = {}, []
    for path in files:
        digest = sha256_file(path)
        if digest in seen:
            duplicates.append({
                "duplicate": str(path),
                "original": seen[digest],
                "hash": digest
            })
        else:
            seen[digest] = str(path)
    return duplicates
```

### 7.3 Mesh 基础检查
```python
import trimesh
import numpy as np

def inspect_mesh(path):
    mesh = trimesh.load(path, force="mesh", process=False)
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces)
    return {
        "path": str(path),
        "is_empty": mesh.is_empty,
        "vertex_count": len(vertices),
        "face_count": len(faces),
        "finite_vertices": bool(np.isfinite(vertices).all()),
        "bounds": mesh.bounds.tolist() if len(vertices) else None,
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent)
    }
```
process=False 用于尽量保留输入状态以供原始检测；读取阶段自动修复会改变证据。

### 7.4 退化面与重复面
```python
import numpy as np

def triangle_areas(vertices, faces):
    tri = vertices[faces]
    a = tri[:, 1] - tri[:, 0]
    b = tri[:, 2] - tri[:, 0]
    return 0.5 * np.linalg.norm(np.cross(a, b), axis=1)

def inspect_faces(vertices, faces, area_eps=1e-12):
    areas = triangle_areas(vertices, faces)
    degenerate = areas < area_eps
    canonical = np.sort(faces, axis=1)
    unique = np.unique(canonical, axis=0)
    return {
        "degenerate_face_count": int(degenerate.sum()),
        "duplicate_face_count": int(len(faces) - len(unique)),
        "min_area": float(areas.min()) if len(areas) else None
    }
```
area_eps 是示例阈值，需根据单位、尺度、数值精度校准。

### 7.5 非破坏性基础修复示例
```python
import trimesh

def clean_mesh_copy(source_path, output_path):
    mesh = trimesh.load(source_path, force="mesh", process=False)
    if mesh.is_empty:
        raise ValueError("Empty mesh")
    before = {"vertices": len(mesh.vertices), "faces": len(mesh.faces)}
    cleaned = mesh.copy()
    cleaned.process(validate=False)
    cleaned.process(validate=True)
    after = {"vertices": len(cleaned.vertices), "faces": len(cleaned.faces)}
    cleaned.export(output_path)
    return {"before": before, "after": after}
```
这只是基础网格处理，不保证修复所有自相交、非流形、语义组件、UV 和纹理问题。必须对比修复前后结果。

### 7.6 Open3D 点云清洗
```python
import open3d as o3d
pcd = o3d.io.read_point_cloud("data/raw/scan.ply")
down = pcd.voxel_down_sample(voxel_size=0.005)
cleaned, indices = down.remove_statistical_outlier(
    nb_neighbors=20, std_ratio=2.0
)
outliers = down.select_by_index(indices, invert=True)
print(len(pcd.points), len(cleaned.points), len(outliers.points))
```
参数依赖单位和采样密度；需要检查是否误删细长结构。

### 7.7 简单几何指纹（仅候选检索）
```python
import numpy as np
import trimesh

def geometry_fingerprint(path):
    mesh = trimesh.load(path, force="mesh")
    if mesh.is_empty:
        raise ValueError("Empty mesh")
    vertices = np.asarray(mesh.vertices)
    vertices = vertices - vertices.mean(axis=0)
    scale = np.max(np.ptp(vertices, axis=0))
    if scale <= 1e-12:
        raise ValueError("Degenerate geometry")
    vertices = vertices / scale
    normalized = trimesh.Trimesh(
        vertices=vertices, faces=mesh.faces, process=False
    )
    points, _ = trimesh.sample.sample_surface(normalized, 2048)
    bbox = np.sort(np.ptp(vertices, axis=0))
    radial = np.linalg.norm(points, axis=1)
    hist, _ = np.histogram(radial, bins=32, range=(0, 1.5), density=True)
    return np.concatenate([bbox, hist])
```
该指纹没有消除任意旋转；径向直方图会丢失方向和局部结构信息，只能用于粗筛，不可作为最终重复判据。

### 7.8 FAISS 候选检索
```python
import faiss
import numpy as np
fingerprints = np.asarray(fingerprints, dtype=np.float32)
index = faiss.IndexFlatL2(fingerprints.shape[1])
index.add(fingerprints)
distances, indices = index.search(fingerprints[:1], 10)
```
IndexFlatL2 是精确向量搜索，不是 ANN；百万规模可按召回、内存和延迟需求考虑 IVF/HNSW 等索引。向量近邻仍需几何验证。

### 7.9 清洗报告
每个资产记录 asset_id、original_hash、pipeline_version、processing_config、detected_issues、repair_operations、before_metrics、after_metrics、decision、reviewer、日志、规则版本和修复后哈希。参数配置不等于实际执行成功，必须记录实际处理数量。

## 8. 评价指标

- Parsing Success Rate。
- Invalid Geometry Rate。
- Non-manifold Rate。
- Repair Success Rate。
- False Rejection Rate。
- Retention Rate。
- Duplicate Rate。
- Review Rate。
- Processing Throughput。
- Duplicate Precision / Recall / F1。
- Candidate Recall@K。
- False Positive Rate。
- 稀有类别误删率。
- 人工审核成本。

阈值校准必须使用人工标注的正负样本对，并按类别和任务分层。不要把教学示例阈值直接用于生产。

## 9. 百万级系统设计

数据规模示例：100 万资产、平均 20 MB，原始数据约 20 TB（不含中间文件、渲染和版本）。

架构：
1. Raw Asset Storage：原始文件不可覆盖。
2. Parallel Ingestion：解析、元数据、依赖检查。
3. File Hash：精确去重。
4. Geometry QA / Topology QA。
5. Canonicalization / Fingerprinting。
6. ANN Candidate Retrieval。
7. Geometric Verification / Duplicate Graph。
8. Repair / Review / Reject。
9. Approved Dataset + Cleaning Report。

工程组件：
- Task Queue：任务拆分。
- Worker Pool：并行处理。
- Object Storage：存原始与处理文件。
- Metadata Database：存索引和报告。
- Retry：失败重试，超限隔离。
- Idempotency：同一资产、处理版本和配置不重复产生不可控写入。

示例 Job ID：
[
JobID=Hash(AssetID+PipelineVersion+Config)
]

三级筛选：
- Stage 1 低成本：Hash、解析、面数、Bounding Box、非法坐标。
- Stage 2 中成本：指纹、统计特征、ANN。
- Stage 3 高成本：ICP、Chamfer、局部几何、多视角渲染、人工审核。

## 10. 面试问题与参考答案

### Q1：3D Data Cleaning 包含什么？
从文件、几何、拓扑、外观、语义和任务适用性分层检查；按问题类型通过、修复、审核或拒收。

### Q2：为什么 SHA256 不能完成几何去重？
SHA256 比较字节内容，无法识别格式转换、顶点重排、重新导出或几何相同但文件不同的情况。

### Q3：如何进行几何近重复检测？
统一坐标/尺度和采样；提取指纹或 Embedding；ANN 召回候选；ICP 对齐；Chamfer、Hausdorff 和局部特征验证；再结合语义和来源判断。

### Q4：为什么需要 Precision 和 Recall？
Precision 低会误删有效设计；Recall 低会漏掉重复。通过标注验证集校准阈值，并按类别、用途和误删成本制定策略。

### Q5：为什么不能把所有异常删除？
开放曲面、多组件装配、特殊比例和有意重叠可能合法；需要结合任务判定。

### Q6：如何设计百万级去重？
文件哈希 → 几何标准化和指纹 → ANN 候选召回 → ICP/Chamfer/局部几何验证 → 重复关系图 → 按任务保留资产家族。

### Q7：如何证明清洗有效？
比较解析率、异常率、重复率、类别分布、多样性和人工审核结果；用固定测试集验证模型效果。不能只看清洗率。

### Q8：如何接入 Agent？
将解析、检测、召回、匹配、修复、验收封装为工具；Agent 规划并编排，处理重试、策略切换和人工介入；保存版本、哈希和报告。

### 高阶追问
1. CD 很低但设计不同，怎样识别？检查局部结构、部件数量、语义、视角轮廓和关键特征。
2. Recall 高而 Precision 低，怎样改进？提高精细验证、引入局部几何和语义约束、类别阈值、困难负样本和人工审核。
3. 如何防止误删稀有资产？类别分层、长尾标记、保留资产家族和人工审核。
4. 清洗后指标提高但生成质量下降，如何分析？检查过度清洗、长尾损失、分布变化、合成比例、类别平衡；通过版本回滚和分层消融实验定位。

## 11. 小测

基础题：
1. SHA256 能识别什么？
2. 为什么需要 Canonicalization？
3. 退化三角面面积公式？
4. MAD 为什么稳健？
5. ICP 解决什么问题？
6. CD 低能否证明完全重复？
7. ANN 的作用？
8. Precision 低意味着什么？
9. 为什么不能删除所有异常？
10. 为什么百万级去重需要多阶段检索？

高阶题：
1. 设计百万级 3D Mesh 去重系统，识别文件重复、不同格式、旋转缩放后的相同模型和相似但不应删除的模型。
2. 对含非流形边、退化面、重复顶点、UV 接缝和多组件的 Mesh 设计非破坏性清洗策略。
3. Recall 98%、Precision 70%，且训练多样性下降，分析原因并设计实验。

评分建议：异常检测 20%，几何去重 25%，统计评价 20%，工程系统 20%，数据治理与长尾保护 15%。完成测验与实践后才能标记 mastered。

## 参考资料

- Open3D：Point Cloud Outlier Removal. https://www.open3d.org/html/tutorial/geometry/pointcloud_outlier_removal.html
- Open3D：Point Cloud / Voxel Downsampling. https://www.open3d.org/docs/latest/tutorial/t_geometry/pointcloud.html
- Trimesh：Mesh Processing and Validation. https://trimesh.org/
- FAISS：Similarity Search and Clustering of Dense Vectors. https://faiss.ai/
- PointNet++. https://arxiv.org/abs/1706.02413
- DGCNN. https://arxiv.org/abs/1801.07829

## 图片恢复清单

聊天中的图片查询/示意图不是原始二进制图片备份。恢复原图时逐一核验：
1. 3D mesh corrupted geometry / holes / non-manifold / self-intersection。
2. Exact duplicate 3D models。
3. Geometric near-duplicate high/low poly models。
4. Semantic near-duplicate chair variants。
5. Bounding Box AABB/OBB。
6. Z-score/MAD/IQR/Isolation Forest/LOF diagrams。
7. Geometry fingerprint and shape descriptors。
8. ICP alignment before/after。
9. Chamfer nearest-neighbor correspondences。
10. Multi-view render similarity.
11. Duplicate Graph / asset family.
12. ANN candidate retrieval.
13. Non-destructive cleaning stages.
14. Million-scale cleaning pipeline.
15. Precision/Recall and threshold calibration visualizations.
