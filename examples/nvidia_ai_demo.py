#!/usr/bin/env python3
"""
Example Script: NVIDIA AI / NIM Demonstration
Demonstrates listing models and issuing prompts to NVIDIA NIM foundation models.
Requires NVIDIA_API_KEY environment variable.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nvidia_ai import NvidiaAIClient, nvidia_chat, list_nvidia_models

def main():
    print("=" * 60)
    print("🚀 NVIDIA AI Integration Demonstration")
    print("=" * 60)

    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print("⚠️ NVIDIA_API_KEY not set. Running in dry-run mode.")
        print("To run live: export NVIDIA_API_KEY='nvapi-...'")
        return

    client = NvidiaAIClient()

    print("\n1️⃣ Fetching available models from NVIDIA API Catalog...")
    try:
        models = client.list_models()
        print(f"   ✅ Successfully fetched {len(models)} models.")
        sample_targets = [
            "meta/llama-3.1-70b-instruct",
            "meta/llama-3.1-8b-instruct",
            "meta/llama-3.3-70b-instruct",
            "nvidia/llama-3.1-nemotron-70b-instruct",
            "mistralai/mistral-large-2-instruct",
            "deepseek-ai/deepseek-r1"
        ]
        available_targets = [m for m in sample_targets if m in models]
        print(f"   Key models available: {available_targets}")
    except Exception as e:
        print(f"   ❌ Error fetching models: {e}")

    print("\n2️⃣ Sending prompt to Llama 3.1 70B Instruct...")
    try:
        test_prompt = "Explain the key security advantage of Workload Identity Federation over long-lived Service Account keys in 2 sentences."
        print(f"   Prompt: '{test_prompt}'")
        resp = client.chat_completion(
            model="meta/llama-3.1-70b-instruct",
            messages=[{"role": "user", "content": test_prompt}],
            temperature=0.2,
            max_tokens=256
        )
        print(f"\n   💬 Response:\n{resp}\n")
    except Exception as e:
        print(f"   ❌ Error during chat completion: {e}")

    print("=" * 60)
    print("✅ NVIDIA AI Demo completed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
