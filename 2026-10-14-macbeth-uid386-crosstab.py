r"""Independent check of MacBeth UID 386 (two T^2 gerbe ends, delta => [g]).
Groups as permutation groups (tuples). For each K:
  g_couples  : exists k,k' with [k,k'] in Z(K)\{1}   (inner band with nonzero central class)
  d_couples  : exists commuting pair (a,b) in Out K such that NO lifts A,B in Aut K commute
               (= nonabelian Giraud obstruction on T^2 = BZ^2; for abelian Inn equals class [A,B]!=0)
  sigma_split: Aut -> Out has a homomorphic section (only computed for small Out)
Rick review 2026-10-14.
"""
import itertools, sys

def mul(p, q):  # p after q
    return tuple(p[i] for i in q)
def inv(p):
    r = [0]*len(p)
    for i, x in enumerate(p): r[x] = i
    return tuple(r)

def closure(gens):
    n = len(gens[0]); e = tuple(range(n))
    G = {e}; frontier = [e]
    while frontier:
        nf = []
        for g in frontier:
            for s in gens:
                h = mul(s, g)
                if h not in G: G.add(h); nf.append(h)
        frontier = nf
    return sorted(G)

class Grp:
    def __init__(self, gens, name):
        self.name = name
        self.el = closure(gens)
        self.idx = {g: i for i, g in enumerate(self.el)}
        N = len(self.el); self.N = N
        self.t = [[self.idx[mul(a, b)] for b in self.el] for a in self.el]
        self.e = self.idx[tuple(range(len(gens[0])))]
        self.inv = [self.idx[inv(a)] for a in self.el]
        self.gens = self.small_gens()
    def m(self, a, b): return self.t[a][b]
    def comm(self, a, b): return self.m(self.m(a, b), self.m(self.inv[a], self.inv[b]))
    def center(self): return [z for z in range(self.N) if all(self.t[z][x] == self.t[x][z] for x in range(self.N))]
    def sub(self, gs):
        S = {self.e}; fr = [self.e]
        while fr:
            nf = []
            for g in fr:
                for s in gs:
                    h = self.m(g, s)
                    if h not in S: S.add(h); nf.append(h)
            fr = nf
        return S
    def small_gens(self):
        gs = []; S = {self.e}
        for x in sorted(range(self.N), key=lambda x: -self.order(x)):
            if x not in S: gs.append(x); S = self.sub(gs)
            if len(S) == self.N: break
        # try to shrink
        for k in range(1, len(gs)):
            for c in itertools.combinations(range(self.N), k):
                if len(self.sub(list(c))) == self.N: return list(c)
            if k >= 2: break
        return gs
    def order(self, x):
        k, y = 1, x
        while y != self.e: y = self.m(y, x); k += 1
        return k
    def lcs_class(self):
        def gen_comm(A, B):
            return self.sub([self.comm(a, b) for a in A for b in B])
        G = set(range(self.N)); c = 0; cur = G
        while len(cur) > 1:
            cur = gen_comm(cur, G); c += 1
            if c > 10: return None  # not nilpotent
        return c

def automorphisms(G):
    gens = G.gens
    # words: express every element as product from BFS over gens
    word = {G.e: []}; fr = [G.e]
    while fr:
        nf = []
        for g in fr:
            for i, s in enumerate(gens):
                h = G.m(g, s)
                if h not in word: word[h] = word[g] + [i]; nf.append(h)
        fr = nf
    auts = []
    cands = [[x for x in range(G.N) if G.order(x) == G.order(s)] for s in gens]
    for imgs in itertools.product(*cands):
        f = [None]*G.N; ok = True
        for g, w in word.items():
            y = G.e
            for i in w: y = G.m(y, imgs[i])
            f[g] = y
        if len(set(f)) != G.N: continue
        # homomorphism check on generators suffices: f(g*s) == f(g)*f(s)
        for g in range(G.N):
            for i, s in enumerate(gens):
                if f[G.m(g, s)] != G.m(f[g], imgs[i]): ok = False; break
            if not ok: break
        if ok: auts.append(tuple(f))
    return auts

def analyse(G, want_split=True):
    Z = set(G.center())
    cls = G.lcs_class()
    abelian = len(Z) == G.N
    g_couples = any(G.comm(a, b) in Z and G.comm(a, b) != G.e for a in range(G.N) for b in range(G.N))
    A = automorphisms(G); Aidx = {a: i for i, a in enumerate(A)}
    ide = tuple(range(G.N))
    comp = lambda f, g: tuple(f[x] for x in g)
    ainv = lambda f: inv(f)
    # inner autos
    Inn = set()
    for k in range(G.N):
        ki = G.inv[k]
        Inn.add(tuple(G.m(G.m(k, x), ki) for x in range(G.N)))
    Inn = list(Inn)
    # cosets of Inn
    rep = {}; reps = []
    for f in A:
        if f in rep: continue
        reps.append(f)
        for i in Inn: rep[comp(f, i)] = len(reps)-1
    nO = len(reps)
    coset = lambda f: rep[f]
    # Out multiplication
    Omul = [[coset(comp(reps[a], reps[b])) for b in range(nO)] for a in range(nO)]
    d_pairs = 0
    for a in range(nO):
        for b in range(a, nO):
            if Omul[a][b] != Omul[b][a]: continue
            found = False
            for i in Inn:
                Ai = comp(reps[a], i)
                for j in Inn:
                    Bj = comp(reps[b], j)
                    if comp(Ai, Bj) == comp(Bj, Ai): found = True; break
                if found: break
            if not found: d_pairs += 1
    split = None
    if want_split and nO <= 8:
        # brute force section: choose a lift for each Out generator set — try all lift assignments for all of Out
        # small: search homomorphic sections via generators of Out
        Oe = coset(ide)
        # generators of Out
        def osub(gs):
            S = {Oe}; fr = [Oe]
            while fr:
                nf = []
                for g in fr:
                    for s in gs:
                        h = Omul[g][s]
                        if h not in S: S.add(h); nf.append(h)
                fr = nf
            return S
        ogs = []
        for x in range(nO):
            if x not in osub(ogs): ogs.append(x)
        lifts = [[comp(reps[o], i) for i in Inn] for o in ogs]
        split = False
        for choice in itertools.product(*lifts):
            H = set(closure(list(choice)) if choice else [ide])
            if len(H) == nO: split = True; break
    return dict(name=G.name, order=G.N, cls=cls, Z=len(Z), Aut=len(A), Inn=len(Inn), Out=nO,
                split=split, d_couple_pairs=d_pairs, d=d_pairs > 0, g=g_couples, abelian=abelian)

# ---------- group constructors (regular perm rep from a multiplication rule) ----------
def from_rule(elems, mulf, name):
    idx = {x: i for i, x in enumerate(elems)}
    gens = [tuple(idx[mulf(g, x)] for x in elems) for g in elems]  # left regular rep
    return Grp(gens, name)

def metacyclic(n, m, s, r, name):
    # <a,b | a^n, b^m = a^s, b a b^-1 = a^r>, elems a^i b^j
    elems = [(i, j) for i in range(n) for j in range(m)]
    def mulf(x, y):
        i, j = x; k, l = y
        # b^j a^k = a^{k r^j} b^j
        ii = (i + k * pow(r, j, n)) % n; jj = j + l
        if jj >= m: jj -= m; ii = (ii + s) % n
        return (ii, jj)
    return from_rule(elems, mulf, name)

def direct(G, H, name):
    elems = [(a, b) for a in range(G.N) for b in range(H.N)]
    return from_rule(elems, lambda x, y: (G.m(x[0], y[0]), H.m(x[1], y[1])), name)

def perm_group(gens, name): return Grp([tuple(g) for g in gens], name)

def cyc(n): return metacyclic(n, 1, 0, 1, f"C{n}")

def heis(p):
    elems = [(a, b, c) for a in range(p) for b in range(p) for c in range(p)]
    return from_rule(elems, lambda x, y: ((x[0]+y[0]) % p, (x[1]+y[1]) % p, (x[2]+y[2]+x[0]*y[1]) % p), f"Heis(F{p})")

def gen_dihedral(A_elems, add, neg, name):
    elems = [(a, e) for a in A_elems for e in (0, 1)]
    def mulf(x, y):
        a, e = x; b, f = y
        return (add(a, b if e == 0 else neg(b)), (e + f) % 2)
    return from_rule(elems, mulf, name)

if __name__ == "__main__":
    D4 = metacyclic(4, 2, 0, 3, "D4(ord8)"); Q8 = metacyclic(4, 2, 2, 3, "Q8")
    C2 = cyc(2)
    groups = [
        D4, Q8, heis(3), metacyclic(8, 2, 0, 5, "M16"), metacyclic(4, 4, 0, 3, "C4:C4"),
        direct(D4, C2, "D4xC2"), direct(Q8, C2, "Q8xC2"),
        metacyclic(8, 2, 0, 7, "D16"), metacyclic(8, 2, 0, 3, "SD16"), metacyclic(8, 2, 4, 7, "Q16"),
        cyc(4), direct(C2, C2, "C2xC2"),
        # class 3/4 order 32
        metacyclic(16, 2, 0, 15, "D32"), metacyclic(16, 2, 0, 7, "SD32"), metacyclic(16, 2, 8, 15, "Q32"),
        direct(metacyclic(8, 2, 0, 7, "D16"), C2, "D16xC2"),
        direct(metacyclic(8, 2, 4, 7, "Q16"), C2, "Q16xC2"),
        direct(metacyclic(8, 2, 0, 3, "SD16"), C2, "SD16xC2"),
        metacyclic(8, 4, 0, 3, "C8:C4(r=3)"), metacyclic(8, 4, 0, 7, "C8:C4(r=7)"),
        # order 81 class 3: C3 wr C3
        perm_group([[1, 2, 0, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8, 0, 1, 2]], "C3wrC3"),
        # non-nilpotent controls
        gen_dihedral([(a, b) for a in range(3) for b in range(3)],
                     lambda x, y: ((x[0]+y[0]) % 3, (x[1]+y[1]) % 3), lambda x: ((-x[0]) % 3, (-x[1]) % 3), "Dih(C3^2)"),
        perm_group([[1, 0, 2], [1, 2, 0]], "S3"),
        perm_group([[1, 2, 0, 3], [1, 0, 3, 2]], "A4"),
    ]
    only = sys.argv[1:]
    for G in groups:
        if only and G.name not in only: continue
        r = analyse(G)
        print(r, flush=True)
