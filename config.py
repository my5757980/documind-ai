import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

AMD_API_KEY = os.environ.get("AMD_API_KEY", "")
AMD_BASE_URL = os.environ.get("AMD_BASE_URL", "https://api.fireworks.ai/inference/v1")
VISION_MODEL = os.environ.get("VISION_MODEL", "accounts/fireworks/models/kimi-k2p5")
TEXT_MODEL = os.environ.get("TEXT_MODEL", "accounts/fireworks/models/deepseek-v3p1")


def get_amd_llm() -> LLM:
    return LLM(
        model=f"openai/{TEXT_MODEL}",
        base_url=AMD_BASE_URL,
        api_key=AMD_API_KEY,
    )


def get_vision_llm() -> LLM:
    return LLM(
        model=f"openai/{VISION_MODEL}",
        base_url=AMD_BASE_URL,
        api_key=AMD_API_KEY,
    )
