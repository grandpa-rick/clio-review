r"""Independent check of MacBeth UID 390 ("waist class delta is quadratic, not additive").
Rick review 2026-10-14. Pure Python, shares no code with MacBeth's scratch script.

Setup (as printed): K class <= 2, M = Inn K abelian, Aut K acts on M by conjugation (factors through Out).
For a band rho = (a,b), commuting pair in Out K, delta(rho) = [A,B] in M_(sigma,tau) = M/((s-1)M+(t-1)M).
Commutator convention [x,y] = x y x^-1 y^-1 (as printed).

Clauses checked:
  T1  master formula (*) on the nose in M, random quadruples with 4 outer classes pairwise commuting
  T2  on Out^0: delta(r1 r2) = delta1 + delta2 + chi, delta(r^n) = n^2 delta(r)
  T3  dichotomy on abelian subgroups of Out^0: additive <=> delta==0 <=> pi^-1(Abar) abelian
  T4  OFF Out^0, natural common receptacle M_Abar (coinvariants under all of Abar):
        (i) the sigma1 tau1 twist dies there (printed Sec 5 says it survives)
        (ii) quadratic law + dichotomy hold there verbatim
        (iii) are there abelian Abar that couple (some band has delta != 0 in its OWN receptacle)
              yet delta is additive (== 0) in M_Abar?  -> tests "a coupled torus is always a witness"
Negative controls (must break):
  C1  additive model delta'(a,b) = phi(a) for a nonzero hom phi: Abar -> M: dichotomy test must report
      "nonzero & additive" (shows the additivity test is not vacuous)
  C2  master formula with sigma2,tau2 in place of sigma1,tau1: must fail
  C3  naive quadratic law (no twist) in the fine receptacle M_(sigma1 sigma2, tau1 tau2) off Out^0: must fail
"""
import itertools, random
random.seed(20261014)

def mul(p, q): return tuple(p[i] for i in q)          # p after q
def inv(p):
    r = [0]*len(p)
    for i, x in enumerate(p): r[x] = i
    return tuple(r)

def closure(gens):
    e = tuple(range(len(gens[0]))); G = {e}; fr = [e]
    while fr:
        nf = []
        for g in fr:
            for s in gens:
                h = mul(s, g)
                if h not in G: G.add(h); nf.append(h)
        fr = nf
    return sorted(G)

def build(gens):
    el = closure(gens); idx = {g: i for i, g in enumerate(el)}; N = len(el)
    t = [[idx[mul(a, b)] for b in el] for a in el]
    e = idx[tuple(range(len(gens[0])))]
    iv = [idx[inv(a)] for a in el]
    return el, idx, t, e, iv

def group_from_perm_gens(gens):
    el, idx, t, e, iv = build(gens)
    return dict(N=len(el), t=t, e=e, iv=iv, gidx=[idx[g] for g in gens])

def autos(G):
    """All automorphisms of G as permutations of range(N) (tuples)."""
    N, t, e = G['N'], G['t'], G['e']
    gens = G['gidx']
    # word for every element in gens
    word = {e: []}; fr = [e]
    while fr:
        nf = []
        for g in fr:
            for k, s in enumerate(gens):
                h = t[g][s]
                if h not in word: word[h] = word[g] + [k]; nf.append(h)
        fr = nf
    def order(x):
        k, y = 1, x
        while y != e: y = t[y][x]; k += 1
        return k
    ords = [order(x) for x in range(N)]
    res = []
    for imgs in itertools.product(*[[x for x in range(N) if ords[x] == ords[g]] for g in gens]):
        f = [None]*N
        for x, w in word.items():
            y = e
            for k in w: y = t[y][imgs[k]]
            f[x] = y
        if len(set(f)) != N: continue
        if all(f[t[a][b]] == t[f[a]][f[b]] for a in range(N) for b in range(N)):
            res.append(tuple(f))
    return res

def analyse(name, Kgens):
    K = group_from_perm_gens(Kgens)
    N, t, e, iv = K['N'], K['t'], K['e'], K['iv']
    A = autos(K)
    Aset = set(A); Aidx = {a: i for i, a in enumerate(A)}
    idA = tuple(range(N))
    def conj(k): return tuple(t[t[k][x]][iv[k]] for x in range(N))
    Inn = sorted(set(conj(k) for k in range(N)))
    Innset = set(Inn)
    assert all(mul(a, b) == mul(b, a) for a in Inn for b in Inn), "Inn not abelian"
    # M = Inn as F2-vector space? check exponent 2
    exp2 = all(mul(m, m) == idA for m in Inn)
    assert exp2 and len(Inn) == 4, (name, len(Inn))
    # coordinates: basis m1,m2
    b1 = next(m for m in Inn if m != idA); b2 = next(m for m in Inn if m not in (idA, b1))
    vec = {idA: (0, 0), b1: (1, 0), b2: (0, 1), mul(b1, b2): (1, 1)}
    def add(u, v): return ((u[0]+v[0]) % 2, (u[1]+v[1]) % 2)
    def comm(x, y): return mul(mul(x, y), mul(inv(x), inv(y)))
    def act(X, m): return mul(mul(X, m), inv(X))
    def actv(X, v):  # X acting on vector
        m = [k for k, w in vec.items() if w == v][0]
        return vec[act(X, m)]
    # Out = cosets of Inn
    cos = {}; reps = []
    for a in A:
        key = min(mul(a, m) for m in Inn)
        if key not in cos: cos[key] = len(reps); reps.append(key)
    def cls(a): return cos[min(mul(a, m) for m in Inn)]
    nO = len(reps)
    omul = [[cls(mul(reps[i], reps[j])) for j in range(nO)] for i in range(nO)]
    oe = cls(idA)
    ocomm = [[omul[i][j] == omul[j][i] for j in range(nO)] for i in range(nO)]
    # action matrices of Out on M (as function on vectors)
    acts = [{v: actv(reps[i], v) for v in vec.values()} for i in range(nO)]
    Out0 = [i for i in range(nO) if all(acts[i][v] == v for v in vec.values())]
    print(f"== {name}: |K|={N} |Aut|={len(A)} |Inn|={len(Inn)} |Out|={nO} |Out0|={len(Out0)}")

    # coinvariant quotient: span of (g-1)M over a set of out classes -> subspace I; quotient map
    def span(vs):
        S = {(0, 0)}
        for v in vs:
            S |= {add(s, v) for s in S}
        return S
    def Ispan(classes):
        return span([add(acts[i][v], v) for i in classes for v in vec.values()])
    def red(v, I):  # canonical rep of coset v+I
        return min(add(v, w) for w in I)

    # ---- T1 + C2: master formula on the nose -------------------------------------------
    viol = viol_c2 = checks = 0
    for _ in range(300000):
        A1, B1, A2, B2 = (random.choice(A) for _ in range(4))
        cs = [cls(x) for x in (A1, B1, A2, B2)]
        if not all(ocomm[i][j] for i in cs for j in cs): continue
        checks += 1
        lhs = vec[comm(mul(A1, A2), mul(B1, B2))]
        s1t1 = mul(A1, B1)
        rhs = vec[comm(A1, B1)]
        rhs = add(rhs, vec[act(s1t1, comm(A2, B2))])
        rhs = add(rhs, vec[act(A1, comm(A2, B1))])
        rhs = add(rhs, vec[act(B1, comm(A1, B2))])
        viol += lhs != rhs
        rc2 = vec[comm(A1, B1)]
        rc2 = add(rc2, vec[act(mul(A2, B2), comm(A2, B2))])
        rc2 = add(rc2, vec[act(A2, comm(A2, B1))])
        rc2 = add(rc2, vec[act(B2, comm(A1, B2))])
        viol_c2 += lhs != rc2
    print(f"T1 master formula on the nose: {viol}/{checks} violations")
    print(f"C2 control (sigma2,tau2 in place of sigma1,tau1): {viol_c2}/{checks} violations (must be >0)")

    # ---- abelian subgroups of Out (generated by <=3 elements) --------------------------
    def osub(gs):
        S = {oe}; fr = [oe]
        while fr:
            nf = []
            for g in fr:
                for s in gs:
                    h = omul[g][s]
                    if h not in S: S.add(h); nf.append(h)
            fr = nf
        return frozenset(S)
    subs = set(); subs2 = set()
    for k in (1, 2, 3):
        for gs in itertools.combinations(range(nO), k):
            if all(ocomm[i][j] for i in gs for j in gs):
                subs.add(osub(gs))
                if k <= 2: subs2.add(osub(gs))
    abel = [S for S in subs if all(ocomm[i][j] for i in S for j in S)]
    # lift: fixed representative per class
    def c_fine(a, b):  # delta of band (a,b) in its own receptacle
        I = Ispan([a, b]); return red(vec[comm(reps[a], reps[b])], I)
    def c_in(a, b, I): return red(vec[comm(reps[a], reps[b])], I)

    # ---- T2: quadratic law on Out0 -------------------------------------------------------
    O0 = set(Out0)
    ab0 = [S for S in abel if S <= O0]
    v2 = v4 = n2 = n4 = 0
    for S in ab0:
        Sl = sorted(S)
        for a1, b1, a2, b2 in itertools.product(Sl, repeat=4):
            d12 = vec[comm(reps[omul[a1][a2]], reps[omul[b1][b2]])]
            chi = add(vec[comm(reps[a1], reps[b2])], vec[comm(reps[a2], reps[b1])])
            rhs = add(add(vec[comm(reps[a1], reps[b1])], vec[comm(reps[a2], reps[b2])]), chi)
            n2 += 1; v2 += d12 != rhs
        for a, b in itertools.product(Sl, repeat=2):
            an, bn = oe, oe
            for n in range(1, 7):
                an, bn = omul[an][a], omul[bn][b]
                d = vec[comm(reps[an], reps[bn])]
                base = vec[comm(reps[a], reps[b])]
                pred = base if (n*n) % 2 else (0, 0)
                n4 += 1; v4 += d != pred
    print(f"T2 on Out0: cross-term law {v2}/{n2} violations; delta(rho^n)=n^2 delta {v4}/{n4} violations")

    # ---- T3 + C1: dichotomy on Out0 ------------------------------------------------------
    def additive(S, dfun):
        Sl = sorted(S)
        bands = list(itertools.product(Sl, repeat=2))
        for (a1, b1), (a2, b2) in itertools.product(bands, repeat=2):
            if dfun(omul[a1][a2], omul[b1][b2]) != add(dfun(a1, b1), dfun(a2, b2)): return False
        return True
    bad3 = 0; coupled0 = 0; c1_hits = 0; c1_tested = 0
    for S in ab0:
        df = lambda a, b: vec[comm(reps[a], reps[b])]
        nz = any(df(a, b) != (0, 0) for a in S for b in S)
        ad = additive(S, df)
        preim = [mul(reps[i], m) for i in S for m in Inn]
        abel_pre = all(mul(x, y) == mul(y, x) for x in preim for y in preim)
        coupled0 += nz
        if not (ad == (not nz) == abel_pre): bad3 += 1
        # C1: additive model phi(a) for a nonzero hom phi: S -> M (search all maps S->M that are homs)
        Sl = sorted(S)
        for img in itertools.product(list(vec.values()), repeat=len(Sl)):
            phi = dict(zip(Sl, img))
            if all(phi[omul[x][y]] == add(phi[x], phi[y]) for x in Sl for y in Sl) and any(v != (0, 0) for v in img):
                c1_tested += 1
                c1_hits += additive(S, lambda a, b: phi[a])
                break
    cp2 = sum(1 for S in subs2 if S <= O0 and any(vec[comm(reps[a], reps[b])] != (0, 0) for a in S for b in S))
    print(f"   coupled abelian subgroups of Out0 that are <=2-generated: {cp2} of {sum(1 for S in subs2 if S <= O0)}")
    print(f"T3 dichotomy on {len(ab0)} abelian subgroups of Out0 ({coupled0} coupled): {bad3} failures")
    print(f"C1 additive model phi(a): nonzero & additive found on {c1_hits}/{c1_tested} subgroups (must be >0)")

    # ---- T4 + C3: off Out0 ----------------------------------------------------------------
    t4_twist = t4_law = t4_dich = 0; t4n = 0
    cpl_fine_add_coarse = []; c3v = c3n = 0
    nonO0 = [S for S in abel if not S <= O0]
    for S in nonO0:
        Sl = sorted(S); I = Ispan(Sl)
        dS = lambda a, b: c_in(a, b, I)
        for a1, b1, a2, b2 in itertools.product(Sl, repeat=4):
            t4n += 1
            # twist term (s1 t1 - 1) delta(rho2) in I ?
            x = vec[comm(reps[a2], reps[b2])]
            tw = add(acts[omul[a1][b1]][x], x)
            t4_twist += red(tw, I) != (0, 0)
            lhs = dS(omul[a1][a2], omul[b1][b2])
            rhs = add(add(dS(a1, b1), dS(a2, b2)), add(dS(a1, b2), dS(a2, b1)))
            t4_law += lhs != rhs
            # C3: naive law (no twist) in fine receptacle of the product band
            If = Ispan([omul[a1][a2], omul[b1][b2]])
            lhs_f = red(vec[comm(mul(reps[a1], reps[a2]), mul(reps[b1], reps[b2]))], If)
            rhs_f = red(add(add(vec[comm(reps[a1], reps[b1])], vec[comm(reps[a2], reps[b2])]),
                            add(vec[comm(reps[a1], reps[b2])], vec[comm(reps[a2], reps[b1])])), If)
            c3n += 1; c3v += lhs_f != rhs_f
        nz = any(dS(a, b) != (0, 0) for a in Sl for b in Sl)
        ad = additive(S, dS)
        t4_dich += (ad != (not nz))
        coupled_fine = any(c_fine(a, b) != (0, 0) for a in Sl for b in Sl if ocomm[a][b])
        if coupled_fine and ad:
            w = next((a, b) for a in Sl for b in Sl if c_fine(a, b) != (0, 0))
            cpl_fine_add_coarse.append((len(S), w, len(I)))
            if len(cpl_fine_add_coarse) == 1:
                a, b = w
                nontriv = [x for x in Sl if x not in O0]
                print(f"   WITNESS: |Abar|={len(S)}, |Abar cap Out0|={len([x for x in Sl if x in O0])}; band (a,b) a in Out0: {a in O0}, b in Out0: {b in O0}")
                print(f"            own receptacle |I_ab|={len(Ispan([a,b]))}, delta_own={c_fine(a,b)}; [A,B] vec={vec[comm(reps[a],reps[b])]}; I_Abar={sorted(I)}")
                print(f"            delta in M_Abar for every band: {sorted(set(dS(x,y) for x in Sl for y in Sl))}; delta_own over all bands: {sorted(set(c_fine(x,y) for x in Sl for y in Sl))}")
    print(f"T4 off Out0 ({len(nonO0)} abelian subgroups not in Out0; {t4n} quadruples):")
    print(f"   (i) twist (s1t1-1)delta2 nonzero in M_Abar: {t4_twist}/{t4n}   [printed Sec 5: 'still carries the twist']")
    print(f"   (ii) quadratic law in M_Abar: {t4_law}/{t4n} violations; dichotomy in M_Abar: {t4_dich} failures")
    print(f"   (iii) coupled (own receptacle) yet delta additive (==0) in M_Abar: {len(cpl_fine_add_coarse)} subgroups")
    for s in cpl_fine_add_coarse[:3]:
        print(f"        e.g. |Abar|={s[0]}, coupled band (out-class idx) {s[1]}, |I|={s[2]} (I = all of M => M_Abar = 0)" if s[2]==4 else f"        e.g. |Abar|={s[0]}, band {s[1]}, |I|={s[2]}")
    print(f"C3 control naive no-twist law in fine receptacle off Out0: {c3v}/{c3n} violations (must be >0)")
    return dict(coupled_fine_add_coarse=len(cpl_fine_add_coarse))

# K = D4 x C2 on 4+2 points; K = Q8 x C2 (Q8 regular rep on 8 points) + 2 points
r = (1, 2, 3, 0, 4, 5); s = (0, 3, 2, 1, 4, 5); z = (0, 1, 2, 3, 5, 4)
analyse("D4 x C2", [r, s, z])
# Q8 regular: elements 1,i,j,k,-1,-i,-j,-k indexed 0..7; left mult by i and j
def qm(a, b):
    tbl = {('1', x): x for x in '1ijk'}
    base = {('i','i'):(-1,'1'),('i','j'):(1,'k'),('i','k'):(-1,'j'),('j','i'):(-1,'k'),('j','j'):(-1,'1'),
            ('j','k'):(1,'i'),('k','i'):(1,'j'),('k','j'):(-1,'i'),('k','k'):(-1,'1')}
    sa, ua = a; sb, ub = b
    if ua == '1': return (sa*sb, ub)
    if ub == '1': return (sa*sb, ua)
    sg, u = base[(ua, ub)]; return (sa*sb*sg, u)
Q = [(1,'1'),(1,'i'),(1,'j'),(1,'k'),(-1,'1'),(-1,'i'),(-1,'j'),(-1,'k')]
Qi = {q: n for n, q in enumerate(Q)}
li = tuple(Qi[qm((1,'i'), q)] for q in Q) + (8, 9)
lj = tuple(Qi[qm((1,'j'), q)] for q in Q) + (8, 9)
zz = tuple(range(8)) + (9, 8)
analyse("Q8 x C2", [li, lj, zz])
