"""
AgentConfig — settings dataclass for the Strands evaluation runner.

To create a model from this config, use:
    from strands_evaluation.llm.llm_factory import build_model
    model = build_model(config)

Short model names (e.g. "bedrock/claude-sonnet-4.5") are resolved via MODEL_REGISTRY
into the canonical provider string and actual model ID required by the Strands SDK.
They also serve as the key for pricing lookups in helper/constants.py MODEL_PRICING.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple
from strands_evaluation.helper.constants import MODEL_REGISTRY, SYSTEM_PROMPT


def resolve_model(model_name: str) -> Tuple[str, str]:
    """Return (provider, model_id) for a short model name, or raise ValueError."""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model name '{model_name}'. "
            f"Available: {', '.join(MODEL_REGISTRY)}"
        )
    return MODEL_REGISTRY[model_name]


@dataclass
class ConditionConfig:
    condition: str = "baseline"          # "a", "b", or "baseline"
    sparse_backend: str = "bm25"         # "bm25" or "splade" (Condition A)
    enable_traces: bool = False
    trace_output_dir: str = "results/traces"


@dataclass
class RunConfig:
    max_tool_calls: int = 30
    sliding_window_k: int = 40
    timeout_seconds: int = 450
    system_prompt: str = SYSTEM_PROMPT
    tool_executor: str = "sequential"    # or "concurrent"
    condition_config: ConditionConfig = field(default_factory=ConditionConfig)


@dataclass
class AgentConfig:
    # ------------------------------------------------------------------
    # Preferred: pass a short model name from MODEL_REGISTRY, e.g.:
    #   AgentConfig(model_name="bedrock/claude-sonnet-4.5")
    # provider and model_id are resolved automatically.
    #
    # For models not in the registry, set provider + model_id directly.
    # ------------------------------------------------------------------
    model_name: Optional[str] = None          # short canonical key (used for pricing)
    provider: str = "bedrock"
    model_id: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    
    temperature: float = 0.0
    max_tokens: int = 8096
    streaming: bool = False

    bedrock_region: Optional[str] = None      # falls back to AWS_DEFAULT_REGION
    anthropic_api_key: Optional[str] = None   # or set ANTHROPIC_API_KEY
    openai_api_key: Optional[str] = None      # or set OPENAI_API_KEY
    openai_base_url: Optional[str] = None     # for Azure / vLLM / compatible APIs
    gemini_api_key: Optional[str] = None      # or set GEMINI_API_KEY
    ollama_host: str = "http://localhost:11434"
    llama_api_key: Optional[str] = None       # or set LLAMA_API_KEY
    litellm_base_url: Optional[str] = None    # or set LITELLM_BASE_URL
    litellm_api_key: Optional[str] = None     # or set LITELLM_API_KEY
    mistral_api_key: Optional[str] = None     # or set MISTRAL_API_KEY
    cohere_api_key: Optional[str] = None      # or set COHERE_API_KEY
    sagemaker_endpoint: Optional[str] = None  # deployed endpoint name
    sagemaker_region: Optional[str] = None
    writer_api_key: Optional[str] = None      # or set WRITER_API_KEY
    extra_model_kwargs: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.model_name:
            self.provider, self.model_id = resolve_model(self.model_name)

@dataclass
class AurumConfig:
    graph_path:str = "aurum_model"
    db_path:str = "aurum.db"