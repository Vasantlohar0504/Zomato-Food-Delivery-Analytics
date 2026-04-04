import pandas as pd

def load_data(path):
    return pd.read_csv(path)


def get_top_cuisines(df):
    cuisines = df['cuisines'].str.split(',').explode()
    return cuisines.value_counts().head(10)


def get_top_locations(df):
    return df['location'].value_counts().head(10)


def rating_distribution(df):
    return df['rate'].value_counts().sort_index()


def cost_rating_relation(df):
    return df[['cost', 'rate']]