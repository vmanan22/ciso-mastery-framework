"""
NVIDIA AI / NIM Client
Zero-dependency client library to interact with NVIDIA NIM Cloud & Self-Hosted endpoints.
"""

import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

DEFAULT_NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "meta/llama-3.1-70b-instruct"
DEFAULT_API_KEY = None

POPULAR_MODELS = [
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.3-70b-instruct",
]


class NvidiaAIClient:
    """Client for interacting with NVIDIA AI Inference Microservices (NIM)."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = (
            api_key
            or os.environ.get("NVIDIA_API_KEY")
            or os.environ.get("NGC_API_KEY")
            or DEFAULT_API_KEY
        )
        self.base_url = (
            base_url
            or os.environ.get("NVIDIA_BASE_URL")
            or DEFAULT_NVIDIA_BASE_URL
        ).rstrip("/")

        if not self.api_key:
            raise ValueError(
                "NVIDIA API Key not found. Set NVIDIA_API_KEY in environment or pass api_key parameter."
            )

    def chat(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        top_p: float = 0.7,
        stream: bool = False,
    ) -> str:
        """
        Send a chat completion request to the specified NVIDIA AI model.
        
        Args:
            prompt: The message/query for the model.
            model: Model identifier (e.g., 'meta/llama-3.3-70b-instruct', 'nvidia/llama-3.1-nemotron-70b-instruct').
            system_prompt: Optional system prompt to instruct the model.
            temperature: Randomness control (0.0 to 1.0).
            max_tokens: Maximum tokens in generated response.
            top_p: Nucleus sampling probability.
            stream: Whether to stream tokens (default: False).
            
        Returns:
            The model's text response.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": stream,
        }

        url = f"{self.base_url}/chat/completions"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"NVIDIA API HTTP Error {e.code}: {err}")
        except Exception as e:
            raise RuntimeError(f"NVIDIA API Request Failed: {str(e)}")

    def list_models(self) -> List[str]:
        """Fetch all available models from the NVIDIA catalog."""
        url = f"{self.base_url}/models"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return sorted([m["id"] for m in data.get("data", [])])
        except Exception as e:
            raise RuntimeError(f"Failed to list NVIDIA models: {str(e)}")


def nvidia_chat(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> str:
    """Convenience helper function to quickly query NVIDIA AI."""
    client = NvidiaAIClient()
    return client.chat(
        prompt=prompt,
        model=model,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def list_nvidia_models() -> List[str]:
    """Convenience helper function to list available models."""
    client = NvidiaAIClient()
    return client.list_models()
