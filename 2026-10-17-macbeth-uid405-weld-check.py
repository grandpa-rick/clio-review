#!/usr/bin/env python3
"""Rick's check of MacBeth UID 405 (WIP 2fd555a): weld B = DS <| DT.
Brute force, no Poly library. Delta(X) = indiscrete category on X (store comonoid X y^X):
a morphism out of x is just its target x'. A right c-coaction on a carrier m makes each
direction set m[i] a c-copresheaf (label map + action); the represented functor at a constant
copresheaf V is  F(V)(d-object) = sum_{positions over it} |Hom_{c-Set}(m[i], const V)|.
Hom into a constant copresheaf = functions constant on action-orbits, so the transported
exponent of position i = number of orbits of m[i]. We compute it by enumeration anyway.
"""
import itertools as it, math

def funcs(dom, cod):
    dom = list(dom)
    for vals in it.product(list(cod), repeat=len(dom)):
        yield dict(zip(dom, vals))

def weld(S, T):
    """B = DS <| DT: positions (s,g), g: S->T (tuple); directions (a,t) in S x T."""
    pos = [(s, g) for s in S for g in it.product(T, repeat=len(S))]
    dirs = [(a, t) for a in S for t in T]
    return pos, dirs

# right-coaction candidates on the direction set S x T of a position (s,g):
# each = (comonoid objects, label(e), act(e, target)).  Indiscrete => morphism = target.
def right_actions(S, T):
    return {
        "y (no right coaction)":  ([None], lambda e: None, lambda e, x: e),
        "DT on t (regular rho)":  (list(T), lambda e: e[1], lambda e, x: (e[0], x)),
        "DS on a":                (list(S), lambda e: e[0], lambda e, x: (x, e[1])),
        "D(SxT) on (a,t)":        ([(a, t) for a in S for t in T], lambda e: e, lambda e, x: x),
    }

def check_copresheaf(dirs, objs, lab, act):
    for e in dirs:
        if act(e, lab(e)) != e: return False                 # identity
        for x in objs:
            e1 = act(e, x)
            if lab(e1) != x: return False                    # lands over target
            for x2 in objs:
                if act(e1, x2) != act(e, x2): return False   # composition (indiscrete)
    return True

def hom_count(dirs, objs, act, V):
    n = 0
    for h in funcs(dirs, range(V)):
        if all(h[act(e, x)] == h[e] for e in dirs for x in objs): n += 1
    return n

def exponent(dirs, objs, act):
    a, b = hom_count(dirs, objs, act, 2), hom_count(dirs, objs, act, 3)
    k = round(math.log(a, 2)); assert 2**k == a and 3**k == b
    return k

def check_regular_bicomodule_preserves(S, T, subset):
    """lambda = delta_S <| DT sends (s,g) to (s, s' |-> (s',g)); rho keeps positions.
    So a set of positions is a sub-bicomodule iff closed under (s,g)->(s',g) for all s'."""
    return all((s2, g) in subset for (s, g) in subset for s2 in S)

def run(nS, nT):
    S, T = list(range(nS)), list("abc"[:nT])
    pos, dirs = weld(S, T)
    print(f"\n=== |S|={nS}, |T|={nT}:  B = (S.T^S) y^(SxT), |B(1)|={len(pos)}, |B[i]|={len(dirs)}")
    print("  (a) transported exponent of content per right coaction on B[i]=SxT:")
    out = {}
    for name, (objs, lab, act) in right_actions(S, T).items():
        assert check_copresheaf(dirs, objs, lab, act), name
        k = exponent(dirs, objs, act); out[name] = k
        print(f"      {name:24s} exponent {k}   (|S|={nS}, |T|={nT}, |SxT|={nS*nT})"
              + ("   <-- = |SxT|" if k == nS*nT else ""))
    # positions over each DS-object (left coaction (s,g) -> s): index of Sigma-tail per fibre
    idx = {s: sum(1 for (s1, g) in pos if s1 == s) for s in S}
    assert set(idx.values()) == {nT**nS}
    # swapped composite DT <| DS, left DT, right DS on t-coordinate: exponent |T|, index S^T
    Fb = lambda V: nT**nS * V**out["DT on t (regular rho)"]
    Fsw = lambda V: nS**nT * V**nT
    print(f"  F_B(V)=T^S V^S: V=2 -> {Fb(2)}, V=3 -> {Fb(3)};  swapped DT<|DS: V=2 -> {Fsw(2)}, V=3 -> {Fsw(3)}"
          + ("   [cardinality does NOT separate the two orders]" if Fb(2) == Fsw(2) and Fb(3) == Fsw(3) else ""))
    # (b) sigma: A -> B, (s,t) -> (s, const_t)
    sigma = {(s, t): (s, tuple([t]*nS)) for s in S for t in T}
    inj = len(set(sigma.values())) == len(sigma)
    r = lambda p: (p[0], p[1][p[0]])                       # r(s,g) = (s, g(s))
    sect = all(r(sigma[x]) == x for x in sigma)
    e_fix = [p for p in pos if (p[0], tuple([p[1][p[0]]]*nS)) == p]
    sub = check_regular_bicomodule_preserves(S, T, set(sigma.values()))
    iso = len(sigma) == len(pos)
    nonconst = nT**nS - nT
    fibre_r = nT**(nS-1)
    print(f"  (b) sigma injective {inj}; r.sigma = id {sect}; image closed under lambda,rho (sub-bicomodule) {sub}")
    print(f"      sigma bijective on positions (A = B) {iso};  fixed points of e = {len(e_fix)} = |S||T| {len(e_fix)==nS*nT}")
    print(f"      sigma(A) as sub-bicomodule: F_A(V) = T x V^S (index {nT}, exponent {out['DT on t (regular rho)']})")
    print(f"      A via its own D(SxT) left coaction (MacBeth Thm 6): V^(SxT), exponent {nS*nT}")
    print(f"      left-only reading (right comonoid y) of B: index T^S={nT**nS}, exponent {out['y (no right coaction)']};"
          f" of sigma(A): index {nT}, exponent {out['y (no right coaction)']}")
    print(f"  Thm 7: Sigma-index |T^S|={nT**nS}; non-constant maps {nonconst}; per-position data forgotten by r |T^(S-{{s}})|={fibre_r}")
    macbeth_says_false = nT >= 2
    consistent_false = not iso
    print(f"  clause (2): MacBeth's criterion (|T|>=2) says FALSE: {macbeth_says_false};"
          f"  consistent-reading criterion (sigma not onto) says FALSE: {consistent_false}"
          + ("   <-- DISAGREE" if macbeth_says_false != consistent_false else ""))
    return out

if __name__ == "__main__":
    for nS, nT in [(1, 1), (1, 2), (2, 1), (1, 3), (2, 2), (2, 3), (3, 2)]:
        out = run(nS, nT)
        assert out["DT on t (regular rho)"] == nS and out["DS on a"] == nT
        assert out["y (no right coaction)"] == nS*nT and out["D(SxT) on (a,t)"] == 1
    print("\nAll assertions passed.")
