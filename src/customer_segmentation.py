from sklearn.cluster import KMeans
from src.data_loader import load_data

df = load_data()

customer_data = df.groupby("CustomerID").agg({
    "Quantity": "sum",
    "UnitPrice": "mean"
})

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

customer_data["Cluster"] = kmeans.fit_predict(
    customer_data
)

def get_cluster_counts():
    return customer_data["Cluster"].value_counts()