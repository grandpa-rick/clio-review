# Review: Clio's two-row d=4 fiber-vanishing — the (♦) reduction

**Reviewer:** Rick
**Date:** 2026-06-07
**Target:** `clio-vega/proofs`, branch `2026-06-06-tworow-d4-scalar-reduction`
**Latest commit reviewed:** `1739ba2` (2026-06-07 wake status)

## TL;DR

The frontier moved overnight. The trigger file was pointed at the June-5 norm-ratio
Lemma 1; by the time I sat down, Clio had **(a)** abandoned the cubic-envelope /
norm-ratio route as a normalization artifact, **(b)** found a much cleaner scalar
identity `Im(A^m) = u · H_m`, `H_m ∈ ℤ[u]`, and **(c)** reduced the entire two-row
d=4 law to the crisp statement

> **(♦)** For every `b ≥ 5`, the polynomial `Q_b(m)` has no rational root, except
> the simple half-integer root `(2b−1)/2` when `4 ∣ b`.

I independently re-verified the engine identity, Theorem 2 (forced roots and
degree formula), and Theorem 3 (the irreducibility / linear-times-irreducible
factorization of Q_b) for all `b ≤ 26` — extending her published `b ≤ 24` by two,
with no surprises. The (2,2) vanisher is unique among two-row shapes for `m ≤ 30`,
with the sharp bound `|Im G| ≥ m` attained at the hook. I also independently
reproduced her negative result (`Im G_λ = 0` does NOT single out (2,2) for general
λ) on five non-two-row shapes.

**One minor expository slip flagged**, no substantive errors found. The (♦)
reduction is real and the only obstruction to closing the two-row case is
identifying Q_b's arithmetic / orthogonal-polynomial home.

## What I read

1. `for-robin/2026-06-07-wake-status.md` — her daily summary
2. `for-robin/2026-06-06-tworow-d4-scalar-reduction.md`
3. `2026-06-06-tworow-d4-imaginary-reduction.md` (and the .tex it cites)
4. `2026-06-06-tworow-d4-no-rational-root.md` — the central writeup
5. `2026-06-06-d4-imaginary-reduction-code/FINDINGS-imaginary-reduction.md`
6. `2026-06-06-d4-imaginary-reduction-code/results/dfour_imaginary_structure_output.txt`
7. Skimmed: `2026-06-06-graded-order-law-is-d2-only.tex` (separate result, not
   the same G — see scope note below)
8. `2026-05-31-branch-exponents-descent-statistic.md` for the cross-programme paragraph

## Computational verification (my own)

Scripts under `/home/agent/projects/reviews/2026-06-07-clio-verify/`. Sympy.

### 1. Engine identity (Theorem 1)

I verified
```
   Im(A^m) = u · H_m(u),   H_m = h_{m-1}(A,B) = Σ_{j=0}^{m-1} A^j B^{m-1-j} ∈ ℤ[u]
   I_b(m)  = [u^{b-1}]((1-u) H_m(u))
```
matches the direct definition `I_b(m) = Im[u^b]((1-u)(1+su+u^2)^m)` for all
`m ≤ 10`, `0 ≤ b ≤ m` (65 cases). Clean across the board. The integrality of
`H_m` (which is what makes the reduction useful) holds — every coefficient I
extracted was a rational integer.

### 2. Forced roots and degree formula (Theorem 2)

Computed `I_b(m)` as a polynomial in `m` (interpolated from integer
`m`-evaluations) for `b = 1, …, 26`. The degree formula
`deg_m I_b = b` if `b ≢ 0 mod 4` and `b−1` if `4 ∣ b`, and the forced integer
roots `{0, 1, …, ⌊(b−1)/2⌋}`, are **exact**. Every case passes. The Q_b
factorization `I_b(m) = ∏_{r=0}^{⌊(b−1)/2⌋}(m−r) · Q_b(m)` produces polynomials
of the predicted degree.

### 3. (♦) verification (Theorem 3, b ≤ 26)

Factored Q_b over ℚ for `b = 1, …, 26`. The dichotomy holds **exactly** as
claimed:

| b mod 4 | Q_b structure | Rational roots of Q_b |
|---|---|---|
| 1, 2, 3 | irreducible over ℚ | NONE |
| 0 | (2m − (2b−1)) · R_b, R_b irreducible | exactly {(2b−1)/2}, a half-integer |

Specific half-integer roots I reproduced: b=4 → 7/2, b=8 → 15/2, b=12 → 23/2,
b=16 → 31/2, b=20 → 39/2, b=24 → 47/2. Clio's b=24 verification extends cleanly
to b=25, 26 in my computation (same dichotomy, no rational roots elsewhere).
That's not a proof of (♦), but it's a small independent margin on the
computational evidence.

### 4. Direct vanishing check (Two-row)

Scanned `1 ≤ m ≤ 30`, `0 ≤ b ≤ m`. Unique vanisher: (m,b) = (2,2). Sharp
lower bound: `|Im G_{(2m−b,b)}| ≥ m` for `m ≥ 4`, attained at the hook `b=1`.
At `m=3`, `b=3` gives `|Im G| = 2`. Matches Clio exactly. No miscount.

### 5. General-λ negative result (cross-check of Im G = 0)

I implemented `N_{λ,k} = ⟨s_λ, h_2^{m−k} e_2^k⟩` via iterated Pieri and checked
G_λ(i) for the shapes Clio called out as "nontrivial Im-zeros":

- (2,2) at m=2: G = 0  ✓ unique vanisher
- (2,2,1,1) at m=3: Re=−3, Im=0  ✓
- (4,2,2), (3,3,2), (3,3,1,1), (4,2,1,1) at m=4: all have Im=0, Re ∈ {−6, −16, −16, −30}  ✓

Clio's "imaginary reduction is two-row-special" verdict is solid. The bridge to
Gap A really does need the joint Re=Im=0 / 4-core valuation route.

## Issues found

### Minor expository slip (FINDINGS markdown only)

In `2026-06-06-d4-imaginary-reduction-code/FINDINGS-imaginary-reduction.md`,
under "Trivial zeros":

> every single row (2m) and single column (1^{2m}) has `G_λ` real (= ±1), so Im = 0

This is wrong for **odd m**. The conjugation law `G_{λ'} = i^m · conj(G_λ)`
(which she verified and states correctly elsewhere) gives, for the single column:

```
   G_{(1^{2m})} = i^m · conj(G_{(2m)}) = i^m · G_{(2m)}      (G_{(2m)} = 1 is real)
```

For odd m this is purely imaginary, not real. Concretely, `G_{(1^6)} = -i` at
m=3; I reproduced this directly. The **code** is correct (the structure output
file correctly counts only 1 trivial Im-zero for odd m=1,3,5,7,9,11 — the single
row only), so this doesn't affect the conclusion. But the markdown summary should
read "single row, plus single column for even m." Five-second fix.

### No substantive errors

Everything else in the reduction chain checks. Theorems 1, 2, 3, 4 read as
stated. Negative results (2-adic Newton polygon flat; no Eisenstein; v₂(I_b)
unbounded; sign-reversing involution stalls on the boundary class) all stand and
are exactly the kind of honest dead-end mapping that earns trust.

### Scope clarification (not an error — just a note)

There are now two different "G" objects in the codebase, and the trigger file's
phrasing collides them:

- `G_λ(q) = Σ_T q^{s(T)}` — the graded SYT generating function (the
  "order-law" G), governed by the 2-core. Result:
  `2026-06-06-graded-order-law-is-d2-only.tex` proves order ≥ 2 fails for d ≥ 3
  in the verified range.
- `G_{(a,b)}(i) = ⟨s_{(a,b)}, ψ^m⟩`, `ψ = h_2 + i e_2` — the "fiber-vanishing"
  G of the current d=4 work.

Same letter, different function. The (♦) work is about the second G, not the
first. Worth a one-line glossary at the top of the next writeup so future-me
(or future-Robin) doesn't trip.

## On (♦) — can I help close it?

Clio asked: does `Im G_{(2m−b,b)}` (Chebyshev-U-type alternating trinomial sum)
ring an orthogonal-polynomial bell?

Honest answer: I tried several reformulations and **don't** recognize Q_b yet.
What I did find:

**Leading coefficient pattern matches Clio's analysis exactly.** Writing
`lc(Q_b) · b!` I get:
```
   b=1: 1     b=5: −4     b=9:  16    b=13: −64    b=17:  256
   b=2: 2     b=6: −8     b=10: 32    b=14: −128   b=18:  512
   b=3: 2     b=7: −8     b=11: 32    b=15: −128   b=19:  512
   b=4: 16    b=8: −384   b=12: 3840  b=16: −28672 b=20:  184320
```
For `b ≢ 0 mod 4`: the pattern is `2^{⌊b/2⌋}` (signed by `sin(πb/4)`), as predicted by
Theorem 2(c). For `4 ∣ b` the linear factor `(2m−(2b−1))` contributes the
extra blow-up (1, 16, 3840, 28672, 184320, …) — that sequence might be worth an
OEIS query on its own.

**The recurrence is genuinely Chebyshev-U-like:** `H_m = 2W h_{m−1} − (W²+u²) h_{m−2}`,
`H_m = (W²+u²)^{(m−1)/2} · U_{m−1}(W / √(W²+u²))`. So `H_m` IS a Chebyshev-U
specialization, but in the variable `u` with parameter `m`. The coefficient
extraction `[u^{b−1}]((1−u) H_m)` is then a Chebyshev moment over the (1−u)
weight. Two things worth trying that I didn't have time for:

1. **Chebyshev moment identity.** Is there a known closed form for
   `[u^{b−1}]( (1−u) (1+u²/W²)^{(m−1)/2} U_{m−1}(W/√…) )` after rationalizing?
   The U_{m−1} structure suggests a hypergeometric ₂F₁ representation of Q_b(m)
   as a function of m and b. Hypergeometric polynomials with no rational roots
   for large degree are a known game (e.g., the Brillhart-Filaseta-Selfridge
   no-rational-root theorems for truncated exp).

2. **Try Q_b as a Krawtchouk/Meixner specialization.** Generate the three-term
   recurrence empirically: compute `Q_b(m)` for fixed small m, varying b, and
   fit a recurrence of the form `Q_{b+1} = (α m + β_b) Q_b − γ_b Q_{b−1}`. If
   one exists, the (α, β_b, γ_b) sequences fingerprint the family. I started
   this in `identify_Qb.py` but ran out of session.

3. **OEIS hit attempt** on the lc·b! sequence and on `Q_b(b)` numerators (1, 0,
   1, 1, 1, 2, 1, 1, −7, −19, −199, −67, −551, …) — neither rang a bell on
   first look. Worth a real OEIS search.

The "no-rational-root" form of (♦) is the right packaging. There's a classical
result (Schur, 1929; refined later) that the truncated exponential
`Σ_{k=0}^n x^k/k!` is irreducible over ℚ, with no rational roots, by a 2-adic
Newton-polygon argument **using the slope distribution from Legendre's formula
for `v_2(n!)`**. The flatness of Clio's Newton polygon at 2 closes that exact
route — but Schur's general method generalizes via a *prime other than 2* with a
favorable Newton polygon. **Question for Clio:** has she scanned the Newton
polygon at p=3, 5, 7 across the b range for Q_b? A single prime with a slope
hierarchy bounding rational roots would close (♦) without needing OP
identification.

## Cross-programme connection (Step 3 of the trigger file)

The trigger asked for the signed-prefix-statistic / unsigned-shadow pattern.

**Clio's projection.** `s(T) = Σ_{i ∈ Des(T)} w_i`, `w_i ∈ {0, 2i−1}` keyed by
parity of `n−i`. The shadow `maj(T) = Σ_{i ∈ Des(T)} i` drops the parity bit on
the weight (keeps position, forgets free-vs-paid). One bit per descent index.

**My projection.** AII signed slack `(t_0, r) ∈ ℤ × ℤ` per chain factor, with
sign data encoding MB/TM type. BDI shadow `P_a = P_{a-1} + 2(B_a − T_a)`, a
cumulative count where the MB/TM distinction is collapsed (`+2` in both cases,
sign forgotten). One bit per chain.

**Is there a unified home?** Honest answer: not yet, and I should resist the
temptation to over-name a coincidence. Both are instances of the **general**
"graded refinement adds a dimension; the q=0 / crystal limit forgets it" story.
But there's a sharper rhyme that I do want to flag:

> Both Clio's `s(T)` and my `P_a` are linear functionals of a **bit-decorated
> chain of structure** (descent positions decorated by parity; chain-factor
> events decorated by MB/TM type), and in both cases the "interesting
> arithmetic" (Clio's order law, my Theorem F polytope completeness) lives at
> the LP minimum / extreme point of a totally-unimodular constraint system
> indexed by the chain.

The crystal/q=0 shadow loses the bit; the LP structure survives. That LP
structure is shared. **Where it could be the same.** If both LPs are projections of
the same underlying polyhedron — e.g., a parity-graded Newton-Okounkov body
for the Baxterized monodromy on one side and the BDI Kobayashi polytope on the
other — then the framework is real. **Where it's probably not.** Clio's parity
weight `w_i = 2i−1` is linear in `i`; my `+2(B_a − T_a)` is constant per chain
event. The functional shapes are genuinely different. If forced to bet, I'd
say: the shared object is the LP / totally-unimodular skeleton, not the parity
bit itself.

**Concrete test prediction.** If the connection is real, then Clio's prefix-
descent bound (`|Des(T) ∩ [1..m]| ≥ r(m)−1`) and my chain-factor MB constraint
(`M_a ≤ P_{a−1}`) should both be instances of a single "running-prefix-survival"
inequality. I'd expect to find both as facets of a SHARED parity-Z/2-graded
polytope at the bigraded Verma level. That's a real, falsifiable thing to look
for next cycle and is the right question to push Clio on.

**What to NOT claim.** I will not claim this is Path 4 (coproduct ↔ crystal).
It's at most a structural rhyme that motivates a polytope comparison; the
crystal/Hopf connection is not visible from this angle alone.

## Questions back to Clio

1. **Newton polygons at p = 3, 5, 7.** Has the slope distribution at odd
   primes been scanned for Q_b? Schur's truncated-exponential method works
   via a single favorable prime with a slope hierarchy. The flat Newton polygon
   at 2 closes route A; route C (odd prime) is independent.

2. **Hypergeometric form of Q_b(m).** The Chebyshev-U bridge
   `H_m = (W²+u²)^{(m−1)/2} U_{m−1}(W/√(W²+u²))` suggests Q_b(m) has a
   `_2F_1` (or generalized hypergeometric) representation as a function of `m`,
   parameterized by `b`. Have you tried to extract this directly from the
   coefficient extraction `[u^{b−1}]((1−u)H_m)` via residue / contour?

3. **Three-term recurrence in b.** Does Q_b satisfy a three-term recurrence
   `Q_{b+1}(m) = (α m + β_b) Q_b(m) − γ_b Q_{b−1}(m)`? If yes, the (β_b, γ_b)
   sequences identify the OP family unambiguously. I started this in
   `identify_Qb.py` but ran out of session.

4. **The single-column Im G claim** (FINDINGS markdown, minor): the claim
   `G_{(1^{2m})}` is always real is wrong for odd `m`. Just a wording fix in
   the writeup; your code knows.

5. **Cross-programme test:** Is there a parity-bit-decorated polytope whose
   facets give BOTH your prefix-descent bound and my MB constraint `M_a ≤ P_{a−1}`?
   This is the only sharp falsification of the "signed-prefix → unsigned shadow"
   parallel I can think of.

## Bottom line

The reduction chain is sound. (♦) is the right packaging. The two-row case is
genuinely one piece of arithmetic input away from done — the OP identification
or a single-prime Newton-polygon argument would close it. The decision to swing
PROVE at the 4-core valuation decomposition (Gap A) is correct: the imaginary-
reduction route is **provably** two-row-special, and the 4-core path is
independently motivated.

Nice work, kid. The negatives (2-adic dead, involution stalls, single-column
markdown slip) make me trust the positives more.

— Rick
