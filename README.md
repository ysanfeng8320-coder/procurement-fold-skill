# procurement-fold-skill

政府采购 **结构折叠** Skill：商业咨询问答 → 资料投喂 → 简易报告 →（自备 API Key 后）场景拟合 / 名单 / 电话补全。

给 Codex、Claude Code、Cursor 等支持 [Agent Skills](https://agentskills.io) 的客户端用；一条命令安装，对齐 `dontbesilent2025/dbskill` 的分发方式。

## 安装

```bash
npx -y skills add ysanfeng8320-coder/procurement-fold-skill -g --all
```

只装到 Codex：

```bash
npx -y skills add ysanfeng8320-coder/procurement-fold-skill -g -a codex
```

更新：重跑上面的 `npx` 命令即可。

### WorkBuddy

官方 `skills` CLI **目前不支持** WorkBuddy（没有 `workbuddy` agent）。  
`npx skills add ... -g --all` 会装到 Codex / Cursor / `~/.agents/skills` 等，**不会**自动进 `~/.workbuddy/skills/`。

装完后补一条软链：

```bash
mkdir -p ~/.workbuddy/skills
ln -sfn ~/.agents/skills/procurement-fold ~/.workbuddy/skills/procurement-fold
```

若本机没有 `~/.agents/skills/procurement-fold`，改为：

```bash
ln -sfn ~/.codex/skills/procurement-fold ~/.workbuddy/skills/procurement-fold
```

## 装完怎么用

对 Agent 说：

```text
用 procurement-fold
```

Skill 会先做商业咨询问答（一次一题），再引导上传产品/公司介绍，再出简易报告。  
**本包不附带知了网 / 世舶 API Key。** 无 Key 也能做问答与简易报告；完整招标拉数、场景拟合、电话补全需要自行配置：

```bash
export ZHILIAO_API_KEY=...
export SHIBO_API_KEY=...
```

完整数据流水线（`kg_engine/fold`）仍在 `procurement-intelligence` 仓库。仅安装本 Skill 时，按 `SKILL.md` 做咨询与简易报告，不要假装已跑通大样本拟合。

## 仓库结构

```text
skills/procurement-fold/   ← 被 skills CLI 发现的 Skill（必须有 SKILL.md）
README.md
```

与 [dbskill](https://github.com/dontbesilent2025/dbskill) 一样：顶层 `skills/<name>/SKILL.md`，`npx skills add` 才能扫到。

## 发布到 GitHub（一次性）

本目录目前在 monorepo 的 `publish/procurement-fold-skill/`。独立公开仓：

https://github.com/ysanfeng8320-coder/procurement-fold-skill

从 monorepo 同步后再推：

```bash
./scripts/sync-from-monorepo.sh
cd publish/procurement-fold-skill   # 若在独立 git 根则省略上层路径
git add . && git commit -m "sync skill" && git push
```

## 从 monorepo 同步

```bash
./scripts/sync-from-monorepo.sh
```

## 许可证

仅供你授权的对象使用；请勿附带任何第三方 API Key 一并分发。
