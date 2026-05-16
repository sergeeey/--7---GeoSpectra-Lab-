from cc_toy_lab.spectral.anderson import run_anderson_sweep


if __name__ == "__main__":
    print(run_anderson_sweep(sizes=[96], disorder_values=[0.5, 30.0], realizations=2))
