from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    # Gemini
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    # Behavior
    use_mock_search: bool = os.getenv("USE_MOCK_SEARCH", "true").lower() == "true"
    model_name: str = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    temperature: float = float(os.getenv("TEMPERATURE", "0"))
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "5"))

settings = Settings()
