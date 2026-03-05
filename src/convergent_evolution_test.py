"""
Convergent Evolution Statistical Test
for "Meaning Between Lenses" §1.6

Tests whether the structural isomorphism across 5 independent
cultural indirect speech systems is statistically significant.
"""

import numpy as np
from scipy import stats
from itertools import product

# ============================================================
# §1.6 Isomorphism Encoding Table (from outline v2.8)
# ============================================================
# 5 cultures × 5 parameters
# Each parameter is coded as: +, -, 0, Yes/Partial, High/Med

# Parameters:
# 1. Surface Polarity:    + (positive) vs - (negative) vs 0 (ambiguous)
# 2. Depth Polarity:      - (negative) vs + (positive)
# 3. Full-Channel Align:  Yes vs Partial vs No
# 4. Deniability:         High vs Med vs Low
# 5. Typical Perlocution: misidentification vs compliance vs confusion vs delayed

# The predicted "convergent" pattern = {+Surface, -Depth, Full-Channel Yes, High Deniability}
# = the pattern we expect if convergent evolution is operating

cultures = {
    "British":      {"surface": "+", "depth": "-", "full_channel": "Yes",     "deniability": "High", "perlocution": "misidentification"},
    "Corporate_US": {"surface": "+", "depth": "-", "full_channel": "Yes",     "deniability": "High", "perlocution": "compliance"},
    "Southern_US":  {"surface": "+", "depth": "-", "full_channel": "Yes",     "deniability": "High", "perlocution": "delayed_recognition"},
    "Australian":   {"surface": "0", "depth": "-", "full_channel": "Partial", "deniability": "Med",  "perlocution": "confusion"},
    "Japanese":     {"surface": "+", "depth": "-", "full_channel": "Yes",     "deniability": "High", "perlocution": "misidentification"},
}

# ============================================================
# Test 1: Core Pattern Match (4 binary parameters)
# ============================================================
# The "convergent" signature: {+Surface, -Depth, Full-Channel=Yes, High Deniability}
# We test: how many cultures match this full pattern?

print("=" * 70)
print("CONVERGENT EVOLUTION STATISTICAL TEST")
print("Meaning Between Lenses — §1.6 Isomorphism Analysis")
print("=" * 70)

# Define the convergent pattern
convergent_pattern = {"surface": "+", "depth": "-", "full_channel": "Yes", "deniability": "High"}

# Count matches
full_matches = 0
partial_matches = {}
for culture, params in cultures.items():
    match_count = sum(1 for k, v in convergent_pattern.items() if params[k] == v)
    partial_matches[culture] = match_count
    if match_count == len(convergent_pattern):
        full_matches += 1
    print(f"  {culture:15s}: {match_count}/{len(convergent_pattern)} parameters match convergent pattern")

print(f"\n  Full pattern matches: {full_matches}/5 cultures")

# ============================================================
# Test 2: Binomial Test per Parameter
# ============================================================
print("\n" + "-" * 70)
print("TEST 2: Per-Parameter Binomial Tests")
print("-" * 70)

# For each parameter, what's the probability of seeing k/5 matches
# under the null hypothesis of random assignment?

# Surface polarity: 3 possible values (+, -, 0)
# Under H0: P(+) = 1/3
surface_positive = sum(1 for c in cultures.values() if c["surface"] == "+")
p_surface = stats.binomtest(surface_positive, 5, 1/3, alternative='greater').pvalue
print(f"\n  Surface Polarity = '+': {surface_positive}/5 cultures")
print(f"    H0: P(+) = 1/3 (three options: +, -, 0)")
print(f"    p-value (one-tailed): {p_surface:.6f}")

# Depth polarity: 2 possible values (-, +)
# Under H0: P(-) = 1/2
depth_negative = sum(1 for c in cultures.values() if c["depth"] == "-")
p_depth = stats.binomtest(depth_negative, 5, 1/2, alternative='greater').pvalue
print(f"\n  Depth Polarity = '-': {depth_negative}/5 cultures")
print(f"    H0: P(-) = 1/2 (two options: -, +)")
print(f"    p-value (one-tailed): {p_depth:.4f}")

# Full-channel alignment: 3 possible values (Yes, Partial, No)
# Under H0: P(Yes) = 1/3
full_channel_yes = sum(1 for c in cultures.values() if c["full_channel"] == "Yes")
p_channel = stats.binomtest(full_channel_yes, 5, 1/3, alternative='greater').pvalue
print(f"\n  Full-Channel Alignment = 'Yes': {full_channel_yes}/5 cultures")
print(f"    H0: P(Yes) = 1/3 (three options: Yes, Partial, No)")
print(f"    p-value (one-tailed): {p_channel:.6f}")

# Deniability: 3 possible values (High, Med, Low)
# Under H0: P(High) = 1/3
deniability_high = sum(1 for c in cultures.values() if c["deniability"] == "High")
p_deny = stats.binomtest(deniability_high, 5, 1/3, alternative='greater').pvalue
print(f"\n  Deniability = 'High': {deniability_high}/5 cultures")
print(f"    H0: P(High) = 1/3 (three options: High, Med, Low)")
print(f"    p-value (one-tailed): {p_deny:.6f}")

# ============================================================
# Test 3: Combined Pattern Test (Fisher's method)
# ============================================================
print("\n" + "-" * 70)
print("TEST 3: Combined Pattern — Fisher's Method")
print("-" * 70)

# Fisher's method: combine independent p-values
p_values = [p_surface, p_depth, p_channel, p_deny]
# Fisher's statistic: -2 * sum(ln(p_i)) ~ chi-squared(2k)
fisher_stat = -2 * sum(np.log(p) for p in p_values)
k = len(p_values)
p_combined = 1 - stats.chi2.cdf(fisher_stat, 2 * k)

print(f"\n  Individual p-values: {[f'{p:.6f}' for p in p_values]}")
print(f"  Fisher's statistic: {fisher_stat:.4f}")
print(f"  Degrees of freedom: {2*k}")
print(f"  Combined p-value:   {p_combined:.8f}")

if p_combined < 0.05:
    print(f"\n  ★ SIGNIFICANT at α = 0.05")
    print(f"    The convergent pattern {'{+Surface, -Depth, Full-Channel, High Deniability}'}")
    print(f"    across 5 independent cultural systems is unlikely due to chance.")
else:
    print(f"\n  Not significant at α = 0.05")

# ============================================================
# Test 4: Exact Probability of Observed Pattern
# ============================================================
print("\n" + "-" * 70)
print("TEST 4: Exact Probability of Observed Configuration")
print("-" * 70)

# What's the probability that 4/5 cultures independently evolve
# the EXACT same 4-parameter pattern?
# 
# Each culture has: 3 × 2 × 3 × 3 = 54 possible configurations
# P(specific pattern) = 1/54 per culture
# P(≥4 of 5 match the same pattern):

total_configs = 3 * 2 * 3 * 3  # 54
p_single = 1 / total_configs

# P(exactly k of 5 match) under independence
# First culture sets the pattern, then P(each subsequent matches) = 1/54
# P(all 5 match same pattern) = 54 * (1/54)^5 = (1/54)^4
# P(exactly 4 of 5 match) = 54 * C(5,4) * (1/54)^4 * (53/54)^1
# ... actually let's compute this properly

# P(at least 4 of 5 match a SINGLE specific pattern)
from math import comb

p_exact_5 = p_single ** 4  # first culture sets it, other 4 must match
p_exact_4 = comb(4, 3) * (p_single ** 3) * (1 - p_single) ** 1  # one of remaining 4 deviates

# But we also need to account for any pattern (not just our predicted one)
# P(at least 4 of 5 match ANY single pattern) = 54 × P(at least 4 match THAT pattern)
# since there are 54 possible patterns

p_any_pattern_5_match = total_configs * p_single ** 4
p_any_pattern_4_match = total_configs * comb(4, 3) * p_single ** 3 * (1 - p_single)

# More precisely: P(≥4 of 5 match some common pattern)
# First picks a pattern, other 4 follow
p_at_least_4 = p_any_pattern_5_match + p_any_pattern_4_match

print(f"\n  Total possible parameter configurations per culture: {total_configs}")
print(f"  P(single culture matches specific pattern): {p_single:.4f}")
print(f"\n  P(all 5 cultures match same pattern):     {p_any_pattern_5_match:.8f}")
print(f"  P(exactly 4 of 5 match same pattern):      {p_any_pattern_4_match:.6f}")
print(f"  P(≥4 of 5 match ANY common pattern):       {p_at_least_4:.6f}")

# ============================================================
# Test 5: Monte Carlo Simulation
# ============================================================
print("\n" + "-" * 70)
print("TEST 5: Monte Carlo Simulation (100,000 trials)")
print("-" * 70)

np.random.seed(42)
n_simulations = 100_000

surface_options = ["+", "-", "0"]
depth_options = ["-", "+"]
channel_options = ["Yes", "Partial", "No"]
deniability_options = ["High", "Med", "Low"]

count_4_or_more = 0

for _ in range(n_simulations):
    # Generate 5 random cultures
    configs = []
    for _ in range(5):
        config = (
            np.random.choice(surface_options),
            np.random.choice(depth_options),
            np.random.choice(channel_options),
            np.random.choice(deniability_options),
        )
        configs.append(config)
    
    # Check: do at least 4 share the same configuration?
    from collections import Counter
    config_counts = Counter(configs)
    max_match = config_counts.most_common(1)[0][1]
    
    if max_match >= 4:
        count_4_or_more += 1

p_monte_carlo = count_4_or_more / n_simulations

print(f"\n  Simulations: {n_simulations:,}")
print(f"  Trials with ≥4/5 matching: {count_4_or_more}")
print(f"  Monte Carlo P(≥4 match): {p_monte_carlo:.6f}")
print(f"  95% CI: [{p_monte_carlo - 1.96*np.sqrt(p_monte_carlo*(1-p_monte_carlo)/n_simulations):.6f}, "
      f"{p_monte_carlo + 1.96*np.sqrt(p_monte_carlo*(1-p_monte_carlo)/n_simulations):.6f}]")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  The isomorphism encoding table from §1.6 shows that 4 of 5 
  independently evolved indirect speech systems share the pattern:
  
    {{+Surface, −Depth, Full-Channel Alignment, High Deniability}}
  
  Statistical tests:
  
  1. Per-parameter binomial tests:
     - Surface (+):    p = {p_surface:.4f}  (4/5, H0: 1/3)
     - Depth (-):      p = {p_depth:.4f}  (5/5, H0: 1/2)
     - Full-Channel:   p = {p_channel:.4f}  (4/5, H0: 1/3)
     - Deniability:    p = {p_deny:.4f}  (4/5, H0: 1/3)
  
  2. Fisher's combined p-value: {p_combined:.8f}
  
  3. Exact probability (≥4/5 match any pattern): {p_at_least_4:.6f}
  
  4. Monte Carlo confirmation: {p_monte_carlo:.6f}
  
  Conclusion: The observed convergent pattern is statistically
  significant. The probability of 4+ independent systems 
  converging on the same structural signature by chance is 
  approximately {p_at_least_4*100:.2f}%.
""")

