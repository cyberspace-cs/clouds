# 🏆 Kaggle 打比赛完整攻略（中文版）

> 配合 `agentic-kaggle-skill` 使用。本文是 Kaggle 竞赛从入门到冲牌的实战路线图，综合了 Kaggle 官方文档、Grandmaster 经验帖（NVIDIA Playbook 等）与实战复盘。来源标注见文末。

---

## 一、先搞懂 Kaggle 比赛怎么运作

Kaggle 比赛的标准流程（官方）：

1. **加入比赛**：阅读赛题说明，接受规则，获得数据访问权
2. **动手**：下载数据，本地或 Kaggle Notebook（免费 GPU）构建模型，生成预测文件
3. **提交**：上传预测文件，获得分数
4. **看榜**：Public Leaderboard 实时显示，最终以 Private Leaderboard 定名次

### 比赛类型（重要，决定策略）

| 类型 | 特点 | 代表 |
| --- | --- | --- |
| Getting Started | 练手赛，无奖金积分，教程齐全 | Titanic、Digit Recognizer |
| Playground | 合成数据赛，量大速刷，适合练流程 | Playground Series S5/S6 |
| Featured / Research | 真实问题赛，奖金高竞争大 | 各行业真实数据 |
| Code Competition | **最终你的 Notebook 会被 Kaggle 在隐藏数据上重跑** | 需要"防御性编码" |

> **关键认知**：Code Competition 和普通预测文件赛的提交方式完全不同，策略必须调整。

---

## 二、新手起步路线（4 周）

**第 1 周：跑通基线**
- 从 Getting Started 赛开始（Titanic → Digit Recognizer → House Prices）
- 先做简单基线：Logistic Regression / Random Forest / XGBoost，**先提交成功一次**，体验全流程
- 搞清楚评估指标怎么算（分类看 Accuracy/AUC，回归看 RMSE/MAE）

**第 2 周：特征工程**
- 这是表格赛最大的提分点
- 读高分公开 Notebook，学特征工程、预处理、评估方法
- 逐步迭代：加特征 → 验证 → 记录

**第 3-4 周：模型多样 + 调参**
- 多模型并行：XGBoost + LightGBM + CatBoost + 神经网络
- 简单调参（随机森林的 n_estimators、max_depth；GBDT 的 learning_rate）
- 尝试模型融合（见第五节）

> **新手大忌**：直接复制最高票 Notebook 无脑提交。你可能拿到高分甚至奖牌，但什么都没学到，且容易踩数据泄露的坑。

---

## 三、核心方法论：验证优先

> Grandmaster 铁律：**CV（交叉验证）是你唯一可信的评估**，Public LB 只是参考。

### 3.1 先建立可信的验证方案

- **标准表格**：Stratified K-Fold（默认 5 折，按目标分层）
- **时间序列**：TimeSeriesSplit（按时间切，**绝不用过去预测过去**）
- **同一实体多样本**（同病人多图、同用户多交易）：GroupKFold，**同一实体必须同折**
- **类别不平衡**：StratifiedKFold 保证每折类别分布一致

### 3.2 CV 与 LB 差距过大的排查

- **数据泄露（Leakage）**：特征与目标过于对齐（如特征里含目标衍生值）
  - 检查：CV 高到不真实（噪声表格数据 AUC > 0.99 就要警惕）
  - 处理：Target Encoding 必须在**折内**计算，绝不能用全量数据统计
  - 时间序列的时序泄露是最常见的生产翻车点
- **分布漂移**：训练集与 LB 数据分布不同（用 train-test distribution check 检测）

> NVIDIA Grandmaster Playbook 原话：**"If you can't trust your validation score, you're flying blind."**（验证不可信 = 蒙眼飞行）

---

## 四、表格赛完整流程（含代码要点）

### 4.1 项目结构（保持可复现）

```text
competition/
├── data/          # 原始数据（只读）
├── configs/       # 配置
├── src/           # 训练代码
├── models/        # 模型产物
├── oof/           # OOF 预测（out-of-fold）
├── logs/          # 实验日志
├── submissions/   # 提交文件
└── experiments.md # 实验记录
```

### 4.2 特征工程清单（按性价比排序）

| 技术 | 说明 | 效果 |
| --- | --- | --- |
| Target Encoding | 用目标均值替换类别值（**必须折内做**） | 高 |
| 聚合特征 | groupby mean/median/std/count | 高 |
| 时序特征 | lag（t-1/t-7/t-30）、滚动均值/标准差 | 高（时间序列） |
| 日期拆解 | year/month/day/hour/weekday/is_weekend | 高 |
| 交互特征 | A×B、A/B、A+B 组合 | 中 |
| 频次编码 | 类别出现频率 | 中 |
| 多项式特征 | A²、A×B | 低-中（易过拟合） |
| 分箱 | 连续变量分箱 | 中 |
| 异常值标记 | IQR/z-score 异常标记 | 中 |

> 顶级选手可能生成**数百个特征**，但会做特征选择避免噪音淹没信号（有选手用置换检验删掉 190 个特征后 CV 提升）。

### 4.3 建模

- 先用多样基线探路：线性模型 + GBDT（XGBoost/LightGBM/CatBoost）+ 神经网络（cuML 加速）
- 记住 OOF 文件：**永远保存 OOF 预测，统一 KFold 与 seed**——这让你后续能做无数尝试
- 类别不平衡：CatBoost 里手调 `class_weights`（有冠军直接调 1:110 看 LB 找最优）

---

## 五、模型融合（冲榜核心武器）

### 5.1 从简单到复杂

1. **加权平均（Blending）**：给多个模型预测按权重平均，权重可用网格搜索/爬山法
2. **Stacking**：用基模型的 OOF 预测作为特征，训练元模型（meta-learner）
3. **分层 Stacking**：第一层模型输出 → 第二层模型再融合（冠军常用 2-3 层）

### 5.2 正确姿势

- **只用 OOF 预测训练元模型**——绝不用训练集内预测（会严重过拟合）
- 元模型常用 Ridge/Logistic Regression（简单稳健）
- 多 seed + 多折重复训练，最后对模型平均（如 10 折 × 2 seed = 20 个模型求平均）
- 融合后 CV 达到平台期就停，别过度优化 LB

> 实战案例：Playground S5E12 冠军用"爬山法选模型 + Ridge 融合"，最终 CV 0.70860 vs Public LB 0.70739，差距 0.00121 即停——**信任 CV，不过度拟合 LB**。

---

## 六、Code Competition 专项（隐藏数据重跑）

这类比赛你的最终 Notebook 会在隐藏数据上被重新执行，要求：

- **防御性编码**：路径用相对路径、处理缺失列、代码可重入
- **producer/consumer 架构**：
  - producer Notebook：训练模型、产出重工件 → 导出为**私有 Dataset**
  - consumer Notebook：加载工件 → 对隐藏测试数据打分
- **GPU 卸载**：重活放 Kaggle GPU 跑，本地只做轻验证
- **错误容忍**：隐藏运行错误信息很少，写健壮重试循环
- **提交前检查**：行数匹配 sample submission、ID 与顺序正确、列齐全、格式符合指标要求

---

## 七、比赛节奏与纪律

### 提交前检查清单
- [ ] 规则已接受、凭据可用
- [ ] 文件存在、行数匹配、ID 顺序正确、必填列齐全
- [ ] 格式符合指标要求（概率 vs 类别、是否裁剪/取整）
- [ ] 本地 CV 与 OOF 诊断与本次提交一致

### 提交后
- 轮询直到状态为 processed 或失败可见
- 保存 submission_receipt.json（收据）
- 把 Public Score 记入实验日志

### 实验纪律
- 每个实验记录：seed、代码版本、数据版本、运行配置、指标、产物、分数收据
- 一次只改一个变量
- **信任 CV，Public LB 只作为反馈**（排名会因测试集换动而变）

---

## 八、资源与工具

| 资源 | 用途 |
| --- | --- |
| Kaggle CLI（`pip install kaggle`） | 数据下载/上传、提交、查分、kernel push |
| `kaggle competitions submit <slug> -f file -m msg` | 提交 |
| `kaggle competitions submissions <slug>` | 查提交历史 |
| Kaggle Notebook | 免费 GPU/TPU |
| NVIDIA Kaggle Grandmasters Playbook | 表格赛 7 大实战技术（cuML/cuDF 加速） |
| 各比赛 Writeups 区 | 冠军解题思路（最好学习材料） |

---

## 参考来源

- Kaggle 官方竞赛文档 & Getting Started 指南
- NVIDIA Blog: *The Kaggle Grandmasters Playbook: 7 Battle-Tested Modeling Techniques for Tabular Data*
- Kaggle 社区冠军 Writeups（Playground S5E12 / S6E1 / Santa 2025 等）
- Kaggle 新手建议帖（Getting Started / Questions-and-Answers 区）
- `agentic-kaggle-skill`（FrankS-IntelLab，MIT）内 references/ 实战工作流

---

*本文由 buleboy 整理，配合 clouds 仓库的 `agentic-kaggle-skill` 使用。*
