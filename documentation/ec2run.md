# EC2 Run

Copy-paste blocks for running evals on an EC2 box.

## One-Command Remote Run

From your laptop, use the wrapper to SSH into the box, activate Python, start a
detached tmux session, and tee output to `run_logs/...`:

```bash
scripts/remote_setup_run.sh full \
  --search ideal \
  --results ideal \
  --plans standard \
  --k 5 \
  --parallel 4 \
  --model openai/gpt-5.4-nano \
  --db lance_data \
  --openai-prompt-cache-retention 24h \
  --verbose \
  --continue \
  --timeout 600 \
  --submit-grace-seconds 30
```

Run SANA through the same SSH/tmux wrapper:

```bash
scripts/remote_setup_run.sh --runner sana --session sana-sprint-k5 full \
  --mode ideal \
  --sana-feature sprint \
  --sprint-mode commitment \
  --k 5 \
  --parallel 4 \
  --model gpt5.4-nano \
  --db lance_data \
  --openai-prompt-cache-key setuprun:v1:tcq:full:gpt5.4-nano:k5:sana-sprint-cadence \
  --openai-prompt-cache-retention 24h \
  --verbose
```

Defaults can be overridden with `--host`, `--repo`, `--venv`, `--session`, and
`--log`, or with `REMOTE_HOST`, `REMOTE_REPO`, and `REMOTE_VENV`. The default
host is `ec2-user@ec2-18-191-139-16.us-east-2.compute.amazonaws.com`, the
default identity is `asw2215.pem`, and the default remote repo is
`~/eval_eqa/exploratory-qa-eval`.

## Pull Outputs Back

The pull helper uses `scp -i asw2215.pem`. If the local target already exists,
it asks whether to move the old directory aside, overwrite it, skip it, or quit.

```bash
scripts/remote_pull_outputs.sh \
  --host ec2-user@ec2-18-191-139-16.us-east-2.compute.amazonaws.com \
  sana-results ./sana-results
```

```bash
scripts/remote_pull_outputs.sh \
  --host ec2-user@ec2-18-221-146-210.us-east-2.compute.amazonaws.com \
  results ./results-ec2
```

Common presets:

```bash
scripts/remote_pull_outputs.sh --preset strands
scripts/remote_pull_outputs.sh --preset sana
```

Use `--backup` to automatically move existing local outputs aside with a
timestamp before copying.

## Session Setup

```bash
cd ~/eval_eqa/exploratory-qa-eval
source .venv/bin/activate
```

Credentials (only if Bedrock inference profile is not already set up):

```bash
./setup_credentials.sh
```

`--plans` controls the planning tool axis. `--skills on` is separate and only attaches the Strands AgentSkills planning/discovery plugin; it defaults to off.

## Smoke Run

```bash
python -m strands_evaluation.setup_run smoke \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data
```

Override the smoke scope:

```bash
python -m strands_evaluation.setup_run smoke \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data \
  --task-dir tasks_core_quality/k-5-d-3
```

## Full Run

```bash
python -m strands_evaluation.setup_run full \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data
```

## Run Detached (survives SSH drops)

Start in tmux, tee output to a log:

```bash
tmux new -s eval -d "python -m strands_evaluation.setup_run full \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data 2>&1 | tee -a run.log"
```

Attach / detach / kill:

```bash
tmux attach -t eval   # detach with Ctrl-b d
tmux kill-session -t eval
```

Or with `nohup`:

```bash
nohup python -m strands_evaluation.setup_run full \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data \
  > run.log 2>&1 &
tail -f run.log
```

## Pull Results Back

From your laptop:

```bash
scripts/remote_pull_outputs.sh --preset strands
```

## Valid `--db` Choices

- `lance_data`
- any custom path
