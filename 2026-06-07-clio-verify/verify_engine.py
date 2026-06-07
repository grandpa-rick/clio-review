"""
Verify Clio's engine identity (Theorem 1 of 2026-06-06-tworow-d4-no-rational-root):

  Im(A^m) = u * H_m(u),  H_m = h_{m-1}(A,B) = sum_{j=0}^{m-1} A^j B^{m-1-j}

with A = 1 + s*u + u^2, B = 1 + sbar*u + u^2, s = 1+i, sbar = 1-i.
Equivalently W = 1+u+u^2, A = W+iu, B = W-iu.

Then I_b(m) := Im G_{(2m-b,b)} = [u^{b-1}]((1-u) H_m(u)) ∈ Z.

Two checks:
 (a) Im(A^m) symbolic in Q[i][u] equals u*H_m where H_m has integer coefficients.
 (b) I_b(m) as defined here matches direct evaluation [u^b]((1-u)P) where P = A^m.
"""
import sympy as sp

u, m_sym = sp.symbols('u m')
I = sp.I  # imaginary unit
s = 1 + I
sbar = 1 - I
W = 1 + u + u**2

def direct_I_b(m, b):
    A = 1 + s*u + u**2
    P = sp.expand(A**m)
    Q = sp.expand((1 - u) * P)
    coef = sp.Poly(Q, u).all_coeffs()
    deg = sp.Poly(Q, u).degree()
    if b > deg:
        return 0
    c = coef[deg - b]
    # c is a Gaussian integer
    c = sp.expand(c)
    re, im = c.as_real_imag()
    return int(im)

def engine_I_b(m, b):
    """Use Im(A^m) = u * H_m, with H_m integer polynomial."""
    A = 1 + s*u + u**2
    B = 1 + sbar*u + u**2
    H = sp.expand(sum(A**j * B**(m-1-j) for j in range(m)))
    # H should have only integer (real) coefficients
    Hpoly = sp.Poly(H, u)
    for c in Hpoly.all_coeffs():
        re, im = sp.expand(c).as_real_imag()
        assert sp.simplify(im) == 0, f"H_m has nonreal coef at m={m}: {c}"
    Hint = sp.Poly([sp.nsimplify(sp.expand(c).as_real_imag()[0]) for c in Hpoly.all_coeffs()], u)
    # I_b = [u^{b-1}]((1-u)*H_m)
    R = sp.expand((1 - u) * Hint.as_expr())
    Rpoly = sp.Poly(R, u)
    deg = Rpoly.degree()
    coefs = Rpoly.all_coeffs()
    target = b - 1
    if target < 0 or target > deg:
        return 0
    return int(coefs[deg - target])

print("Engine identity check (Im(A^m) = u * H_m, H_m ∈ Z[u]):")
print(f"{'m':>3} {'b':>3} {'I_b direct':>14} {'I_b engine':>14} {'match':>6}")
results = []
for m in range(1, 11):
    for b in range(0, m+1):
        a = direct_I_b(m, b)
        c = engine_I_b(m, b)
        ok = (a == c)
        results.append((m, b, a, c, ok))
        if m <= 6 or (m in (7, 8, 9, 10) and b in (1, 2, 3, 4, 5, b)):
            print(f"{m:>3} {b:>3} {a:>14} {c:>14} {str(ok):>6}")

all_ok = all(r[4] for r in results)
print(f"\nALL MATCH: {all_ok}  ({len(results)} cases, m up to 10)")
