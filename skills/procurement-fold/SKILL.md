---
name: procurement-fold
description: >-
  政府采购结构折叠销售情报。启动时必须先做商业咨询问答（挖出用户已有的产品定位、
  客户特质、成交路径），再引导上传产品/公司介绍（PPT/Word等），然后才可简易报告
  或（有自备 API Key 时）跑闸门/拟合/名单/电话补全。
  Use when procurement-fold, 采购折叠, 政府采购, 场景拟合, 印控仪, 装订机, 法院采购,
  中标商渠道, 电话补全, WorkBuddy, or user wants bid intelligence with product packs.
---

# Procurement Fold / 采购结构折叠

你是执行本 skill 的 Agent（Codex / Cursor / Workflow Builder 均可）。  
**先读本文件再动手。** 详细编排见同目录 `ORCHESTRATION.md`；可视化：`orchestration.html`。

## 0. 环境与能力边界

本 skill 有两档能力：

| 档位 | 需要什么 | 能做什么 |
|------|----------|----------|
| A. 咨询 + 简易报告 | 仅本 skill（`npx skills add` 安装即可） | 阶段 0–1–2：商业问答、资料投喂、基于资料的简易报告 |
| B. 完整数据流水线 | 本地打开 `procurement-intelligence`（含 `kg_engine/`）+ 自备 API Key | 闸门、场景拟合、名单、电话补全、HTML 报告 |

```text
# 档位 A：skill 装在 Agent skills 目录即可
~/.codex/skills/procurement-fold/   （或 ~/.agents / ~/.cursor 等）

# 档位 B：另需 monorepo
<REPO>/skills/procurement-fold/
<REPO>/kg_engine/
<REPO>/scout_data/          ← 可空
<REPO>/fold_runs/           ← 自动创建
```

1. **档位 A（默认）**：没有 monorepo 也继续问答与简易报告；**禁止**假装已跑通大样本拟合。  
2. **档位 B**：工作区是 `procurement-intelligence` 根时，再跑自检与引擎：

```bash
python3 skills/procurement-fold/scripts/doctor.py
```

3. 依赖：档位 B 需要 `python3`、建议 `PyYAML`。  
4. **API Key（重要）**：本包**不附带**知了网/世舶 Key。  
   - 完整拉数、大样本场景发现、API 电话补全 → 对方必须**自己申请/配置** Key：  
     `export ZHILIAO_API_KEY=...` 和/或 `export SHIBO_API_KEY=...`  
   - **无 Key 也可先用档位 A**。  
5. HTML 报告用系统浏览器打开：`open <path>.html`（macOS）。

### Agent 必须口头提示用户（无 Key 时）

检测到未设置 `ZHILIAO_API_KEY` / `SHIBO_API_KEY` 时，先明确告诉用户：

> 你现在没有知了网/世舶 API Key，完整招标数据分析需要自行准备 Key。  
> 但你可以先把产品介绍和使用场景发上来，我可以先出一份简易报告（产品结构、建议场景、价带、排除词、下一步采集计划）。  
> 有 Key 并过采集闸门后，再做场景拟合与名单。

失败则停止并告诉用户缺什么，不要假装跑通。

## 1. 总目标

找到可赚钱的「**产品 × 场景 × 价带 × 渠道**」，落到可打电话的名单（陕甘默认可改）。

**前提假设（对本 skill 用户几乎总成立）**：对方通常**已有产品、已有场景认知、已有客户画像与路径**——高端/低端、客户特质、怎么卖，他们心里大体清楚。  
Skill 的第一件事不是替他「找产品」，而是**把他脑子里已有的商业知识问清楚并结构化**，再引导上传资料，最后才跑数据。

价值顺序：  
**商业问答入库** → 资料投喂 → 利润带/物种锚定 →（有 Key 再）规律与场景拟合 → 名单 → 电话补全 → 人外呼。

## 2. 何时启用

用户提到：采购折叠、政府采购情报、场景拟合、法院/检察/公安货盘、印控仪/装订机/碎纸机、中标商渠道、电话补全、`fold_runs`、要用 Codex/Workflow/WorkBuddy 跑招标分析。

## 3. 启动顺序（强制）

**禁止**一上来就跑 `scene_fit` / `run_fold` / 拉 API。  
新会话默认走：**商业咨询问答 → 引导上传资料 → 简易报告 →（可选）有 Key 再进数据流水线**。

仅当用户明确说「资料和定位已经在 pack 里，直接跑某某报告」且你核对过 pack 后，才可跳过问答。

### 3A · 商业咨询问答（阶段 0，逐题问、等回答）

风格对齐 dbs：一次只问一题，等用户答完再下一题；不替用户编造定位。

开场固定说：

> 用这个 skill 前，先把你已经知道的说清楚——产品、客户、路径你通常都有数。  
> 我按咨询方式问几题；答完再请你上传产品/公司介绍。  
> 没有知了网/世舶 API Key 也能先做简易报告；完整招标大数据分析需要你自己准备 Key。

然后**按序单题**询问（可随回答追问，但不要一次丢整卷）：

1. **产品原话**：「你现在主推的产品叫什么？一句话它解决什么问题？」（原封不动记）  
2. **定位高低**：「它偏高端、中端还是低端？大概什么价带（可以到千元/万元）？利润大概怎样？」  
3. **客户是谁**：「你最想成交的客户是哪类单位？（例如法院/检察/公安/政务/企业）他们有什么共同特质？」  
4. **场景**：「这类客户在什么具体场景下会买？（合规/归档/批量网点/项目打包…）」  
5. **路径**：「你现在主要怎么成交？直联采购、找集成商/运营商、还是替换竞品？哪条最熟？」  
6. **区域**：「先落哪些省？发现规律是否也看外省？」  
7. **竞品**：「市场上你常碰到的对标品牌/型号是谁？（没有就说没有）」  
8. **成功样本**：「有没有一单你觉得‘就该是这样卖’的真实例子？（客户+价+怎么成的）」

问答收束时，用一段话复述用户的「产品×客户×价带×路径」，请用户确认或改正。**未确认不得进入跑数。**

### 3B · 引导上传资料（阶段 1）

确认问答后引导：

> 请上传你方便给的材料（有什么传什么，不要求一次齐全）：  
> - 产品介绍 PPT / Word / PDF  
> - 公司介绍  
> - 培训纪要、会议记录、销售话术  
> - 竞品截图或说明书  
> 我会写入产品包，并据此出简易报告。

收到文件后：摘要进 `product_packs/<id>/`（或先口头结构化再落盘），抽出价带、场景词、排除词、竞品。

### 3C · 简易报告（无 Key 也可交付）

至少包含：

1. 用户确认过的产品定位与价带  
2. 优先系统客户与客户特质  
3. 建议成交路径（直客 / 集成商）  
4. 采集时要排除的噪声（物业服务等）  
5. **若有 API Key**：下一步采哪些关键词、建议预算档（test/formal）  
6. **若无 API Key**：明确写「完整招标分析需自行准备知了网/世舶 Key；当前仅为资料级简易报告」

### 3D · 两条数据入口（资料齐了再选）

| 入口 | 用户说法 | 从哪开始 |
|------|----------|----------|
| A 物种优先 | 「法院/公安这周推什么」 | 阶段2→4 `run_fold.py --species …` |
| B 产品发现 | 「筛印控仪场景」 | 阶段3a→3c `scene_fit.py` |

未说明时问一句：`先锁定系统客户，还是先按产品做场景拟合？`  
**无 Key 且无本地 scout 时**：停在简易报告，不要空跑拟合装样子。

## 4. 阶段流水线（问答与资料之后）

```text
0 商业问答 → 1 资料入库+简易报告 → 2 定位与包
→ 闸门 → 3a 数据分析(物种锚定) → 3b 找规律 → 3c 场景发现
→ 4 名单 → 5 电话补全(必做) → 5b 人行动 → 6 验证回写
```

### 阶段 0–1
见上文 3A–3C。阶段 0 本质是**把卖方已有认知问出来**，不是替他找品。

### 阶段 2 · 定位与包
- 产品包：`product_packs/`（seal_control, binding_machine, shredder, copier, …）  
- 物种包：`species_packs/`（court, procuratorate, police, agriculture）  
- 发现区学规律 / 行动区出名单（默认发现皖浙京沪，行动陕甘）。  
- 写入问答得到的价带硬过滤与排除词。
### 采集闸门（花钱前必过）

```bash
cd <REPO>/kg_engine && PYTHONPATH=. python3 -B fold/acquisition_gate.py \
  --mode test --api-budget 200 \
  --keywords 印控仪,智能印章 --species court --product seal_control
```

不过闸禁止打满 API。配置：`config/acquisition_gate.yaml`。

### 阶段 3a · 数据分析（硬规则）
- 每条必须锚定系统客户：**公安局=公安局**，禁止早期 a/b/c 扁标签。  
- 结构字段：species + product hit + 价带 + 年月 + 买方/中标商。

### 阶段 3b · 寻找规律
- 在物种切片上统计/图推理（默认不上神经网络）。

### 阶段 3c · 场景发现

```bash
cd <REPO>/kg_engine && PYTHONPATH=. python3 -B fold/scene_fit.py seal_control
open ../fold_runs/*_scene_fit_seal_control/report.html
```

拟合 = 份额 × 密度 × 客单；淘汰复印纸式共现与过稀场景。

### 阶段 4 · 名单

```bash
python3 skills/procurement-fold/scripts/run_fold.py \
  --species court \
  --portfolio seal_control,binding_machine \
  --discovery 安徽,浙江,北京,上海 \
  --action 陕西,甘肃 \
  --reuse-local \
  --api-budget 0 \
  --phone-complete
```

多品类×系统看板：

```bash
cd <REPO>/kg_engine && PYTHONPATH=. python3 -B fold/tpv_matrix_report.py
```

### 阶段 5 · 电话补全（必做）

名单后必须跑；禁止只交单位名。

```bash
cd <REPO>/kg_engine && PYTHONPATH=. python3 -B fold/phone_complete.py \
  --run ../fold_runs/<run_id>
open ../fold_runs/<run_id>/phone_report.html
```

策略：本地抠号 → 买方/参照中标商 → 物种有号渠道池 → 可选 `--api-budget N`。  
输出：`直联 ☎` 或 `经集成商联系：XX☎…`。

### 阶段 6 · 验证复盘
- `train_predict_validate` / `tpv_matrix_report`：训练→预测→验证。  
- 预测不得偷看验证年实测。  
- 结论应回写有效边（产品×物种×价带）；不要只堆 HTML。

## 5. Agent 执行清单（每次任务）

1. 新用户/新会话：先走 **3A 商业问答**（逐题），再 **3B 上传**，再 **3C 简易报告**。  
2. `doctor.py` 在即将跑脚本前执行即可（问答阶段可不打断用户）。  
3. 无 Key：口头提示 + 只交简易报告；有 Key 且要拉数：先采集闸门。  
4. 跑脚本后用浏览器打开 HTML；中文摘要结论与缺口。  
5. 不把物业/服务类当办公设备机会；不用裸共现当场景发现；不替用户编造他没说过的定位。

## 6. 输出约定

| 产物 | 位置 |
|------|------|
| 物种货盘销售报告 | `fold_runs/<id>/report.md` |
| 线索 JSON | `fold_runs/<id>/leads.json` |
| 电话报告 | `fold_runs/<id>/phone_report.html` |
| 场景拟合 | `fold_runs/*_scene_fit_*/report.html` |
| TPV 矩阵 | `fold_runs/*_tpv_matrix/report.html` |

金额单位默认 **千元**。机会分档：高≥60% / 中35–59% / 低&lt;35%。

## 7. 硬禁止

- **跳过商业问答**直接跑脚本或空问「你要分析什么品」  
- **替用户编造**他没说过的定位/客户/路径  
- 一次甩出整卷问卷（必须逐题等回答，对齐 dbs）  
- 未过闸打满收费 API  
- 扁标签采购方（必须定点物种）  
- 小样本冒充大样本结论  
- 名单无电话补全就当交付完成  
- 泄露或提交 API Key 到 git  
- 无 Key 却假装已完成大样本场景拟合

## 8. 给 Workflow Builder 的默认 Prompt

复制 `WORKFLOW.md` 中对应场景整段作为自动化步骤说明；工作目录必须是仓库根。

## 9. 语言

用户用中文则全程中文回复。
