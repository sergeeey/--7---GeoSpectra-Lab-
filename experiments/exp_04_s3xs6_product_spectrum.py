from cc_toy_lab.geometry.analytic_spectra import product_spectrum


if __name__ == "__main__":
    for row in product_spectrum(3, 6, 2, 2)[:8]:
        print(row)
