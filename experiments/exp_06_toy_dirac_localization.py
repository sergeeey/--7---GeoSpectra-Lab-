import numpy as np

from cc_toy_lab.spectral.toy_dirac import build_toy_dirac_operator


if __name__ == "__main__":
    operator = build_toy_dirac_operator(size=32, mass_disorder=0.1, seed=42)
    print(np.linalg.eigvalsh(operator.toarray())[:6])
