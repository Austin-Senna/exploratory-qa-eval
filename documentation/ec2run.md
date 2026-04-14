# EC2 Run

Copy-paste blocks for running evals on an EC2 box.

## Session Setup

```bash
cd ~/exploratory-qa-eval
source .venv/bin/activate
```

Credentials (only if Bedrock inference profile is not already set up):

```bash
./setup_credentials.sh
```

## Smoke Run

```bash
python -m strands_evaluation.setup_run smoke \
  --search ideal \
  --results ideal \
  --plan ideal \
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
  --plan ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data \
  --task-dir tasks_mini/k-5-d-3
```

## Full Run

```bash
python -m strands_evaluation.setup_run full \
  --search ideal \
  --results ideal \
  --plan ideal \
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
  --plan ideal \
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
  --plan ideal \
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
scp -r ec2:~/exploratory-qa-eval/results ./results-ec2
scp -r ec2:~/exploratory-qa-eval/logs    ./logs-ec2
```

## Valid `--db` Choices

- `lance_data`
- any custom path
