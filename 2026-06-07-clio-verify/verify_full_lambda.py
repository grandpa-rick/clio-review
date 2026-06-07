"""
Cross-check Clio's negative finding: Im G_λ = 0 fails to single out (2,2)
in general (not two-row). Use the formula

  G_λ(i) = sum_{k=0}^m C(m,k) i^k N_{λ,k},   N_{λ,k} = <s_λ, h_2^{m-k} e_2^k>

Compute N_{λ,k} for small λ ⊢ 2m via direct Hall inner product:
  <s_λ, h_2^{m-k} e_2^k> = K_{λ, (2^{m-k}, 1^{2k}_paired)} — actually:
  h_2^{m-k} e_2^k = Σ_μ <h_2^{m-k} e_2^k, s_μ> s_μ, then <s_λ, ...> = Kostka-like.

Simpler: compute h_2^{m-k} e_2^k in power-sum basis or directly expand:
   h_2 = (p_1^2 + p_2)/2
   e_2 = (p_1^2 - p_2)/2
Use sympy.combinatorics with Newton's identities, or expand explicitly.

For brevity, I'll just verify (4,2,2) ⊢ 8 (m=4) has G_{(4,2,2)}(i) imag part = 0.
"""
import sympy as sp
from sympy.combinatorics import Permutation
from sympy.functions.combinatorial.numbers import nC

# Use sympy's symmetric_function support? Manual via power-sums.
# p_1 = e_1, p_2 = e_1^2 - 2 e_2; or use Newton.
# Actually let's compute N_{λ,k} via Kostka numbers:
#   h_2^{m-k} e_2^k = Σ_μ <h_2^{m-k} e_2^k, s_μ> s_μ
# Since e_2 = ω(h_2) where ω is the involution s_λ → s_{λ'}:
#   h_2^{m-k} e_2^k corresponds to a product. The coefficient of s_λ is:
#   number of ways to fill λ with a horizontal-2-strip tableau of m-k 2's and
#   vertical-2-strip tableau of k 2's combined? This is iterated Pieri.

# Use the iterated Pieri (LR) computation. Define multiplication of Schur by h_2 and e_2.

def schur_times_h2(sf_dict):
    """sf_dict: dict (partition tuple) → coefficient. Multiply by h_2 (horizontal 2-strip)."""
    result = {}
    for mu, c in sf_dict.items():
        # add horizontal 2-strip to mu
        for new in add_horizontal_strip(mu, 2):
            result[new] = result.get(new, 0) + c
    return result

def schur_times_e2(sf_dict):
    """Multiply by e_2 (vertical 2-strip)."""
    result = {}
    for mu, c in sf_dict.items():
        for new in add_vertical_strip(mu, 2):
            result[new] = result.get(new, 0) + c
    return result

def add_horizontal_strip(mu, size):
    """Yield all partitions ν ⊃ μ with ν/μ a horizontal strip of size `size`.
    A horizontal strip has at most one box in each column.
    """
    # Pad mu with zeros
    mu = list(mu) + [0]
    # Pieri rule: ν_1 ≥ μ_1 ≥ ν_2 ≥ μ_2 ≥ ... ≥ ν_{l+1} ≥ μ_{l+1} = 0
    # and Σ ν_i = Σ μ_i + size.
    # Enumerate.
    L = len(mu)
    results = []
    def recurse(i, nu_so_far, remaining):
        if remaining < 0:
            return
        if i == L:
            if remaining == 0:
                # trim trailing zeros
                nu = tuple(x for x in nu_so_far if x > 0)
                results.append(nu)
            return
        # ν_{i+1} can be from μ_{i+1} up to (nu_so_far[-1] if any else infinity, but bounded above by μ_i)
        mu_i = mu[i]
        upper = mu[i-1] if i > 0 else float('inf')
        if i == 0:
            # ν_1 ≥ μ_1, also ν_1 ≥ ν_2 (recursion handles by upper for next)
            # Upper bound: anything (since μ_0 doesn't exist)
            upper_bound = mu_i + remaining
        else:
            upper_bound = min(nu_so_far[i-1], mu_i + remaining) if False else mu[i-1]  # ν_{i+1} ≤ ν_i (but ν_i = nu_so_far[i-1])
            upper_bound = nu_so_far[i-1] if nu_so_far else mu_i + remaining
        # Cleaner: ν_{i+1} in [μ_{i+1}, ν_i] (and ν_0 = ∞)
        prev_nu = nu_so_far[-1] if nu_so_far else None
        # Wait — Pieri: ν_1 ≥ μ_1 ≥ ν_2 ≥ μ_2 ≥ ν_3 ≥ ...
        # So for i=0 (computing ν_1): bound is ≥ μ_1 = mu[0], upper bounded by sum constraint and prev (none)
        # For i=1 (computing ν_2): bound is in [μ_2, μ_1] = [mu[1], mu[0]]
        if i == 0:
            low = mu_i
            high = mu_i + remaining
        else:
            low = mu_i
            high = mu[i-1]
            # also ν_{i+1} ≤ ν_i which is nu_so_far[i-1]
            high = min(high, nu_so_far[i-1])
        for nu_val in range(low, high + 1):
            add = nu_val - mu_i
            if add > remaining:
                continue
            recurse(i + 1, nu_so_far + [nu_val], remaining - add)
    recurse(0, [], size)
    return set(results)

def add_vertical_strip(mu, size):
    """A vertical strip: at most one box per row."""
    # Pieri: ν_1 ≥ μ_1 ≥ ν_2 - 1 if added box in row 2... actually:
    # Vertical strip: ν/μ has at most one box per row. So ν_i - μ_i ∈ {0, 1} for all i (and add 1 in `size` rows).
    L_max = len(mu) + size + 1
    mu = list(mu) + [0] * (L_max - len(mu))
    results = []
    # ν_i = μ_i + ε_i, ε_i ∈ {0, 1}, sum ε_i = size, ν_1 ≥ ν_2 ≥ ...
    def recurse(i, nu_so_far, used, ε_left):
        if ε_left < 0:
            return
        if i == L_max:
            if ε_left == 0:
                nu = tuple(x for x in nu_so_far if x > 0)
                results.append(nu)
            return
        for ε in (0, 1):
            new_val = mu[i] + ε
            if nu_so_far and new_val > nu_so_far[-1]:
                continue
            if ε > ε_left:
                continue
            recurse(i + 1, nu_so_far + [new_val], used + (1 if ε else 0), ε_left - ε)
    recurse(0, [], 0, size)
    return set(results)

def coefficient_of_s_lambda(λ, target_size, mults):
    """mults: list of ('h2' or 'e2') in some order. Compute coefficient of s_λ."""
    sf = {(): 1}  # s_∅ = 1
    for op in mults:
        if op == 'h2':
            sf = schur_times_h2(sf)
        else:
            sf = schur_times_e2(sf)
    return sf.get(tuple(λ), 0)

def N_lambda_k(λ, m, k):
    """N_{λ,k} = <s_λ, h_2^{m-k} e_2^k>. Order doesn't matter (commute)."""
    ops = ['h2'] * (m - k) + ['e2'] * k
    return coefficient_of_s_lambda(λ, sum(λ), ops)

def G_lambda(λ, m):
    """G_λ(i) = sum_k C(m,k) i^k N_{λ,k}."""
    re_part = 0
    im_part = 0
    for k in range(m + 1):
        N = N_lambda_k(λ, m, k)
        c = sp.binomial(m, k) * N
        # i^k pattern: k=0 → 1, k=1 → i, k=2 → -1, k=3 → -i, ...
        if k % 4 == 0:
            re_part += c
        elif k % 4 == 1:
            im_part += c
        elif k % 4 == 2:
            re_part -= c
        else:
            im_part -= c
    return int(sp.simplify(re_part)), int(sp.simplify(im_part))

# Test cases from Clio's findings:
test_cases = [
    ((2, 2), 2, "expected G = 0"),
    ((2, 2, 1, 1), 3, "expected Im=0, Re != 0"),
    ((4, 2, 2), 4, "expected Im=0, Re != 0"),
    ((3, 3, 2), 4, "expected Im=0, Re != 0"),
    ((3, 3, 1, 1), 4, "expected Im=0, Re != 0"),
    ((4, 2, 1, 1), 4, "expected Im=0, Re != 0"),
    ((4, 4), 4, "two-row, should be nonzero generally"),  # not in vanishers
    ((6,), 3, "single row, Re=±1, Im=0"),
    ((1,1,1,1,1,1), 3, "single column"),
]

for λ, m, descr in test_cases:
    re_, im_ = G_lambda(λ, m)
    print(f"λ={λ}, m={m}: G = {re_} + {im_}i   ({descr})")
