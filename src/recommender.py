from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from src.data_loader import load_data

df = load_data()

# Keep only useful columns
df = df[["CustomerID", "Description"]]

# Remove empty descriptions
df = df.dropna(subset=["Description"])

# Customer-Product Matrix
customer_product_matrix = pd.crosstab(
    df["CustomerID"],
    df["Description"]
)

# Product similarity
product_similarity = cosine_similarity(
    customer_product_matrix.T
)

product_similarity_df = pd.DataFrame(
    product_similarity,
    index=customer_product_matrix.columns,
    columns=customer_product_matrix.columns
)

def recommend_products(product_name, n=5):

    matches = [
        p for p in product_similarity_df.index
        if product_name.lower() in p.lower()
    ]

    if not matches:
        return ["Product not found"]

    selected_product = matches[0]

    recommendations = (
        product_similarity_df[selected_product]
        .sort_values(ascending=False)
        .iloc[1:n+1]
        .index
        .tolist()
    )

    return recommendations