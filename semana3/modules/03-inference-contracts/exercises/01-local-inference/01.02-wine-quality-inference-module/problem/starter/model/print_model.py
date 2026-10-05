from pathlib import Path

import joblib


MODEL_PATH = Path(__file__).with_name("wine_quality_classifier.joblib")


def main() -> None:
    artifact = joblib.load(MODEL_PATH)
    print(artifact)


if __name__ == "__main__":
    main()