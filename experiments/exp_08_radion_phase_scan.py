import numpy as np

from cc_toy_lab.radion.phase_transition import scan_alpha_transition


if __name__ == "__main__":
    print(scan_alpha_transition(np.linspace(1.25, 1.45, 41)).estimated_alpha_c)
