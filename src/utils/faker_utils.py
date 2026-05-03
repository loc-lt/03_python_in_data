import random
from pathlib import Path

from faker import Faker
import numpy as np

from src.config import RANDOM_SEED


def build_faker() -> Faker:
    fake = Faker()
    Faker.seed(RANDOM_SEED)
    return fake


def seed_everything() -> None:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
