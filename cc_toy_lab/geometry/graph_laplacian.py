from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from sklearn.neighbors import NearestNeighbors


@dataclass(frozen=True)
class GraphLaplacianResult:
    laplacian: sparse.csr_matrix
    weights: sparse.csr_matrix
    epsilon: float
    connected_components: int


def build_knn_graph_laplacian(
    points: np.ndarray,
    k: int = 12,
    epsilon: float | None = None,
    normalized: bool = True,
) -> GraphLaplacianResult:
    """Build a symmetric kNN heat-kernel graph Laplacian.

    This is a numerical approximation, not a proof of continuum convergence.
    """
    if points.ndim != 2:
        raise ValueError("points must be a 2D array")
    n_points = points.shape[0]
    if not (1 < k < n_points):
        raise ValueError("k must be between 2 and number of points - 1")

    nbrs = NearestNeighbors(n_neighbors=k + 1).fit(points)
    distances, indices = nbrs.kneighbors(points)
    local = distances[:, 1:]
    if epsilon is None:
        epsilon = float(np.median(local[:, min(k - 1, max(0, k // 2))]) ** 2)
        epsilon = max(epsilon, 1e-12)

    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    for i in range(n_points):
        for distance, j in zip(distances[i, 1:], indices[i, 1:]):
            rows.append(i)
            cols.append(int(j))
            data.append(float(np.exp(-(distance**2) / (4.0 * epsilon))))

    weights = sparse.coo_matrix((data, (rows, cols)), shape=(n_points, n_points))
    weights = weights.maximum(weights.T).tocsr()
    degree = np.asarray(weights.sum(axis=1)).ravel()
    if normalized:
        inv_sqrt = np.zeros_like(degree)
        mask = degree > 0
        inv_sqrt[mask] = 1.0 / np.sqrt(degree[mask])
        d_inv = sparse.diags(inv_sqrt)
        laplacian = sparse.eye(n_points, format="csr") - d_inv @ weights @ d_inv
    else:
        laplacian = sparse.diags(degree) - weights

    components = sparse.csgraph.connected_components(weights, directed=False, return_labels=False)
    return GraphLaplacianResult(laplacian=laplacian.tocsr(), weights=weights, epsilon=epsilon, connected_components=int(components))


def first_graph_eigenvalues(laplacian: sparse.spmatrix, count: int = 10) -> np.ndarray:
    count = min(count, laplacian.shape[0] - 2)
    values = eigsh(laplacian, k=count, which="SM", return_eigenvectors=False)
    return np.sort(np.real(values))
