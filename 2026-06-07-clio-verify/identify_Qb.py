"""
Try to identify Q_b as a classical orthogonal polynomial family.

Strategies:
 1. Look at monic form: coefficients integer? Pattern?
 2. Compute Q_b(0), Q_b at small integers — match against OEIS templates.
 3. Test three-term recurrence: does Q_{b+1}(m) = (alpha_b * (m - c_b)) * Q_b(m) - gamma_b * Q_{b-1}(m)
    for some sequences alpha, c, gamma?
 4. Check whether the variable-shifted polynomial T_b(n) := Q_b(b + n) has cleaner integer structure.

Also: Im G as a polynomial in m has been studied with leading coefficient = 2^{b/2} sin(πb/4)/b!.
So Q_b should have leading coefficient = that / (something from forced roots).
"""
import sympy as sp

u, m, n = sp.symbols('u m n')
I = sp.I
s = 1 + I

def direct_I_b_int(M, b):
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
    return int(c.as_real_imag()[1])

def Qb_poly(b):
    deg_bound = b + 4
    pts = [(M, direct_I_b_int(M, b)) for M in range(0, deg_bound + 1)]
    Ib = sp.interpolate(pts, m)
    Ib = sp.Poly(sp.expand(Ib), m)
    forced_roots = list(range(0, (b - 1)//2 + 1))
    forced_factor = sp.Mul(*[m - r for r in forced_roots]) if forced_roots else sp.Integer(1)
    Qb = sp.cancel(Ib.as_expr() / forced_factor)
    return sp.Poly(Qb, m)

# Generate Q_b
Qbs = {b: Qb_poly(b) for b in range(1, 21)}

print("Q_b shifted to n = m - b (away from forced roots, ascending in n):")
for b in range(1, 21):
    Qb = Qbs[b]
    # Shift: substitute m = n + b
    Qb_shift = sp.Poly(Qb.as_expr().subs(m, n + b), n)
    # Normalize: print leading coefficient and shifted poly (denominator-cleared)
    lc = Qb_shift.LC()
    # Multiply by denominator of lc
    den = sp.denom(lc)
    Qb_int = sp.Poly(sp.expand(Qb_shift.as_expr() * den), n)
    print(f"  b={b:2d}: lc = {lc}, den = {den}")
    s_ = str(sp.expand(Qb_int.as_expr()))
    if len(s_) > 90:
        s_ = s_[:88] + ".."
    print(f"        Q_b * {den} (as poly in n=m-b): {s_}")

print()
print("Q_b values at m = b (smallest valid m where (♦) is being tested):")
print(f"{'b':>3} {'Q_b(b)':>20} {'Q_b(b)*den':>20} {'factor':>30}")
for b in range(1, 21):
    Qb = Qbs[b]
    val_b = Qb(b)
    val_simp = sp.nsimplify(val_b)
    print(f"{b:>3} {str(val_simp):>20} {str(val_simp):>20} {str(sp.factorint(sp.numer(val_simp))) if val_simp != 0 else '-':>30}")

print()
print("Leading coefficient of Q_b (as a fraction):")
print(f"{'b':>3} {'lc':>20} {'lc*b!':>20}")
for b in range(1, 21):
    lc = Qbs[b].LC()
    print(f"{b:>3} {str(lc):>20} {str(sp.nsimplify(lc * sp.factorial(b))):>20}")

print()
print("Trying three-term recurrence check for Q_b shifted at m=b+n:")
print("Test: Q_b * (something_b) - Q_{b-1} * (something_b-1) = (linear in m) * lower?")
# Just print Q_b in the variable n = 2m - (2b-1) (centered around the half-integer root)
v = sp.symbols('v')
print()
print("Q_b in variable v where m = (2b-1)/2 + v/2 (centered at half-integer):")
for b in range(1, 17):
    Qb = Qbs[b]
    Qb_v = sp.Poly(sp.expand(Qb.as_expr().subs(m, sp.Rational(2*b-1, 2) + v/2)), v)
    print(f"  b={b:2d}: {sp.factor(Qb_v.as_expr())}")
