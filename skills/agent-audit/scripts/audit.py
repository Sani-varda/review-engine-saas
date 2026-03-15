#!/usr/bin/env python3
import json
import os
import sys
import glob
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path

MODEL_PRICING = {
    "claude-opus": {"input": 15.0, "output": 75.0, "tier": "complex", "provider": "anthropic"},
    "claude-sonnet": {"input": 3.0, "output": 15.0, "tier": "medium", "provider": "anthropic"},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.0, "tier": "simple", "provider": "anthropic"},
    "claude-haiku": {"input": 0.25, "output": 1.25, "tier": "simple", "provider": "anthropic"},
    "gpt-4.5": {"input": 75.0, "output": 150.0, "tier": "complex", "provider": "openai"},
    "gpt-4o": {"input": 2.5, "output": 10.0, "tier": "medium", "provider": "openai"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "tier": "simple", "provider": "openai"},
    "o1": {"input": 15.0, "output": 60.0, "tier": "complex", "provider": "openai"},
    "o3-mini": {"input": 1.10, "output": 4.40, "tier": "medium", "provider": "openai"},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.0, "tier": "complex", "provider": "google"},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40, "tier": "simple", "provider": "google"},
    "gemini-3-flash": {"input": 0.075, "output": 0.30, "tier": "simple", "provider": "google"},
    "gemini-flash-lite": {"input": 0.025, "output": 0.10, "tier": "simple", "provider": "google"},
    "grok-3": {"input": 3.0, "output": 15.0, "tier": "complex", "provider": "xai"},
    "grok-3-mini": {"input": 0.30, "output": 0.50, "tier": "simple", "provider": "xai"},
}

SIMPLE_PATTERNS = [r"health.?check", r"status", r"monitor", r"ping", r"reminder", r"notify", r"alert", r"heartbeat", r"uptime"]
MEDIUM_PATTERNS = [r"draft", r"research", r"summary", r"analysis", r"report", r"brief", r"scan", r"digest", r"trending", r"scrape"]
COMPLEX_PATTERNS = [r"code", r"build", r"architect", r"security", r"audit", r"review", r"fix", r"debug", r"deploy", r"refactor"]

def find_openclaw_config():
    candidates = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        "/home/ubuntu/.openclaw/openclaw.json",
    ]
    for path in candidates:
        if os.path.exists(path): return path
    return None

def detect_model_pricing(model_string):
    if not model_string: return None
    model_lower = model_string.lower()
    for key, pricing in MODEL_PRICING.items():
        if key in model_lower: return {**pricing, "model_key": key}
    return None

def run_audit():
    config_path = find_openclaw_config()
    if not config_path:
        print("❌ Config not found.")
        return

    with open(config_path) as f:
        config = json.load(f)

    agents = config.get("agents", {})
    if isinstance(agents, dict):
        agent_map = agents.get("list", agents)
    else:
        agent_map = agents

    print("# 🔍 Agent Audit Report")
    print(f"\n**Config:** `{config_path}`")
    
    print("\n## 👥 Agents")
    for k, v in (agent_map.items() if isinstance(agent_map, dict) else enumerate(agent_map)):
        name = v.get("id") or v.get("name") or k
        model = v.get("model") or v.get("defaultModel") or config.get("defaultModel")
        pricing = detect_model_pricing(model)
        tier = pricing["tier"] if pricing else "unknown"
        print(f"### {name}")
        print(f"- **Model:** `{model}`")
        print(f"- **Tier:** {tier}")
        if pricing:
            print(f"- **Cost:** ${pricing['input']}/M in, ${pricing['output']}/M out")
        
        # Recommendation
        if tier == "complex" and any(re.search(p, str(name).lower()) for p in SIMPLE_PATTERNS):
            print(f"⚠️ **Downgrade Recommended:** This looks like a simple task running on a complex model.")

run_audit()
