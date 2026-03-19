"""
Evaluation Framework for Data Lake Benchmark

This package provides:
- LLM Factory: Unified interface for multiple model providers via Strands
- Agent Tools: Functions for accessing the S3 data lake
- Agent: Strands-native runner for benchmark tasks
- Metrics: Evaluation metrics for comparing answers

Usage:
    from strands_evaluation.agent import DataLakeAgent, BatchRunner, RunConfig
    from strands_evaluation.config import AgentConfig

    # Run single question
    agent = DataLakeAgent(AgentConfig())
    result = agent.run("What is the capital of France?")

    # Run batch evaluation
    from strands_evaluation.agent import BatchRunner
    batch = BatchRunner(AgentConfig())
    results = batch.run_from_files(["tasks/task_1.json", "tasks/task_2.json"])
"""

from .agent import DataLakeAgent, BatchRunner, RunConfig
from .helper.result import AgentResult
from .config import AgentConfig
from .llm.llm_factory import build_model
from .helper.metrics import (
    compute_exact_match,
    compute_f1_score,
    normalize_text,
)

__all__ = [
    # Agent
    "DataLakeAgent",
    "BatchRunner",
    "AgentResult",
    "AgentConfig",
    "RunConfig",
    # LLM
    "build_model",
    # Metrics
    "compute_exact_match",
    "compute_f1_score",
    "normalize_text",
]
