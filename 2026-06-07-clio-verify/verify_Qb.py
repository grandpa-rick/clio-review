"""
Verify Clio's (♦) reduction by:
 (a) Computing I_b(m) by interpolation from integer m values
 (b) Factoring Q_b(m) = I_b(m) / forced-roots-product
 (c) Listing rational roots of Q_b for b ≤ 26

Reference: 2026-06-06-tworow-d4-no-rational-root.tex (Clio).
"""
import sympy as sp

u, m = sp.symbols('u m')
I = sp.I
s = 1 + I

def direct_I_b_int(M, b):
    """I_b at integer m = M."""
    if b < 0:
        return 0
    A = 1 + s * u + u**2
    P = sp.expand(A**M)
    Q = sp.expand((1 - u) * P)
    coefs = sp.Poly(Q, u).all_coeffs()
    deg = sp.Poly(Q, u).degree()
    if b > deg:
        return 0
    c = sp.expand(coefs[deg - b])
    re_, im_ = c.as_real_imag()
    return int(im_)

def I_b_poly_interp(b, max_extra=4):
    """Interpolate I_b(m) as polynomial in m. deg <= b."""
    deg_bound = b + max_extra
    pts = [(M, direct_I_b_int(M, b)) for M in range(0, deg_bound + 1)]
    poly = sp.interpolate(pts, m)
    return sp.Poly(sp.expand(poly), m)

print("=" * 78)
print("VERIFY Theorems 2 & 3: forced roots, deg formula, Q_b rational roots")
print("=" * 78)
print(f"{'b':>3} {'b mod 4':>8} {'deg I_b':>8} {'deg Q_b':>8} {'Q_b rational roots':>40}")
structural = []
for b in range(1, 27):
    Ib_poly = I_b_poly_interp(b)
    deg_Ib = Ib_poly.degree()
    forced_roots = list(range(0, (b - 1)//2 + 1))
    forced_factor = sp.Mul(*[m - r for r in forced_roots]) if forced_roots else sp.Integer(1)
    Qb = sp.cancel(Ib_poly.as_expr() / forced_factor)
    Qb_poly = sp.Poly(Qb, m)
    Qb_deg = Qb_poly.degree()
    expected_deg_Ib = b if b % 4 != 0 else b - 1
    expected_deg_Qb = b // 2 if b % 4 != 0 else b // 2 - 1
    structural.append((b, deg_Ib, expected_deg_Ib, Qb_deg, expected_deg_Qb))
    rat_roots = Qb_poly.ground_roots()
    print(f"{b:>3} {b % 4:>8} {deg_Ib:>8} {Qb_deg:>8} {str(rat_roots):>40}")

print()
print("Theorem 2 degree formula check (all rows match):")
for b, d, ed, dQ, edQ in structural:
    assert d == ed, f"b={b}: deg I_b = {d}, expected {ed}"
    assert dQ == edQ, f"b={b}: deg Q_b = {dQ}, expected {edQ}"
print("  PASS")

print()
print("=" * 78)
print("Theorem 3: factor Q_b over Q")
print("=" * 78)
for b in range(1, 27):
    Ib_poly = I_b_poly_interp(b)
    forced_roots = list(range(0, (b - 1)//2 + 1))
    forced_factor = sp.Mul(*[m - r for r in forced_roots]) if forced_roots else sp.Integer(1)
    Qb = sp.cancel(Ib_poly.as_expr() / forced_factor)
    Qb_poly = sp.Poly(Qb, m)
    fact = sp.factor(Qb_poly.as_expr())
    fact_str = str(fact)
    if len(fact_str) > 100:
        fact_str = fact_str[:98] + ".."
    print(f"b={b:2d} ({b%4}):  Q_b = {fact_str}")
