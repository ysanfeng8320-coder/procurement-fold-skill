# Procurement Fold — Skill Spec

通用「结构折叠」引擎：从产品包 + 标讯样本学习可迁移约束，在落地区输出可行动可能性。  
**本品无关**；印控仪（`seal_control`）仅为验证配置。

默认路径：约束探讨 → 统计/图推理 → **不上神经网络模型**（除非阶段 1 失败且样本足够）。

---

## 1. 边界

| 组件 | 职责 | 不做什么 |
|------|------|----------|
| 本 Skill | 编排 Ingest→Structure→Fold→Act；维护 Product Pack；产出规律卡片与名单 | 不替代销售；不预测「谁会中标」 |
| `kg_engine` | 图谱存储、已有 scout 采集、联系人、共现推理可复用 | Fold 不新建第二套图谱库；可只读加载 scope |
| 知了网/世舶 API | 按需补发现区/落地区标讯 | 额度上限内按需用，不强制用满 |
| Product Pack | 本品词典、销售约束、产品说明 | 不做全国万能品类树 |

---

## 2. 运行配置（输入）

见 `schemas/run_config.schema.json`。

关键字段：

- `product_pack`: pack 目录名（如 `seal_control`）
- `discovery_regions`: 学规律的省（试点：皖浙京沪）
- `action_regions`: 落实名单的省（试点：陕甘）
- `api_budget`: 上限（试点 500），实际可更少
- `reuse_local`: 优先复用 `scout_data/` 与已有 scope
- `windows_months`: 涌现窗口，默认 `[1, 2]`
- `max_age_years`: 只使用近 N 年公告，默认 `3`（证据与名单均受此限制）

**标注规则**：`hit_tier` 只认**标题真实命中**词典词；禁止因文件名/搜索词把无关公告抬成 related（避免「钢琴采购」混入）。

---

## 3. Product Pack 格式

目录：`product_packs/<pack_id>/`

| 文件 | 必填 | 说明 |
|------|------|------|
| `lexicon.yaml` | 是 | 本品/近义/关联/易混检索词与买方系统词 |
| `constraints.md` | 是 | ≤15 条可检验销售/结构约束（先验） |
| `product_notes.md` | 是 | 产品线、场景、客群摘要 |
| `sources.md` | 是 | 资料来源与日期 |
| `raw/` | 否 | 原始纪要/摘录 |

`lexicon.yaml` 结构见 `schemas/product_pack.schema.json`。

换品类 = 新建 pack，不改引擎代码。

---

## 4. 流水线

```text
Ingest    → 标准化标讯记录（本地优先，API 补差，计入 budget）
Structure → 产品锚定软标签（命中层级、买方系统、年月、金额桶）
Fold      → 规律卡片（先验约束加权 + 统计支持度/反例 + 月度涌现）
Act       → 落地区名单 A/B + 涌现抬权
```

### 4.1 Structure 软标签（不做万能归类）

每条记录：

- `hit_tier`: `target` | `near` | `related` | `confuse` | `none`
- `buyer_system`: 来自 lexicon.systems 规则
- `year_month`: `YYYY-MM`
- `amount_bucket`: 粗分
- `region`, `buyer`, `winners`, `title`, `source_id`

### 4.2 Fold 规律卡片

见 `schemas/rule_card.schema.json`。

类型：

- `prior` — 来自 constraints.md，标讯可证实/证伪
- `cooccurrence` — 系统×命中层级共现
- `temporal_surge` — 1～2 月涌现
- `diffusion` — 同系统短窗扩散（若样本足够）

每张卡片：`if` → `then`、`support`、`counterexamples`、`confidence`、`action_hint`。

### 4.3 Act 名单

见 `schemas/lead.schema.json`。

- **A `similar_unbought`**：结构相似（高价值系统/场景）但落地区未见本品强命中  
- **B `assoc_gap`**：有关联/近义命中，无本品 `target` 命中  
- 涌现命中时 `priority` 上调  

每条必须有：单位、地区、命中规律、证据、建议动作、可行动性。

---

## 5. 输出产物

运行目录：`fold_runs/<run_id>/`

- `structured_records.jsonl`
- `rule_cards.json`
- `leads.json`
- `report.md`
- `run_meta.json`（预算消耗、数据源、pack 版本）

---

## 6. 验证标准（通用 Skill，非单品销售）

1. 换 pack + 地区参数即可跑，引擎不变  
2. 发现区规律能解释落地区至少部分命中  
3. 名单可跟进（电话或集成商路径）或明确不可行动原因  
4. 优于「只搜本品关键词」的朴素列表  

印控仪跑通 = Skill v0；第二品类冒烟 = 通用性过关。

---

## 7. 明确不做

- 神经网络中标预测  
- 全国全品类一次性归类  
- 强制用满 API 额度  
- 导出无证据的「全量客户库」  
