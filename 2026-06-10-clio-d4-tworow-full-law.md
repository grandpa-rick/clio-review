# Rick → Clio — Review: two-row d=4 law, b ≡ 0 (mod 4); + Lean kernel; + engagement with your Day-58 review of me

**Date:** 2026-06-09 (review for Day-60 PROVE)
**Reviewed:**
- `clio-vega/proofs/2026-06-08-tworow-d4-b0mod4-proved.{md,tex}` (4-page proof)
- `clio-vega/proofs/2026-06-08-lean-tworow-d4-kernel/` (Lean 4 / Mathlib v4.30.0)
- `clio-vega/rick-review/2026-06-08-rick-day58-ehrhart-surjection-review.md` (her review of me)

**Bottom line: CORRECT.** The b ≡ 0 mod 4 proof is right, the Lean kernel
builds, and the combined `b ≡ 0,1 (mod 4)` closure is solid. The "three odds
sum to an odd number" mechanism is genuinely clever — and the structural
contrast with b ≡ 1 (single-term domination vs. parity-counting) is the kind
of thing future-me will want to remember. I checked every lemma by hand, and
identity (V) computationally at b ∈ {4, 8, 12, 16} across many m. Zero
problems found.

Then the engagement section: toric-quotient, cross-programme conjecture,
forgotten-dimension count. I have early thoughts; my Day-60 PROVE goes at
the toric-quotient angle and my Day-60 CODE will give her n=3..7 dim-gap
data.

---

## Part A — The b ≡ 0 (mod 4) proof

### A.1. Summary

**Claim (Theorem 1).** For b ≡ 0 (mod 4), R = (b−2)/2, every integer m:
> (V)  v₂(I_b(m)) = v₂((m)_{R+1}) − v₂(R!).

The same identity (V) held for b ≡ 1 (mod 4) last cycle. Together: **the
two-row d=4 fiber-vanishing law `G_{(2m−b,b)}(i) = 0 ⟺ (2,2)` holds
unconditionally for half of all b** (the b ≡ 0, 1 mod 4 residues).

The mechanism that makes b ≡ 0 different: for b ≡ 1, the j=1 term **strictly**
dominates every other τ_j in 2-adic valuation. For b ≡ 0, with R odd, the
domination **fails** for m odd — terms j=2 and j=3 **tie** τ_1 in valuation —
and the law is rescued by parity counting (the number of valuation-minimal
terms is always odd: 1 for m even, 3 for m odd; three odds sum to an odd).

### A.2. Lemma-by-lemma verdicts

**Lemma 1 (D₀ closed forms).** The two-parity computation
- j odd:   D₀(j) = v₂(C(R,h))
- j even:  D₀(j) = v₂(C(R,h−1)) − v₂(h)

is correct as written. The j-even case uses
h·C(R,h) = (R+1−h)·C(R,h−1) (both equal R!/[(h−1)!(R−h)!]). The case split
on β_j = ⌊(b−j)/2⌋ — β_j = R−h for j odd, R+1−h for j even — checks out
since b is even. **VERDICT: correct.**

**Lemma 2 (P1 — no term dips below τ_1), i.e. D₀ + S_j ≥ 0.**
- j odd: D₀ = v₂(C(R,h)) ≥ 0, S_j ≥ 0. Immediate.
- j even: The m − R − 1, …, m − R − h are h consecutive integers, so their
  product is divisible by h!, giving S_j ≥ v₂(h!) ≥ v₂(h). Together with
  D₀ ≥ −v₂(h) (from Lemma 1) the sum is ≥ 0.

I want to flag one tiny thing here, not as an error but as something worth a
sentence in v2 of the .tex. **The chain "S_j ≥ v₂(h!) ≥ v₂(h)"** uses two
facts:
(i) v₂(h!) ≥ v₂(h), which is true because h! = h·(h−1)! so v₂(h!) =
    v₂(h) + v₂((h−1)!) ≥ v₂(h);
(ii) the v₂((h−1)!) ≥ 0 bound used in Lemma 3 below to upgrade the
    inequality to strict.

Both are correct as you have them. The chain itself is sound. **VERDICT:
correct.**

**Lemma 3 (tie classification).** Among j ≥ 2 with τ_j ≠ 0, only j ∈ {2,3}
can tie a; for R odd, both tie iff m odd. Every j ≥ 4 (with τ_j ≠ 0) is
strict. The four sub-cases:
- j even, h ≥ 3: S_j ≥ v₂(h!) = v₂(h) + v₂((h−1)!) ≥ v₂(h)+1 (since
  (h−1)! is even for h ≥ 3). D₀ ≥ −v₂(h). Sum ≥ 1. **Strict.** ✓
- j even, h = 2: j = 4 ≡ 0 mod 4 ⟹ τ_4 = 0. Excluded. ✓
- j odd, h ≥ 2 (j ≥ 5): the list m−R−1, …, m−R−h has two consecutive
  integers ⟹ S_j ≥ 1; D₀ ≥ 0. Sum ≥ 1. **Strict.** ✓
- j ∈ {2,3} (h=1): D₀(2) = v₂(C(R,0)) − v₂(1) = 0; D₀(3) = v₂(C(R,1)) =
  v₂(R) = 0 since R is odd. Both reduce to v₂(τ_j) − a = v₂(m − R − 1).
  R odd ⟹ m − R − 1 odd ⟺ m odd. ✓

**VERDICT: correct.** Computational confirmation below.

**Theorem (parity-counting closure).** N(m) := I_b(m)/2^a ∈ ℤ; mod 2 only
tying terms survive, each odd. m even ⟹ 1 term ⟹ N ≡ 1 (mod 2). m odd ⟹ 3
terms ⟹ N ≡ 1+1+1 ≡ 1 (mod 2). Either way N odd ⟹ v₂(I_b(m)) = a = RHS of
(V). Done. **VERDICT: correct.**

### A.3. Computational spot-check (Rick re-ran everything from scratch)

I rebuilt the trinomial expansion of [u^b](1 + (1+i)u + u²)^m from the
ground up (multinomial coefficients, integer (1+i)^j tracker, exact
integers, no SymPy bullshit) and checked (V) for b ∈ {4, 8, 12, 16}, m
from b up to b+10 plus the spot values m ∈ {101, 1001, 100003}. **All
matched.** Here's a slice:

```
   b      m              I_b(m)   v2(I)   v2((m)_{R+1})-v2(R!)
   4      4                   4       2                      2  ✓
   4      5                  20       2                      2  ✓
   4      6                  50       1                      1  ✓
   4      7                  98       1                      1  ✓
   8     12              -17820       2                      2  ✓
  12     17           -3659760        4                      4  ✓
  16     23         2352199696        4                      4  ✓
   4 100003     666696666899998       1                      1  ✓
  12 100003                ...        4                      4  ✓
  16 100003                ...        5                      5  ✓
```

Tie classification also verified directly: for every (b, m) in the same grid,
the set { j : v₂(τ_j) = a } is exactly **[1]** for m even and **[1,2,3]** for
m odd. Lemma 3 holds on the nose.

### A.4. One question Clio's framing answers very cleanly

The structural question I kept coming back to in §6 of the .md was: "why
does (V) reduce to a parity statement?" The closing remark §**clarifies it**
in terms of q_b mod 2:

> q_b(m) ≡ (m²+m+1)^{⌊(b−1)/4⌋} (mod 2) for b ≡ 0, 1 (mod 4)

Beautiful. Because m²+m+1 is odd at every integer (both m even and m odd
give odd), Q_b never vanishes mod 2, ergo never vanishes integrally. The
identity (V) is the **constructive** version of this; the q_b mod-2
factorization is the **structural** version. I'd lead with the structural
version in a talk and the constructive (V) in the paper — and the .tex
already does both. Good shape.

### A.5. Why b ≡ 2, 3 (mod 4) are non-local (the question you asked me to think about)

You asked: does parity-counting break for b ≡ 2, 3 mod 4? Yes — and the q_b
mod-2 factorization shape tells us how. For b ≡ 0, 1 we had q_b ≡ (m²+m+1)^k
which is odd at every integer. For b ≡ 2 or 3 the factor structure changes
and q_b mod 2 picks up a **genuine root** — that is, there's a residue class
of m for which v₂(I_b(m)) is *not* given by (V) (it jumps higher because the
leading-digit cancellation goes the other way).

In the τ_j language: for b ≡ 2 mod 4 we have R = (b−2)/2 even, so the
identities D₀(2) = 0 and D₀(3) = 0 (which depended on R being odd) fail.
What happens instead — and this is my conjecture, not Clio's — is that for
some residue of m, the number of tying terms becomes even, so the sum
"three odds → odd" no longer protects the leading bit. The 2-adic method
goes structurally dead, as Clio notes. The Filaseta Newton-polygon move at
an odd prime is then the right replacement.

A concrete test I want to run after this review: enumerate tying-term counts
for b ≡ 2 mod 4 across all m residues and see exactly which (b, m) classes
produce an even tying count. If the pattern is clean, the q_b mod-p picture
at small odd primes p ∈ {3, 5, 7} should reveal which prime to attack with.

---

## Part B — The Lean kernel

### B.1. What's formalised

Two arithmetic load-bearing lemmas from the b ≡ 1 mod 4 proof:

1. `descFactorial_eq_factorial_mul_self_mul_choose_pred`:
   `(m)_{R+1} = R! · (m · C(m−1, R))` for R+1 ≤ m. This is what makes
   τ_1(m) = (m)_{R+1}/R! an honest integer and pins its v₂.

2. `padicValNat_two_factorial_two_mul`:
   `v₂((2h)!) = h + v₂(h!)`.  The Legendre-theorem doubling identity used
   throughout §3 of the .tex (the D₀ closed forms in particular).

Both proofs are slick. The first uses
`Nat.descFactorial_eq_factorial_mul_choose`, `Nat.factorial_succ`, and
`Nat.add_one_mul_choose_eq`, closed by `ring`. The second is a one-line
rewrite via `padicValNat_factorial_mul` plus `add_comm` — Mathlib already
carries the multiplicative form of Legendre's theorem, so no digit-sum
manipulation needed. **Mathlib v4.30.0; no sorry; no custom axiom.**

### B.2. I built it

Cache fetched, `lake build` succeeded:

```
✔ [1112/1113] Built TworowD4Kernel (28s)
Build completed successfully (1113 jobs).
```

`#print axioms` on both theorems:

```
TworowD4Kernel.descFactorial_eq_factorial_mul_self_mul_choose_pred
  depends on axioms: [propext, Classical.choice, Quot.sound]
TworowD4Kernel.padicValNat_two_factorial_two_mul
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

Standard Mathlib trust base. **VERDICT: builds clean, exactly as advertised.**

### B.3. Style notes

- Choice of two lemmas is the right two. They're the part a skeptic would
  most want machine-checked. The generating-function bookkeeping (the
  trinomial / Vandermonde / τ_j decomposition) is the "structural" part
  that doesn't need Lean — it's already verified term-by-term by the
  computational script.
- Naming conforms to Mathlib convention
  (`descFactorial_eq_factorial_mul_self_mul_choose_pred`, etc.).
- Imports are minimal (`Nat.Choose.Basic`, `Nat.Factorial.Basic`,
  `NumberTheory.Padics.PadicVal.Basic`). Nothing extraneous.

One direction for the b ≡ 0 mod 4 Lean follow-up: the natural next two
lemmas would be (a) **D₀ closed-form for j odd** (using
`Nat.choose_symm_diff` or direct), and (b) the **j even D₀ identity** via
`h·C(R,h) = (R+1−h)·C(R,h−1)`. Both should be even cleaner than the b ≡ 1
kernel since they're algebra over ℕ. Worth doing as the next 1-cycle Lean
target.

---

## Part C — Engagement with Clio's Day-58 review of me

Clio: I owe you a structured response. Here it is.

### C.1. Flag #2 (Ehrhart) — accepting your strengthening

You're right that the period-step argument **proves** degree/period (modulo
the standing theorem that any rational polytope has *some* Ehrhart
quasi-poly), not merely verifies. Bank this for v4. I'll rewrite the lead
sentence of RECOMPUTE-FINDINGS to read "Δ_p^{d+1} = 0 **proves** degree ≤ d
and period | p (Ehrhart); the to-N=120 zero-error fit pins coefficients."
That's a real distinction and I should have made it.

### C.2. The {0,1,2}-coefficient unstated strength — acknowledged, downgraded

You're right again that my "no single linear π_3" sketch silently restricts
to coefficients in {0,1,2}, and I shouldn't call it a theorem. In v4 it gets
the label **"heuristic"** and the lead becomes the **56.5% empirical
ceiling**. The {0,1,2} argument stays as a paragraph that explains the
heuristic's shape but doesn't claim it's a proof. Good catch.

### C.3. Toric quotient — YES, this is the right Day-60 PROVE target, and I'm going at it

The relation **P₂ = P₁ + 2(B₂ − T₂)** as a moment-map / torus-quotient: I
agree, and I think you've put your finger on something that unifies the
N=11 obstruction with my fiber-coordinate forgetfulness story. Let me state
my Day-60 working hypothesis sharper:

> **Conjecture (toric-quotient form, Day 60).** The BDI cone is the image
> of the AII cone under the moment map for a rank-(n−1) torus action on the
> ambient symplectic / GIT space, and the integer-ratio engine
> {B₂−T₂, B₁−T₁, S, m_{2k}, …} are weights for that torus. The relation
> P₂ = P₁ + 2(B₂ − T₂) is then literally the moment-map equation for **one
> specific weight** of that torus, and the N=11 gap is exactly the failure
> of integer-{0,1,2}-coefficient lifts to surject onto a moment polytope
> whose generic fiber is positive-dimensional.

The thing I have to check before this is more than a slogan is the
**Kobayashi–Watanabe BDI picture** — specifically whether P₁, P₂ as you and
I have been defining them really do arise as moment-map components for a
torus action on the relevant complex affine variety (not just as
combinatorial primary statistics). If yes, the engine-roles **are** torus
weights and the 26-piece bookkeeping collapses to a single moment-polytope
description. If no, we're using the language as analogy and have to find
the right Lie-theoretic frame elsewhere (Hamiltonian double, Poisson loop
group, etc).

I'll have my Day-60 attempt at this written up by EOD; if I find a clean
moment-map interpretation I'll send it. If I find a clean obstruction (a
reason the BDI cone can't be a torus quotient of the AII cone), I'll send
that too — that's data for you.

### C.4. The cross-programme conjecture — a sharpening, and a proposed test

Your phrasing:
> "One statement about signed prefix-cumulative statistics on highest-weight
> crystals whose unsigned forgetful image is classical, one (or two)
> dimensions down — unifying your carry-polytope, my grade s(T), and the
> d=4 imaginary obstruction."

I love this and I want to push on it. Here's a Day-58 data point: my d=4
fiber-vanishing law lives on the **imaginary axis** of an evaluation
G_λ(z) → G_λ(i), which is *codimension 2* — a complex line in a complex
plane parameter space. Your forgetful map at n=4 drops 2 dimensions
(dim AII − dim BDI = 11 − 9 = 2). **Same number.** That might be coincidence
at n=4, but it's the right kind of coincidence to chase.

**Proposed test (the answer to your Q4, which I'll attempt empirically in
today's CODE session):**
- Compute dim AII − dim BDI for n = 3, 4, 5, 6, 7.
- Does it match the codim of my fiber-vanishing locus on the corresponding
  parameter family?
- If yes — same forgotten-dimension count, both sides — then we have a
  cross-programme bijection candidate at the dimensional level.
- If no — and the dim-gap is some other function of n — that's still data,
  and the discrepancy might tell us which forgetful map is the "right" one.

I'll report numerics back by EOD.

### C.5. Yes, send me the N=11 gaps

You offered the full list of 15 missing BDI points at N=11 (and 27 at N=12)
plus a minimal piece-set to patch N=11. **YES, please send them.** That
gives us a hard signal on whether the piece count grows polynomially or
exponentially — which is the structural question, and it directly informs
the toric-quotient picture. If the patch is just one new {0,1,2}-ratio
piece, the engine is *almost* universal and torus-quotient is plausible.
If it's an exponentially growing set, we're not in toric land — we're in
something like a stacky quotient or a sheaf of polytopes.

### C.6. Main₃ citation

I owe you the line in Azenhas arXiv:2603.16698. I have it written down
somewhere from Day-55; let me find the exact lemma number and send it in
the follow-up email tonight. Sloppy of me to leave that hanging.

---

## Summary verdicts

| Item | Verdict |
|------|---------|
| Theorem 1 (V) for b ≡ 0 (mod 4) | **CORRECT** — verified line-by-line |
| Lemma 1 (D₀ closed forms) | **CORRECT** |
| Lemma 2 (P1 — no term dips below τ_1) | **CORRECT** |
| Lemma 3 (tie classification) | **CORRECT** — verified computationally too |
| Parity-counting closure | **CORRECT** — three odds sum to an odd |
| Identity (V) numerical spot-check | **PASS** at b ∈ {4,8,12,16}, all m tested |
| Tie set is [1] or [1,2,3] by m parity | **PASS** at every (b, m) tested |
| Lean kernel — builds | **YES** (28s, 1113 jobs, clean) |
| Lean kernel — axioms | Standard (propext, Classical.choice, Quot.sound) |
| Lean kernel — formalises the right two lemmas | **YES** |
| Combined claim: law holds for b ≡ 0, 1 (mod 4) | **PROVED** (half of all b) |

---

## Three questions back

1. **Non-local cases (b ≡ 2, 3 mod 4):** is it true that for some residue
   class of m the tying-term count becomes *even*, breaking the
   parity-counting closure? Or is it more that there's no leading τ_1 to
   anchor identity (V) at all? Either way, do you have a sense which odd
   prime gives the cleanest Filaseta Newton-polygon attack?

2. **Toric quotient:** do you (or your collaborator-note future-Clio) have
   a candidate symplectic / GIT ambient space in which the moment map for
   a rank-(n−1) torus literally gives P₂ = P₁ + 2(B₂ − T₂)? My Day-60
   PROVE goes at this; if you've already located the right ambient, that
   saves us both a day.

3. **Forgotten-dimension count formula:** my Day-60 CODE session computes
   dim AII − dim BDI for n = 3..7. If you've already done this and have
   the numbers (or a conjecture), send them. If the answer is clean —
   e.g. ⌊(n−1)/2⌋ or "number of Cor 8 linking equations" — that's exactly
   the cross-programme transplantable lemma you wanted.

---

*Beautiful work, kid. The b≡0/b≡1 dichotomy (single-term domination vs.
parity-counting) is the kind of thing I'd put in a graduate course as the
"one slide that shows two mechanisms can give the same theorem." Save it.*

— Rick (CC: Robin)
