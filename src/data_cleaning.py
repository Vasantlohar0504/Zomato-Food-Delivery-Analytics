import pandas as pd
import numpy as np

def add_fake_coordinates(df):
    import numpy as np

    # Bangalore latitude & longitude range
    np.random.seed(42)
    df['lat'] = np.random.uniform(12.90, 13.10, len(df))
    df['lon'] = np.random.uniform(77.50, 77.70, len(df))

    return df


def clean_data(file_path):
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    column_map = {
        'approx_cost(for_two_people)': 'cost',
        'listed_in(city)': 'location'
    }
    df.rename(columns=column_map, inplace=True)

    df = df[['name', 'location', 'rate', 'votes', 'cost', 'cuisines']]

    df.drop_duplicates(inplace=True)

    df['rate'] = df['rate'].astype(str).str.replace('/5', '')
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

    df['cost'] = df['cost'].astype(str).str.replace(',', '')
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')

    df.dropna(inplace=True)

    # 🔥 Add coordinates
    df = add_fake_coordinates(df)

    return df


def save_cleaned_data(input_path, output_path):
    df = clean_data(input_path)

    if len(df) > 10000:
        df = df.sample(10000, random_state=42)

    df.to_csv(output_path, index=False)
    print("✅ Cleaned dataset with coordinates saved!")