"""
Direct vanishing check: G_{(2m-b,b)}(i) = 0 iff (m,b) = (2,2)
in the two-row case for 1 <= m <= M_max, 0 <= b <= m.

Also verify the sharp lower bound |Im G| >= m (Clio's Sec. 'Sharp structure').
"""
import sympy as sp

u = sp.symbols('u')
I = sp.I
s = 1 + I

def G_lambda(M, b):
    """G_{(2M-b,b)}(i) = [u^b]((1-u)(1+su+u^2)^M)."""
    A = 1 + s * u + u**2
    P = sp.expand(A**M)
    Q = sp.expand((1 - u) * P)
    coefs = sp.Poly(Q, u).all_coeffs()
    deg = sp.Poly(Q, u).degree()
    if b > deg or b < 0:
        return sp.Integer(0)
    return sp.expand(coefs[deg - b])

M_MAX = 30
print(f"Direct vanishing check: scanning 1 <= m <= {M_MAX}, 0 <= b <= m")
print(f"{'m':>3} {'b':>3} {'lambda=(a,b)':>15} {'Re G':>10} {'Im G':>10} {'|G|^2':>12} {'vanish?':>8}")
vanishers = []
for M in range(1, M_MAX + 1):
    for b in range(0, M + 1):
        G = G_lambda(M, b)
        re_, im_ = G.as_real_imag()
        re_ = int(sp.simplify(re_))
        im_ = int(sp.simplify(im_))
        a = 2*M - b
        if G == 0:
            print(f"{M:>3} {b:>3} {f'({a},{b})':>15} {re_:>10} {im_:>10} {0:>12} {'YES':>8}")
            vanishers.append((M, b))

print()
print(f"All vanishers up to m={M_MAX}: {vanishers}")
print()

print("Sharp lower bound check: min_{b in [1,m], (m,b)!=(2,2)} |Im G_{(2m-b,b)}|")
print(f"Expected: >= m for m >= 4, and equals 2 at (m,b)=(3,3) for m=3.")
for M in range(3, M_MAX + 1):
    min_im = None
    min_b = None
    for b in range(1, M + 1):
        if (M, b) == (2, 2):
            continue
        G = G_lambda(M, b)
        _, im_ = G.as_real_imag()
        im_ = abs(int(sp.simplify(im_)))
        if min_im is None or im_ < min_im:
            min_im = im_
            min_b = b
    flag = "OK" if min_im >= M or (M == 3 and min_im >= 2) else "FAIL"
    print(f"  m={M:>3}: min |Im G| = {min_im:>4} attained at b={min_b}  {flag}")
