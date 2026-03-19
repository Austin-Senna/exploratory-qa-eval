"""
LLM Factory - Creates Strands model objects from an AgentConfig.

Supported providers (set AgentConfig.provider to one of these strings):
    "bedrock"       Amazon Bedrock — needs AWS credentials in env
    "anthropic"     Anthropic API — needs ANTHROPIC_API_KEY
    "openai"        OpenAI API — needs OPENAI_API_KEY
    "gemini"        Google Gemini — needs GEMINI_API_KEY
    "ollama"        Ollama local server — needs ollama running at ollama_host
    "llamaapi"      LlamaAPI — needs LLAMA_API_KEY
    "litellm"       LiteLLM proxy — needs LITELLM_BASE_URL + LITELLM_API_KEY
    "mistral"       MistralAI — needs MISTRAL_API_KEY
    "cohere"        Cohere — needs COHERE_API_KEY
    "sagemaker"     Amazon SageMaker — needs AWS credentials + endpoint name
    "writer"        Writer AI — needs WRITER_API_KEY

Usage:
    from strands_evaluation.config import AgentConfig
    from strands_evaluation.llm.llm_factory import build_model

    model = build_model(AgentConfig(provider="bedrock", model_id="..."))

    from strands import Agent
    agent = Agent(model=model, tools=[...])
"""

import os
from typing import Any

from strands_evaluation.config import AgentConfig


def build_model(config: AgentConfig) -> Any:
    """Instantiate and return a Strands model object for the given config."""
    p = config.provider.lower()

    builders = {
        "bedrock":    _build_bedrock,
        "anthropic":  _build_anthropic,
        "openai":     _build_openai,
        "gemini":     _build_gemini,
        "ollama":     _build_ollama,
        "llamaapi":   _build_llamaapi,
        "litellm":    _build_litellm,
        "mistral":    _build_mistral,
        "cohere":     _build_cohere,
        "sagemaker":  _build_sagemaker,
        "writer":     _build_writer,
    }

    if p not in builders:
        raise ValueError(
            f"Unknown provider '{config.provider}'. "
            f"Choose one of: {', '.join(builders)}"
        )

    return builders[p](config)


# ---------------------------------------------------------------------------
# Provider builders
# ---------------------------------------------------------------------------

def _build_bedrock(c: AgentConfig) -> Any:
    # Requires: AWS credentials (env vars, IAM role, or ~/.aws/credentials)
    # Optional: AWS_DEFAULT_REGION (defaults to us-east-1)
    from strands.models import BedrockModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        streaming=c.streaming,
        **c.extra_model_kwargs,
    )
    if c.bedrock_region:
        kwargs["region_name"] = c.bedrock_region
    return BedrockModel(**kwargs)


def _build_anthropic(c: AgentConfig) -> Any:
    # Requires: ANTHROPIC_API_KEY env var (or AgentConfig.anthropic_api_key)
    from strands.models.anthropic import AnthropicModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    api_key = c.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    return AnthropicModel(**kwargs)


def _build_openai(c: AgentConfig) -> Any:
    # Requires: OPENAI_API_KEY env var (or AgentConfig.openai_api_key)
    # Optional: AgentConfig.openai_base_url for Azure / vLLM / other compatible APIs
    from strands.models.openai import OpenAIModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    api_key = c.openai_api_key or os.getenv("OPENAI_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    if c.openai_base_url:
        kwargs["base_url"] = c.openai_base_url
    return OpenAIModel(**kwargs)


def _build_gemini(c: AgentConfig) -> Any:
    # Requires: GEMINI_API_KEY env var (or AgentConfig.gemini_api_key)
    from strands.models.gemini import GeminiModel

    api_key = c.gemini_api_key or os.getenv("GEMINI_API_KEY")
    kwargs = dict(
        model_id=c.model_id,
        params={"temperature": c.temperature, "max_output_tokens": c.max_tokens},
        client_args={"api_key": api_key} if api_key else {},
        **c.extra_model_kwargs,
    )
    return GeminiModel(**kwargs)


def _build_ollama(c: AgentConfig) -> Any:
    # Requires: Ollama server running at AgentConfig.ollama_host (default localhost:11434)
    # Pull the model first: `ollama pull <model_id>`
    from strands.models.ollama import OllamaModel

    kwargs = dict(
        host=c.ollama_host,
        model_id=c.model_id,
        **c.extra_model_kwargs,
    )
    return OllamaModel(**kwargs)


def _build_llamaapi(c: AgentConfig) -> Any:
    # Requires: LLAMA_API_KEY env var (or AgentConfig.llama_api_key)
    from strands.models.llamaapi import LlamaAPIModel

    kwargs = dict(
        model_id=c.model_id,
        **c.extra_model_kwargs,
    )
    api_key = c.llama_api_key or os.getenv("LLAMA_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    return LlamaAPIModel(**kwargs)


def _build_litellm(c: AgentConfig) -> Any:
    # Requires: LITELLM_BASE_URL + LITELLM_API_KEY env vars
    #           (or AgentConfig.litellm_base_url / litellm_api_key)
    from strands.models.litellm import LiteLLMModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    base_url = c.litellm_base_url or os.getenv("LITELLM_BASE_URL")
    api_key = c.litellm_api_key or os.getenv("LITELLM_API_KEY")
    if base_url:
        kwargs["base_url"] = base_url
    if api_key:
        kwargs["api_key"] = api_key
    return LiteLLMModel(**kwargs)


def _build_mistral(c: AgentConfig) -> Any:
    # Requires: MISTRAL_API_KEY env var (or AgentConfig.mistral_api_key)
    from strands.models.mistral import MistralModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    api_key = c.mistral_api_key or os.getenv("MISTRAL_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    return MistralModel(**kwargs)


def _build_cohere(c: AgentConfig) -> Any:
    # Requires: COHERE_API_KEY env var (or AgentConfig.cohere_api_key)
    from strands.models.cohere import CohereModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    api_key = c.cohere_api_key or os.getenv("COHERE_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    return CohereModel(**kwargs)


def _build_sagemaker(c: AgentConfig) -> Any:
    # Requires: AWS credentials + AgentConfig.sagemaker_endpoint (endpoint name)
    from strands.models.sagemaker import SageMakerModel

    if not c.sagemaker_endpoint:
        raise ValueError("AgentConfig.sagemaker_endpoint must be set for the sagemaker provider")
    kwargs = dict(
        endpoint_name=c.sagemaker_endpoint,
        **c.extra_model_kwargs,
    )
    if c.sagemaker_region:
        kwargs["region_name"] = c.sagemaker_region
    return SageMakerModel(**kwargs)


def _build_writer(c: AgentConfig) -> Any:
    # Requires: WRITER_API_KEY env var (or AgentConfig.writer_api_key)
    from strands.models.writer import WriterModel

    kwargs = dict(
        model_id=c.model_id,
        temperature=c.temperature,
        max_tokens=c.max_tokens,
        **c.extra_model_kwargs,
    )
    api_key = c.writer_api_key or os.getenv("WRITER_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    return WriterModel(**kwargs)
