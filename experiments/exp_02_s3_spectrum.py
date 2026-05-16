from cc_toy_lab.geometry.analytic_spectra import sphere_laplacian_eigenvalue


if __name__ == "__main__":
    print([sphere_laplacian_eigenvalue(3, ell) for ell in range(5)])
