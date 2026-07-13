# Method changelog — procurement-fold v2 iteration

## 2026-07-12 — 可分发完备包（Codex / Workflow Builder）

### Deliverable
- 重写 `SKILL.md`：Agent 可直接执行的强制清单与阶段命令
- `README.md`：给人安装/桥接说明
- `WORKFLOW.md`：5 个可粘贴 Workflow Prompt（W1–W5）
- `scripts/doctor.py`：仓库完整性自检
- `agents/openai.yaml`：Codex 展示元数据
- 已桥接 `~/.codex/skills` / `~/.agents/skills` / `~/.claude/skills`
- 修复 `portfolio.py` 电话判断缩进错误

### Share rule
- 必须分享整个 `procurement-intelligence` 仓库（含 `kg_engine/`），不能只拷 skill 目录

---

## 2026-07-12 — 电话补全必做 + 采集闸门 + 总链路完善

### Phone (阶段5硬规则)
- 新增 `kg_engine/fold/phone_complete.py`：harvest → 中标商/参照单位 → 物种有号渠道池 → 可选 API
- `run_v2 --phone-complete` / `--phone-api-budget`
- 法院样例 run `20260711_122047_court`：补全后 18/18 可行动（经集成商路径）
- 产出 `phone_report.html`

### Gate
- `config/acquisition_gate.yaml` + `fold/acquisition_gate.py`
- `run_v2` 在 api-budget>0 时默认过闸（`--gate-mode skip` 可关）

### Docs
- 阶段3拆 3a分析→3b规律→3c发现；阶段1改为产品知识入库
- `orchestration.html` 同步

---

## 2026-07-12 — 总链路编排（对齐内容 skill 树格式）

### Goal
- 把散落报表收成 Phase0–6 树状编排，便于 Agent 按阶段调用。

### Deliverable
- `ORCHESTRATION.md`：总目标、双入口（物种优先 / 产品发现）、各阶段子能力与缺口。
- `SKILL.md`：改为总链路入口，指向编排文档。
- 阶段3已有：`scene_fit`（印控仪）；下一优先：阶段4中标商渠道名单 + 阶段6有效边回写。

---

## 2026-07-11 — 三板块：训练→预测→验证

### Goal clarified
- 2025 = 训练；2026预测 = 只用2025逻辑（不偷看实测）；2026实测 = 验证层
- 同页三板块：①训练实绩 ②预测 ③验证对照

### Deliverable
- `fold_runs/20260711_163357_tpv/report.html`
- 金额千元；可切换装订机/碎纸机/复印机/印控仪
- 验证发现：当前2025成交池偏年底 → 预测主推12月，但2026实测旺在5–6月 → MAPE高，需补全2025月度后再训

---

### User ask
- 机会分叠加时间：7月 vs 8–9月 vs 11月何时推碎纸机
- 什么系统推什么价；成交池要有价位与台数；推荐窗口期望中标台数

### Deliverable
- `fold_runs/20260711_162122_timing_price/report.html`
- Canvas: `shredder-timing-price`
- 时机分 = 基础机会分(42) × 季节乘数；档位仍按 ≥60% / 35–59% / <35%
- 结论：5–6月首选(期望173台) > 11–12月(95) > 11月(31) > 7月跟尾(10) > 8–9月不主推
- 价位：法院 0.8–1.5万；检察 0.3–0.8万；多数 <1万/1台
- 台数：标题「N台」优先；办公设备整包不按金额虚增台数

### Note
- 知了网余额 0，未拉全市场月度；5–6月来自本地样本，11–12月来自成交池。

---

### User feedback
- 档位要写清百分比区间；交付要有增长率曲线，不能只有数字表。
- 复印机/碎纸机不可能只有 1–2 条线索。

### Root cause
- 旧报告把「线索」定义成 assoc_gap 缺口预测，且 `max_leads` 很小。
- 知了网 2025 全市场：碎纸 85,638 / 复印 106,601 / 一体机 161,477；印控仪仅 159 → **产品不窄，算法窄**。

### Changes
1. 档位显式：`高≥60%` / `中35%–59%` / `低<35%`（机会分即百分制）。
2. `build_volume_leads`：高销量品按买方单位去重成交池，每品目标 100+。
3. 可视化：`fold_runs/20260711_155538_volume/report.html` + canvas `procurement-volume-growth`。
4. 本次成交池：复印 119 / 碎纸 95 / 装订 60 / 印控 6。

### Quota
- 后续按月全市场 total 拉取时触发 `QUOTA_EXCEEDED`；月曲线暂用成交池按月代理，年总量仍为真实查询。

---

### What changed
1. **知了网 `begin_date`/`end_date`**：`ZhiliaoCollector.search` + `UnifiedCollector.collect_one_page(prefer_zhiliao)`；带日期强制走知了网。
2. **`fetch_api_records` 关键词均分预算**：修复首词（碎纸机）吃光额度导致装订机/复印机假荒漠。
3. **`temporal_validate.py`**：整年 2025 训练 → 2026-04~06 验证；多物种×多产品；物种桥接额度按物种切开（法院不再饿死农业局）。
4. **产品包**：`shredder` / `binding_machine` / `copier`；物种包：`agriculture`。

### Deliverable
- Run: `fold_runs/20260711_150734_temporal/report.md`
- 全真实 API（训练 ~450 条 / 验证 ~173 条，source=zhiliao）
- 主结论：法院×印控/碎纸、检察×碎纸、农业×复印/装订 可推；农业×印控荒漠；assoc_gap 精确率不适合当主 KPI，改看 2026 新出现单位。

### Honest gaps
- 单次预算下 bridge 深度仍有限（每物种 ~100 条）；加大预算会更稳。
- 线索单位名跨季精确命中≈0；验证价值在「组合是否仍有陕甘实购」与「新单位跟进池」。

---

## 2026-07-11 — court × seal_control → USABLE (6/6)

### Problem
- Police wedge: 陕甘公开数据近3年几乎无「公安局×印控/电子印章」买方命中 → G2/G3 失败。
- Court 初跑：陕甘有真实印控仪成交，但发现区空、无 assoc_gap、leads=0。

### Method changes
1. **Region inference**：API 省码过滤常串省；按买方名/标题/API province 回填真实省。
2. **National bridge search**：`法院印控仪` 等桥接词走「全国」检索（额度约 40%），再回填省份。
3. **peer_gap / 同省参照**：落地区已有强相关成交时，未购同物种单位标为同省跟风缺口（证据优先同省已购院）。
4. **Eval gates**：G3/G4 接受 `assoc_gap` 或 `peer_gap`；G4 要求缺口线索必须有 `matched_keyword`。
5. **Province map**：采集器扩展至全国省码，支持发现区动态扩入。

### Deliverable
- Run: `fold_runs/20260711_122047_court`（6/6 USABLE）
- Sales report: `fold_runs/20260711_122047_court/report.md`
- Lead mix: 1 assoc_gap（漳县印章管理系统）+ 12 peer_gap（同省跟风，参照南郑/肃州印控仪）+ 5 already_bought
- Eval: 陕甘 action events=9；events=28。

### Honest gaps
- 公安局楔子在公开 API 上仍是数据荒漠；本交付改用**法院**物种验证。
- 名单电话几乎全空 → 行动路径以集成商/运营商为主。
- 扩散名单含「本院近窗无本品公开记录」单位，不保证未私下采购。
