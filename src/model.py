from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

def train_model(df):
    df = df.copy()

    # Feature engineering
    df['cuisine_count'] = df['cuisines'].str.split(',').apply(len)

    X = df[['cost', 'votes', 'cuisine_count']]
    y = df['rate']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X_train, y_train)

    # Score (optional)
    preds = model.predict(X_test)
    print("R2 Score:", r2_score(y_test, preds))

    return model


def predict_rating(model, cost, votes, cuisine_count):
    return model.predict([[cost, votes, cuisine_count]])[0]