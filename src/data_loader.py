import pandas as pd

def load_data():
    df = pd.read_csv(
        "data/OnlineRetail.csv",
        encoding="latin1"
    )

    df = df.dropna(subset=["CustomerID"])

    return df