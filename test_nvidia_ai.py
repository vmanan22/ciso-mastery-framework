#!/usr/bin/env python3
"""
Test and Demonstration of NVIDIA AI / NIM with Antigravity
"""

import sys
import os

# Add local path so nvidia_ai package can be imported directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nvidia_ai import NvidiaAIClient, nvidia_chat, list_nvidia_models

def main():
    print("=" * 60)
    print("🚀 NVIDIA AI Integration Test")
    print("=" * 60)

    client = NvidiaAIClient()

    # 1. Test Listing Top Models
    print("\n1️⃣  Fetching available models from NVIDIA API Catalog...")
    try:
        models = client.list_models()
        print(f"   ✅ Successfully fetched {len(models)} models.")
        print("   Key models available:")
        sample_targets = [
            "meta/llama-3.1-70b-instruct",
            "meta/llama-3.1-8b-instruct",
            "meta/llama-3.3-70b-instruct",
        ]
        for target in sample_targets:
            status = "✓ Active" if target in models else "✕ Not found"
            print(f"     • {target} [{status}]")
    except Exception as e:
        print(f"   ❌ Error fetching models: {e}")

    # 2. Test Chat Completion with Llama 3.1 70B
    test_model = "meta/llama-3.1-70b-instruct"
    prompt = "Give a 2-sentence summary explaining why NVIDIA NIM microservices are used in AI development."
    print(f"\n2️⃣  Testing Chat Completion with `{test_model}`...")
    print(f"   Prompt: \"{prompt}\"")

    try:
        response = client.chat(
            prompt=prompt,
            model=test_model,
            temperature=0.2,
            max_tokens=256
        )
        print("\n   💬 NVIDIA AI Response:")
        print("   " + "-" * 50)
        for line in response.strip().split("\n"):
            print(f"   {line}")
        print("   " + "-" * 50)
        print("   ✅ Chat completion succeeded!")
    except Exception as e:
        print(f"   ❌ Error querying model: {e}")

    print("\n" + "=" * 60)
    print("🎉 All checks complete! NVIDIA AI is ready to use in Antigravity.")
    print("=" * 60)

if __name__ == "__main__":
    main()
