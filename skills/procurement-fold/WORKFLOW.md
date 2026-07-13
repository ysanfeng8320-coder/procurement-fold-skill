# Workflow Builder / Codex / WorkBuddy 可粘贴 Prompt

工作目录必须是 `procurement-intelligence` 仓库根（含 `kg_engine/`）。

---

## 场景 W0 · 新用户启动（默认必跑）

```text
使用 skill procurement-fold。
这是新会话。禁止立刻跑 scene_fit / run_fold。
按 SKILL.md「3A 商业咨询问答」逐题询问（一次一题，等回答）：
产品原话 → 高低端价带 → 客户是谁与特质 → 场景 → 成交路径 → 区域 → 竞品 → 成功样本。
全部确认后，引导用户上传产品介绍/公司介绍/PPT或Word/培训纪要。
然后输出「简易报告」。
若检测到没有 ZHILIAO_API_KEY / SHIBO_API_KEY，必须明确告诉用户：
完整招标分析需自行准备 API Key；当前只能做资料级简易报告。
```

---

## 场景 W1 · 产品场景拟合（入口 B）

```text
使用 skill procurement-fold。
任务：对产品 seal_control（印控仪/智能印章）做场景拟合。
步骤：
1. 运行 doctor.py 确认仓库完整。
2. cd kg_engine && PYTHONPATH=. python3 -B fold/scene_fit.py seal_control
3. 用系统浏览器打开最新 fold_runs/*_scene_fit_seal_control/report.html
4. 用中文摘要：各系统拟合分、份额、密度、客单、结论与下一步。
约束：拟合看份额×密度×客单；不要把物业/服务类当机会；小样本结论要标明。
```

把 `seal_control` 换成 `binding_machine` / `shredder` / `copier` 即可换品。

---

## 场景 W2 · 物种货盘名单 + 电话补全（入口 A）

```text
使用 skill procurement-fold。
任务：物种 court（法院），货盘 seal_control,binding_machine，行动区陕西+甘肃，本地数据，并电话补全。
步骤：
1. doctor.py
2. 若 api-budget>0 先跑 acquisition_gate；本任务 api-budget=0。
3. python3 skills/procurement-fold/scripts/run_fold.py \
   --species court \
   --portfolio seal_control,binding_machine \
   --discovery 安徽,浙江,北京,上海 \
   --action 陕西,甘肃 \
   --reuse-local --api-budget 0 --phone-complete
4. 打开 fold_runs/<最新court>/report.md 与 phone_report.html
5. 中文交付：货盘机会分、可行动名单（直联/经集成商）、仍缺电话的数量。
硬规则：名单后必须有电话补全；物种锚定法院不变成扁标签。
```

`--species` 可改为 `procuratorate` / `police` / `agriculture`。

---

## 场景 W3 · 品类×系统训练预测验证看板

```text
使用 skill procurement-fold。
任务：生成品类×系统三板块报告（训练2025→预测2026→验证2026），金额千元。
步骤：
1. doctor.py
2. cd kg_engine && PYTHONPATH=. python3 -B fold/tpv_matrix_report.py
3. 打开最新 fold_runs/*_tpv_matrix/report.html
4. 摘要：默认品类、样本偏差风险、哪一组合可行动。
约束：预测面板不得使用2026实测；验证仅对照。
```

---

## 场景 W4 · 仅电话补全已有 run

```text
使用 skill procurement-fold。
任务：对 fold_runs/<RUN_ID> 做电话补全并打开报告。
步骤：
1. doctor.py
2. cd kg_engine && PYTHONPATH=. python3 -B fold/phone_complete.py --run ../fold_runs/<RUN_ID>
3. open ../fold_runs/<RUN_ID>/phone_report.html
4. 报告可行动/直联/经集成商/仍缺数量。
```

---

## 场景 W5 · 采集闸门检查（花钱前）

```text
使用 skill procurement-fold。
任务：检查采集闸门是否允许 test 模式拉取 200 条。
步骤：
cd kg_engine && PYTHONPATH=. python3 -B fold/acquisition_gate.py \
  --mode test --api-budget 200 \
  --keywords 印控仪,智能印章 --species court --product seal_control
根据退出码告诉用户是否可拉数；未过闸则列出失败项，禁止调 API。
```

---

## Workflow Builder 建议设置

| 项 | 建议 |
|----|------|
| Working directory | 仓库根 |
| Model | 任意能跑 shell 的 Agent |
| 网络 | 仅本地时可不开放；API 补数/补电话再开 |
| 成功标准 | 生成 `fold_runs/...` 报告并用浏览器打开；中文摘要 |
| 失败标准 | doctor 失败、闸门未过、无 phone_report 却声称交付完成 |
