from src.data_loader import load_data

df = load_data()

def get_stats():
    return {
        "products": df["Description"].nunique(),
        "customers": df["CustomerID"].nunique(),
        "transactions": len(df),
        "countries": df["Country"].nunique()
    }

def top_products():
    return (
        df["Description"]
        .value_counts()
        .head(10)
    )

def top_countries():
    return (
        df["Country"]
        .value_counts()
        .head(10)
    )