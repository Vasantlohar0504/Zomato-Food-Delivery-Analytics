from src.data_cleaning import save_cleaned_data

INPUT_PATH = "data/raw/zomato.csv"
OUTPUT_PATH = "data/processed/zomato_cleaned_sample.csv"

if __name__ == "__main__":
    print("🔄 Cleaning data...")

    save_cleaned_data(INPUT_PATH, OUTPUT_PATH)

    print("✅ Data cleaning completed!")