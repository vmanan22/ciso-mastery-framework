---
name: nvidia-ai
description: Guide and tools for utilizing NVIDIA AI / NVIDIA NIM (Inference Microservices) models within Antigravity, including Meta Llama 3.3 70B, NVIDIA Nemotron, DeepSeek R1, and Mistral.
---

# NVIDIA AI Integration in Antigravity

This workspace is configured with access to NVIDIA NIM cloud models via the NVIDIA API Catalog (`https://integrate.api.nvidia.com/v1`).

## 1. Available Tools & Components

- **MCP Server**: Defined in `mcp_config.json` pointing to `.agents/mcp/nvidia_mcp_server.py`.
- **Python Client**: Importable directly via `from nvidia_ai import NvidiaAIClient, nvidia_chat, list_nvidia_models`.
- **Verification Script**: `test_nvidia_ai.py`

## 2. Supported Models

| Model | ID | Best For |
|---|---|---|
| **Llama 3.3 70B** | `meta/llama-3.3-70b-instruct` | General coding, reasoning, agentic tasks |
| **NVIDIA Nemotron 70B** | `nvidia/llama-3.1-nemotron-70b-instruct` | Complex reasoning, synthetic data, evaluation |
| **DeepSeek R1** | `deepseek-ai/deepseek-r1` | Deep step-by-step reasoning, mathematical logic |
| **Mistral Large 2** | `mistralai/mistral-large-2-instruct` | Multilingual coding, structured output |

## 3. Quick Python Usage

```python
from nvidia_ai import nvidia_chat

response = nvidia_chat(
    prompt="Explain gradient descent in 3 bullet points.",
    model="meta/llama-3.3-70b-instruct",
    temperature=0.2
)
print(response)
```

## 4. Environment Variables

- `NVIDIA_API_KEY`: Authentication key for NVIDIA API Catalog (saved in `~/.zshrc`).
- `NGC_API_KEY`: Alias for NVIDIA GPU Cloud access.
