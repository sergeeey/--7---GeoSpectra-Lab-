from cc_toy_lab.radion.potentials import DEFAULT_RADION_PARAMS, find_minimum, potential_b


if __name__ == "__main__":
    print(find_minimum(potential_b, DEFAULT_RADION_PARAMS))
