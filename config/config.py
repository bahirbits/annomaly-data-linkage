"""
Project configuration with essential paths and settings
"""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

@dataclass
class Config:
    """Central project configuration"""
    
    # Core paths
    ROOT_DIR: Path = Path(__file__).parent.parent
    DATA_RAW: Path = ROOT_DIR / "data/raw/csv"
    DATA_PROCESSED: Path = ROOT_DIR / "data/processed"
    ARTIFACTS: Path = ROOT_DIR / "artifacts"
    MODELS: Path = ROOT_DIR / "models"
    LOGS: Path = ROOT_DIR / "logs"
    
    # Environment settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    VERSION: str = os.getenv("VERSION", "0.0.1")
    
    
    def __post_init__(self):
        """Ensure directories exist"""
        for path in [self.DATA_RAW, self.DATA_PROCESSED, 
                    self.ARTIFACTS, self.MODELS, self.LOGS]:
            path.mkdir(parents=True, exist_ok=True)

# Instantiate configuration
config = Config()

if __name__ == "__main__":
    print("Project configuration:")
    print(f"Version: {config.VERSION}")
    print(f"Root directory: {config.ROOT_DIR}")
    print(f"Debug mode: {config.DEBUG}")