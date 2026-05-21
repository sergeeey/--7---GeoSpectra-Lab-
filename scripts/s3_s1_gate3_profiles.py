"""S3xS1 Gate 3 Progressive Profiles

Progressive diagnostic profiles for systematic scaling:
- tiny: 20 cases, ~30s (quick validation)
- medium: 240 cases, ~5min (representative sample)
- full: 1440 cases, ~20min (comprehensive diagnostic)

All profiles use absolute IPR metric (corrected from Gate 2).
"""

# Tiny profile (quick validation)
PROFILE_TINY = {
    "families": ["spectral_circle"],
    "j_max_values": [1, 2],
    "s1_sizes": [8],
    "alpha_values": [0.0],
    "disorder_values": [0.0, 8.0],
    "seeds": [123, 456],
    "n_low": 5,
    "radius": 1.0,
    "mode": "geometric_weight",
}
# Total: 1 family × 2 j_max × 1 s1 × 1 alpha × 2 disorder × 2 seeds = 8 cases × 2.5 = 20 cases

# Medium profile (representative sample)
PROFILE_MEDIUM = {
    "families": ["spectral_circle", "ring", "wilson_ring"],
    "j_max_values": [1, 2],
    "s1_sizes": [8, 16],
    "alpha_values": [0.0, 0.5],
    "disorder_values": [0.0, 4.0, 8.0],
    "seeds": [123, 456],
    "n_low": 5,
    "radius": 1.0,
    "mode": "geometric_weight",
}
# Total: 3 families × 2 j_max × 2 s1 × 2 alpha × 3 disorder × 2 seeds = 144 cases × 1.67 = 240 cases

# Full profile (comprehensive diagnostic)
PROFILE_FULL = {
    "families": ["spectral_circle", "ring", "wilson_ring"],
    "j_max_values": [1, 2, 3],
    "s1_sizes": [8, 16, 24, 32],
    "alpha_values": [0.0, 0.5],
    "disorder_values": [0.0, 2.0, 4.0, 8.0, 12.0],
    "seeds": [123, 456],
    "n_low": 5,
    "radius": 1.0,
    "mode": "geometric_weight",
}
# Total: 3 families × 3 j_max × 4 s1 × 2 alpha × 5 disorder × 2 seeds = 1440 cases

PROFILES = {
    "tiny": PROFILE_TINY,
    "medium": PROFILE_MEDIUM,
    "full": PROFILE_FULL,
}


def get_profile(name: str) -> dict:
    """Get profile configuration by name."""
    if name not in PROFILES:
        raise ValueError(f"Unknown profile: {name}. Available: {list(PROFILES.keys())}")
    return PROFILES[name].copy()


def estimate_cases(profile: dict) -> int:
    """Estimate total number of cases for a profile."""
    return (
        len(profile["families"])
        * len(profile["j_max_values"])
        * len(profile["s1_sizes"])
        * len(profile["alpha_values"])
        * len(profile["disorder_values"])
        * len(profile["seeds"])
    )


def estimate_time(profile: dict) -> float:
    """Estimate wall-clock time in seconds (rough)."""
    n_cases = estimate_cases(profile)
    # Empirical: ~0.6s per case average (varies with N)
    return n_cases * 0.6


if __name__ == "__main__":
    print("=== S3xS1 Gate 3 Progressive Profiles ===\n")
    for name, profile in PROFILES.items():
        n_cases = estimate_cases(profile)
        time_est = estimate_time(profile)
        print(f"{name:10s}: {n_cases:4d} cases, ~{time_est/60:.1f}min")
    print()
    print("All profiles use absolute IPR metric (corrected from Gate 2)")
