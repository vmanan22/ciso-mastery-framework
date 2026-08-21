#!/usr/bin/env python3
"""
NVIDIA AI Model Context Protocol (MCP) Server
Allows Antigravity agents to query NVIDIA NIM models on demand via stdio.
"""

import sys
import json
import os
import urllib.request
import urllib.error

NVIDIA_BASE_URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
DEFAULT_API_KEY = None

def get_api_key():
    return os.environ.get("NVIDIA_API_KEY") or os.environ.get("NGC_API_KEY") or DEFAULT_API_KEY

def call_nvidia_chat(prompt: str, model: str = "meta/llama-3.1-70b-instruct", system_prompt: str = None, temperature: float = 0.2, max_tokens: int = 1024):
    api_key = get_api_key()
    url = f"{NVIDIA_BASE_URL}/chat/completions"
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            content = resp_data["choices"][0]["message"]["content"]
            usage = resp_data.get("usage", {})
            return {
                "text": content,
                "model": resp_data.get("model", model),
                "usage": usage
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"NVIDIA API HTTP Error {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"NVIDIA API Request Failed: {str(e)}")

def call_nvidia_list_models():
    api_key = get_api_key()
    url = f"{NVIDIA_BASE_URL}/models"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m["id"] for m in data.get("data", [])]
            return sorted(models)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch models list: {str(e)}")

TOOLS = [
    {
        "name": "nvidia_chat",
        "description": "Generate responses or code using NVIDIA NIM AI models (e.g. meta/llama-3.3-70b-instruct, nvidia/llama-3.1-nemotron-70b-instruct, deepseek-ai/deepseek-r1, mistralai/mistral-large-2-instruct).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The user prompt or query to send to the NVIDIA AI model."
                },
                "model": {
                    "type": "string",
                    "description": "NVIDIA model ID. Examples: 'meta/llama-3.3-70b-instruct', 'nvidia/llama-3.1-nemotron-70b-instruct', 'deepseek-ai/deepseek-r1', 'mistralai/mistral-large-2-instruct'. Default: 'meta/llama-3.3-70b-instruct'."
                },
                "system_prompt": {
                    "type": "string",
                    "description": "Optional system instructions or persona."
                },
                "temperature": {
                    "type": "number",
                    "description": "Sampling temperature between 0.0 and 1.0 (default: 0.2)."
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Maximum tokens in response (default: 1024)."
                }
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "nvidia_list_models",
        "description": "List all available NVIDIA NIM AI foundation models in the NVIDIA catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_message(msg):
    method = msg.get("method")
    msg_id = msg.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "nvidia-ai",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        try:
            if tool_name == "nvidia_chat":
                res = call_nvidia_chat(
                    prompt=args.get("prompt", ""),
                    model=args.get("model", "meta/llama-3.3-70b-instruct"),
                    system_prompt=args.get("system_prompt"),
                    temperature=float(args.get("temperature", 0.2)),
                    max_tokens=int(args.get("max_tokens", 1024))
                )
                output_text = f"**Model:** `{res['model']}`\n\n{res['text']}"
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": output_text}],
                        "isError": False
                    }
                }
            elif tool_name == "nvidia_list_models":
                models = call_nvidia_list_models()
                output_text = f"Found {len(models)} available NVIDIA NIM models:\n\n" + "\n".join([f"- `{m}`" for m in models])
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": output_text}],
                        "isError": False
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                        "isError": True
                    }
                }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error executing {tool_name}: {str(e)}"}],
                    "isError": True
                }
            }
    else:
        if msg_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        return None

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            resp = handle_message(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
