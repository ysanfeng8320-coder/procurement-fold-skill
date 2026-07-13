# procurement-fold

政府采购 **结构折叠** Skill：给 Codex / Cursor / 通用 Agents / Workflow Builder 使用。

别人拿到后，只要打开本仓库（或把本 skill 软链到 Agent skills 目录），即可按阶段跑分析与名单。

## 给你同事的最短安装

### 推荐：一条命令（Codex / Cursor / Claude 等）

发布仓：`ysanfeng8320-coder/procurement-fold-skill`（源文件在 monorepo `publish/procurement-fold-skill/`）：

```bash
npx -y skills add ysanfeng8320-coder/procurement-fold-skill -g --all
```

WorkBuddy 需额外软链（官方 `skills` CLI 暂不支持 workbuddy）：

```bash
mkdir -p ~/.workbuddy/skills
ln -sfn ~/.agents/skills/procurement-fold ~/.workbuddy/skills/procurement-fold
```

### 完整数据流水线（可选）

需要引擎时，另打开 `procurement-intelligence`（含 `kg_engine/`），在仓库根执行：

```bash
python3 skills/procurement-fold/scripts/doctor.py
```

本机已有 dbs-bridge 时，也可从 monorepo 桥接：

```bash
~/.claude/skills/dbs-bridge/scripts/bridge-skill.sh link \
  "/path/to/procurement-intelligence/skills/procurement-fold"
```

### 在对话里怎么唤起

对 Agent 说：

- `用 procurement-fold`
- `procurement-fold：先咨询，再出简易报告`
- `/procurement-fold`（若客户端支持斜杠）

### Workflow Builder

打开 Cursor Automations / Workflow Builder，工作目录选 monorepo 根（若要跑引擎），Prompt 粘贴 `WORKFLOW.md` 里对应场景。

## 目录说明

| 路径 | 作用 |
|------|------|
| `SKILL.md` | Agent 必读执行说明书 |
| `ORCHESTRATION.md` | 阶段 0–6 总链路 |
| `orchestration.html` | 可视化总链路（浏览器打开） |
| `WORKFLOW.md` | Workflow Builder 可粘贴 Prompt |
| `README.md` | 给人看的安装说明（本文件） |
| `config/acquisition_gate.yaml` | 采集闸门 |
| `product_packs/` | 产品包 |
| `species_packs/` | 系统客户物种包 |
| `scripts/run_fold.py` | 物种×货盘入口 |
| `scripts/doctor.py` | 环境自检 |
| `agents/openai.yaml` | Codex skill 展示元数据 |

引擎在仓库 `kg_engine/fold/`。

## 一条龙命令（本地、不花钱）

```bash
# 场景拟合（产品入口）
cd kg_engine && PYTHONPATH=. python3 -B fold/scene_fit.py seal_control

# 物种货盘 + 电话补全
python3 skills/procurement-fold/scripts/run_fold.py \
  --species court \
  --portfolio seal_control \
  --reuse-local --api-budget 0 --phone-complete
```

## 权限与费用

- **本包不附带知了网/世舶 API Key。** 完整拉数分析需对方自行申请并设置：
  - `export ZHILIAO_API_KEY=...`
  - `export SHIBO_API_KEY=...`（或 `GOVBID_API_KEY`）
- **无 Key 也能先用**：先投喂产品介绍 / 使用场景 / 培训纪要 → 出简易报告（结构、建议场景、价带、排除词、采集计划）。
- 有本地 `scout_data` 时可用 `--reuse-local --api-budget 0` 做有限分析。
- 拉新数前必须过采集闸门；正式模式上限见 `config/acquisition_gate.yaml`。
- 切勿把 Key 写进 SKILL.md 或提交 git。

## 状态

可分发的执行版：编排、闸门、场景拟合、名单、电话补全、验证报表均已挂载。  
仍在演进：资料投喂自动化、有效边回写库、大样本公安等稀缺场景。
