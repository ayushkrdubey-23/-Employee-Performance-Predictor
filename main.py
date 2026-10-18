"""
Employee Performance Predictor - Main Entry Point
Runs the full pipeline: data generation -> preprocessing -> training -> evaluation -> prediction
"""

from src.generate_data import generate_dataset
from src.preprocess import preprocess_data
from src.train_model import train_models
from src.evaluate import evaluate_model
from src.predict import predict_performance


def main():
    print("=" * 60)
    print("Employee Performance Predictor - Pipeline")
    print("=" * 60)

    # Phase 2: Data Creation
    print("\n[Phase 2] Generating synthetic HR dataset...")
    generate_dataset()

    # Phase 3: Data Cleaning
    print("\n[Phase 3] Preprocessing and cleaning data...")
    preprocess_data()

    # Phase 5 & 6: Feature Engineering + Model Building
    print("\n[Phase 5-6] Feature engineering and model training...")
    train_models()

    # Phase 7: Evaluation
    print("\n[Phase 7] Evaluating model...")
    evaluate_model()

    # Phase 7: Prediction on new data
    print("\n[Phase 7] Making predictions on new employee data...")
    predict_performance()

    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
