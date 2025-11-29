#!/usr/bin/env python3
"""
Ollama Warmup Script for aia-day2-a Labs
=========================================

This script warms up Ollama models (llama3.2:3b and llama3.2:1b) by running
representative queries for each lab in the workshop.

It ensures models are pulled and ready, then runs sample prompts that mirror
the actual lab exercises to prime the model cache and reduce first-run latency.

Usage:
    python warmup_ollama.py [--models MODEL1 MODEL2 ...] [--quick]
"""

import subprocess
import sys
import time
from typing import List, Dict
import json
import argparse

# ╔══════════════════════════════════════════════════════════════════╗
# │ Configuration                                                      │
# ╚══════════════════════════════════════════════════════════════════╝

DEFAULT_MODELS = ["llama3.2:3b", "llama3.2:1b", "llama3.2"]

# Warmup prompts organized by lab and use case
WARMUP_PROMPTS = {
    "Lab 1 - Weather Agent (LangChain)": [
        {
            "prompt": "You are a helpful weather assistant. What's the weather like in Paris?",
            "context": "Chain of Thought reasoning for location extraction"
        },
        {
            "prompt": "Extract coordinates from: London, UK (51.5074°N, 0.1278°W)",
            "context": "Coordinate extraction pattern"
        },
        {
            "prompt": "Convert 15 degrees Celsius to Fahrenheit and provide a weather summary.",
            "context": "Temperature conversion and summarization"
        }
    ],
    "Lab 2 - Currency Agent (SmolAgents)": [
        {
            "prompt": "Convert 100 USD to EUR. What is the result?",
            "context": "Currency conversion tool calling"
        },
        {
            "prompt": "Remember the last conversion was USD to EUR. Now convert 200.",
            "context": "Memory-based partial input completion"
        },
        {
            "prompt": "Generate Python code to convert currencies using an API.",
            "context": "Code generation for tools"
        }
    ],
    "Lab 3 - RAG Agent (ChromaDB)": [
        {
            "prompt": "Based on this context about OmniTech returns policy: 'Products can be returned within 30 days'. Answer: How long do I have to return a product?",
            "context": "RAG retrieval and grounded generation"
        },
        {
            "prompt": "Follow-up: What about the condition of the product?",
            "context": "Conversation memory and follow-up handling"
        },
        {
            "prompt": "I don't have information about that in the knowledge base. Please ask about returns, shipping, or device troubleshooting.",
            "context": "Out-of-scope query handling"
        }
    ],
    "Lab 4 - Multi-Agent (CrewAI)": [
        {
            "prompt": "You are an Airline Booking Assistant. Extract travel information from: 'I want to fly from New York to Paris on December 15th'",
            "context": "Multi-agent task delegation - customer service"
        },
        {
            "prompt": "You are a Travel Assistant. Find flights from New York to Paris for December 15th. Provide options.",
            "context": "Multi-agent task delegation - travel planning"
        },
        {
            "prompt": "You are a Booking Assistant. Confirm booking for flight BA123 from New York to Paris.",
            "context": "Multi-agent task delegation - booking"
        }
    ],
    "Lab 5 - Reflective Agent (AutoGen)": [
        {
            "prompt": "Write Python code to determine if a number is prime.",
            "context": "Code generation for reflection pattern"
        },
        {
            "prompt": "Review this code and identify any errors: def is_prime(n): return n > 1 and all(n % i != 0 for i in range(2, n))",
            "context": "Code critique and review"
        },
        {
            "prompt": "Fix this code to handle edge cases: def is_prime(n): return n > 1",
            "context": "Code fixing and improvement"
        }
    ]
}

# Quick mode - minimal prompts per lab
QUICK_WARMUP_PROMPTS = {
    "Lab 1 - Weather Agent": [
        {"prompt": "What's the weather in Paris?", "context": "Basic weather query"}
    ],
    "Lab 2 - Currency Agent": [
        {"prompt": "Convert 100 USD to EUR", "context": "Currency conversion"}
    ],
    "Lab 3 - RAG Agent": [
        {"prompt": "Answer based on context: What is the return policy?", "context": "RAG query"}
    ],
    "Lab 4 - Multi-Agent": [
        {"prompt": "Extract travel info from: New York to Paris", "context": "Multi-agent"}
    ],
    "Lab 5 - Reflective Agent": [
        {"prompt": "Write code to check if a number is prime", "context": "Code generation"}
    ]
}

# ╔══════════════════════════════════════════════════════════════════╗
# │ Helper Functions                                                   │
# ╚══════════════════════════════════════════════════════════════════╝

def print_header(text: str, char: str = "="):
    """Print a formatted header."""
    width = 70
    print(f"\n{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}\n")

def print_section(text: str):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}\n")

def check_ollama_running() -> bool:
    """Check if Ollama is running."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def pull_model(model_name: str) -> bool:
    """Pull an Ollama model if not already present."""
    print(f"📥 Checking model: {model_name}")

    # Check if model exists
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if model_name in result.stdout:
            print(f"   ✓ Model {model_name} already available")
            return True
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Timeout checking for {model_name}")
        return False

    # Pull the model
    print(f"   ⬇️  Pulling {model_name} (this may take a few minutes)...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for pulling
        )

        if result.returncode == 0:
            print(f"   ✓ Successfully pulled {model_name}")
            return True
        else:
            print(f"   ✗ Failed to pull {model_name}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ✗ Timeout pulling {model_name}")
        return False

def warmup_model(model_name: str, prompt: str, context: str = "") -> bool:
    """Send a warmup query to the model."""
    try:
        # Show what we're doing
        context_str = f" ({context})" if context else ""
        print(f"   🔥 Warming up: {prompt[:50]}...{context_str}")

        # Run the query
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout per query
        )

        if result.returncode == 0:
            # Don't print the response, just confirm it worked
            response_preview = result.stdout[:80].replace('\n', ' ')
            print(f"      ✓ Response received: {response_preview}...")
            return True
        else:
            print(f"      ✗ Query failed: {result.stderr[:100]}")
            return False

    except subprocess.TimeoutExpired:
        print(f"      ⚠️  Query timeout (model may be slow)")
        return False
    except Exception as e:
        print(f"      ✗ Error: {e}")
        return False

def warmup_all_labs(models: List[str], quick_mode: bool = False, max_per_model: int = 0):
    """Run all warmup prompts for all labs.

    Improvements:
    - Deduplicate prompts so the same prompt isn't sent repeatedly.
    - In quick mode, restrict to the first model to avoid long runs.
    - Allow an optional `max_per_model` cap to limit work per model.
    """
    prompts_map = QUICK_WARMUP_PROMPTS if quick_mode else WARMUP_PROMPTS

    # In quick mode, only use the first model unless user overrides
    if quick_mode and len(models) > 1:
        print("⚡ Quick mode: limiting to first model to speed up warmup")
        models = [models[0]]

    # Build a deduplicated ordered list of prompts (preserve order of appearance)
    seen_prompts = set()
    unique_prompts = []
    for lab_name, lab_prompts in prompts_map.items():
        for item in lab_prompts:
            prompt = item.get("prompt") if isinstance(item, dict) else item
            if prompt is None:
                continue
            if prompt in seen_prompts:
                continue
            seen_prompts.add(prompt)
            unique_prompts.append((lab_name, prompt, item.get("context", "") if isinstance(item, dict) else ""))

    # Apply max_per_model if provided (>0)
    if max_per_model and max_per_model < len(unique_prompts):
        print(f"⚠️  Limiting to {max_per_model} prompts per model (from {len(unique_prompts)})")

    total_queries = len(unique_prompts) * len(models)
    completed = 0
    failed = 0

    print_header("Starting Warmup Queries")
    print(f"Models: {', '.join(models)}")
    print(f"Mode: {'Quick' if quick_mode else 'Full'}")
    print(f"Total queries (approx): {total_queries}")

    for model in models:
        print_section(f"Warming up model: {model}")

        per_model_count = 0
        for lab_name, prompt, context in unique_prompts:
            if max_per_model and per_model_count >= max_per_model:
                break

            print(f"\n🧪 {lab_name}")

            if warmup_model(model, prompt, context):
                completed += 1
            else:
                failed += 1

            per_model_count += 1

            # Small delay between queries
            time.sleep(0.5)

    print_header("Warmup Complete")
    print(f"✓ Completed: {completed}/{total_queries}")
    if failed > 0:
        print(f"✗ Failed: {failed}/{total_queries}")
    print(f"\n🎯 Models are ready for the labs!")

# ╔══════════════════════════════════════════════════════════════════╗
# │ Main Execution                                                     │
# ╚══════════════════════════════════════════════════════════════════╝

def main():
    parser = argparse.ArgumentParser(
        description="Warm up Ollama models for aia-day2-a labs"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help=f"Models to warm up (default: {' '.join(DEFAULT_MODELS)})"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode - minimal warmup prompts"
    )
    parser.add_argument(
        "--no-pull",
        action="store_true",
        help="Skip pulling models (assume they exist)"
    )
    parser.add_argument(
        "--max-per-model",
        type=int,
        default=0,
        help="Maximum prompts to run per model (0 = all, default: 0)"
    )

    args = parser.parse_args()

    print_header("Ollama Warmup Script for aia-day2-a", "=")

    # Step 1: Check Ollama is running
    print("🔍 Checking Ollama status...")
    if not check_ollama_running():
        print("❌ ERROR: Ollama is not running!")
        print("\nPlease start Ollama first:")
        print("   macOS/Linux: ollama serve &")
        print("   Or use the Ollama app")
        sys.exit(1)
    print("✓ Ollama is running\n")

    # Step 2: Pull models
    if not args.no_pull:
        print_section("Pulling Required Models")
        for model in args.models:
            if not pull_model(model):
                print(f"\n❌ ERROR: Could not pull model {model}")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    sys.exit(1)

    # Step 3: Warm up models
    try:
        warmup_all_labs(args.models, args.quick, args.max_per_model)
    except KeyboardInterrupt:
        print("\n\n⚠️  Warmup interrupted by user")
        sys.exit(1)

    # Step 4: Final summary
    print_section("Summary")
    print("Models warmed up and ready:")
    for model in args.models:
        print(f"  ✓ {model}")

    print("\n📚 You can now run the labs:")
    print("   Lab 1: cd agents && python agent1.py")
    print("   Lab 2: cd agents && python curr_conv_agent.py")
    print("   Lab 3: cd agents && python rag_agent.py")
    print("   Lab 4: cd agents && python agent5.py")
    print("   Lab 5: cd agents && python reflect_agent.py")
    print()

if __name__ == "__main__":
    main()
