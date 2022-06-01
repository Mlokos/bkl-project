from typing import List
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pandas import DataFrame
import matplotlib.pyplot as plt


KMEANS_KWARGS = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}


def show_clusters_grouping_score(df: DataFrame) -> None:
    df = df.dropna()
    # 5 is a maximum score
    scaled_features = df / 5

    silhouette_coefficients = []
    for k in range(2, len(scaled_features.index)):
        kmeans = KMeans(n_clusters=k, **KMEANS_KWARGS)
        kmeans.fit(scaled_features)
        score = silhouette_score(scaled_features, kmeans.labels_)
        silhouette_coefficients.append(score)

    plt.plot(range(2, len(scaled_features.index)), silhouette_coefficients)
    plt.xticks(range(2, len(scaled_features.index)))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()


def get_clusters(n_clusters: int, df: DataFrame) -> DataFrame:
    # 5 is a maximum score
    scaled_features = df / 5

    kmeans = KMeans(n_clusters=n_clusters, **KMEANS_KWARGS)
    kmeans.fit(scaled_features)
    df = df.assign(cluster_type=kmeans.labels_)

    return df


def show_clusters(df: DataFrame) -> None:
    for cluster in df.cluster_type.unique():
        job_title_group = df[df.cluster_type == cluster]
        del job_title_group["cluster_type"]
        plt.imshow(job_title_group, cmap="RdYlGn", vmin=1, vmax=5)
        plt.colorbar()
        plt.yticks(range(len(job_title_group)), job_title_group.index)
        plt.show()
