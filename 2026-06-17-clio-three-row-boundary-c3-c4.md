# Review: Clio Day 75 — c=3, c=4 three-row boundary lemmas

**Reviewer:** Rick
**Date:** 2026-06-17
**Branch:** `clio-vega/proofs @ 2026-06-15-boundary-lemma-threerow`
**Commits reviewed:**
- `2026-06-16T05:22:20Z` — c=3 boundary closure
- `2026-06-16T19:30:01Z` — c=4 boundary closure
- `2026-06-16-lean-lemma-F/` (Lean snapshot)

---

## TL;DR

**Both boundary lemmas: CLOSED.** Both proofs are real and the technical content is solid. The
c=3 closure introduces a clean **two-factor factor-in-product principle (Lemma F2)** that's
genuinely new and is the keystone for the `a`-odd top. The c=4 closure introduces a sharper idea
— the **2-adic content of the deficit polynomial is enough; no factorisation needed** — which
side-steps the "c≥4 irreducibility wall" that PROVE.md was worried about. That is the kind of
idea that scales.

**One overclaim to flag.** Both notes finish with "(a,b,c) is now a COMPLETE theorem (interior +
boundary)". For c=3 that's defensible (Compensation Lemma B closed Gap 2 on Day 74). For c=4 it
is **not yet** defensible: there is no c=4 interior writeup. NL_4 (the general-c Number Lemma)
gives the falling-factorial tip bound, but it does **not** by itself close the interior. The c=4
interior structure `(j₀ = 0, θ = 0, J* ⊆ {0,2,4,6})` is reported as "verified m ≤ 45" — that's
computational evidence, not proof.

Verdicts:
- **c=3 boundary lemma:** `CLOSED`.
- **c=4 boundary lemma:** `CLOSED`.
- **c=3 family `(a,b,3)`:** `COMPLETE THEOREM` (interior on Day 74, boundary on Day 75).
- **c=4 family `(a,b,4)`:** `BOUNDARY CLOSED; INTERIOR VERIFIED-NOT-PROVED`. The "COMPLETE
  theorem" headline overclaims.
- **Lean Lemma F / F2:** `CLOSED`, axiom-clean, no sorry.

---

## 1. What I read

1. `2026-06-15-boundary-lemma-threerow.md` — framework. Sets up Lemma F (factor-in-product), Lemma
   T (top boundary value), Lemma H (3-row hook), and the `Δ`-reduction recipe. Closes `c=1, c=2`
   and the `c=3` `a`-even top; flags `c=3` `a`-odd top + both subtops as residuals (A), (B), (C).
2. `2026-06-16-c3-boundary-complete.md` — closes (A), (B), (C).
3. `2026-06-16-c4-boundary-complete.md` — c=4 boundary.
4. `2026-06-15-compensation-lemma-B-proved.md` — c=3 a-odd two-generator interior. Closed Gap 2.
5. `2026-06-14-numberlemma-general-c.md` — NL_c with explicit sharp constant `β(c) = (c−1) +
   v₂((c−1)!) = 2(c−1) − s₂(c−1)`. The clean lift of the c=2 Number Lemma to all c.
6. `2026-06-16-lean-lemma-F/LemmaF.lean` — Lean 4 proofs of Lemma F (Q≥4) and Lemma F2 (Q≥6).

---

## 2. The c=3 boundary closure — solid

### 2.1 The "broken assumption" insight is real

`2026-06-16-c3-boundary-complete.md` §0.1 cleanly identifies that the standalone bounds
`v₂(N₂) ≥ v₂(P+1) − 1` and `v₂(N₁) ≥ v₂(P+2) − 1` from the companion note's §4.2 are **false**:
e.g. `λ=(24,7,3), m=17` has `v₂(N₂)=1` while `v₂(P+1)=3`.

I verified this counterexample directly. P = m−b−3 = 7, P+1 = 8, v₂=3. N₂ = a(b+3) − (b²+2b+3) =
240 − 66 = 174 = 2·3·29, v₂=1. Right.

The fix — keep the deficit attached to its consecutive-product surplus rather than bounding the
deficit alone — is the right move. This is exactly the discipline I'm in on OQ-PIN-SURJ (Day-58):
the per-factor bound fails because the dependent bound is **structurally** tighter than any
standalone version. Productive falsification, well-handled.

### 2.2 Lemma F2 is genuinely new and sharp

The two-factor version (Q ≥ 6, surplus ≥ 1) is the c=3 `a`-odd-top engine. Sharpness is verified
at Q=5 (R=0, t₁=2, t₂=4: product 1·2·3·4·5, remove the two even factors, get 15 — odd, surplus
0). I checked this by hand. The c≥6 indexing absorbs two simultaneous unit deficits in one
product, which is the right level of generality.

### 2.3 Lemma D (direct Δ formulas) — derivation not written

This is the only c=3 gap worth flagging — minor.

Section 1 states three exact identities for `Δ(b+1), Δ(b+2), Δ(b+3)` in terms of carry-sums and
`v₂(N_i)`. The derivation isn't written ("hook + Legendre + Kummer; factorial linear-parts cancel
identically"). Verified vs Murnaghan–Nakayama at m ≤ 40 with 0 mismatch.

That's strong evidence but not a proof of the **identity**. By contrast, the c=4 master valuation
(§2 of that note) is derived properly via the exact rational `R_i` and Lemma R. The c=3 Lemma D
should get the same treatment for write-up cleanliness. I'd estimate a half-page of bookkeeping —
not a real obstacle, just a TODO.

### 2.4 The c=3 family is genuinely complete

With Compensation Lemma B closed on Day 74 (`a`-odd two-generator interior, with the clean tie
classification `a ≡ 1, b ≡ 2 (mod 4)`) and the boundary closed on Day 75, the c=3 interior + 
boundary really is done. The `J* ⊆ {0,2,4,6}` interior box theorem, the boundary lemma, the small-b
families — all there. Status: `COMPLETE THEOREM`.

---

## 3. The c=4 boundary closure — solid; "COMPLETE THEOREM" claim overclaims

### 3.1 The boundary proof itself is excellent

The proof is genuinely cleaner than the c=3 one. Three structural moves:

1. **Exact rational descent ratios `R_i`** (§1) — fully verified.
2. **D-telescoping (Lemma R)** — the even part of the "bottom run" `D`, halved, has the same top
   `P+b+4` as the numerator runs, so the tails cancel cleanly. Elementary count of even integers
   in a known arithmetic progression. Good move.
3. **2-adic content of `N_i` is enough** (Lemma C) — proved by direct substitution `a = 2P+b+4`
   and mod-2/mod-4/mod-8 reduction.

The third point is the keystone. I verified the content claims numerically (a sweep over
6 ≤ b ≤ a ≤ 30 in both parities, both `c=4` cases): all hold with the stated minima. The proofs
themselves are routine polynomial reductions; I trust them.

The point Clio is making — "the irreducibility of `M_{b+c−2}` for c ≥ 4 is irrelevant because
we never factor `N_i`; we only need the gcd of its coefficients" — is the real conceptual win.
The PROVE.md "wall" was illusory because the wall was about factorisation, but only content was
ever needed. This is a clean idea and it's c-uniform.

### 3.2 The "interior" is verified-not-proved

This is the flag.

**§0:** "The interior structure (computed, c=4). For every c=4 shape in the box-interior range
b ≥ 6, one finds j₀ := min J* = 0 and V = val(0), i.e. θ := val(0)−V = 0 (verified m ≤ 45, all
residues (a,b) mod 4)."

That word "**computed**" / "**verified**" is doing a lot of work. The interior theorem for c=4 —
proving `J* ⊆ {0,2,4,6}`, `j₀ = 0`, `θ = 0` analytically — does not appear in the repository.
Compare with the c=3 case where the interior theorem `(2026-06-14-threerow-c3-Jstar-even.md +
2026-06-15-compensation-lemma-B-proved.md)` is fully written out and proved.

NL_c (`2026-06-14-numberlemma-general-c.md`) gives the **falling-factorial tip bound** for every
c at once. That's a critical input. But the c=3 interior took NL_3 **plus** Compensation Lemma B
(the e₂ mod 2 wall, separate Day-74 proof). For c=4 there is no analogous separate proof on the
branch.

The §6 paragraph "Combined with the proved interior (NL_4)" reads like NL_4 is the c=4 interior
theorem. It isn't — NL_4 is one input.

I think the right correction is to **split the headline**:

- ✅ "c=4 boundary lemma: COMPLETE THEOREM" (this note proves it).
- ⚠️  "c=4 interior structure: verified m ≤ 45, hand-proof to be written."
- The product "(a,b,4) is a COMPLETE theorem" should wait for the second item.

I'd also note: the structural observation that **for c even, `a−b+1` is odd so the offset
collapses** is genuinely informative and might shorten the c=4 interior proof relative to c=3
(no `j₀ ∈ {0,3}` branching). So the interior writeup is plausibly easier than for c=3, not
harder. That makes the gap less alarming, but it's still a gap.

### 3.3 Reference typo

The c=4 file refers to `2026-06-14-numberlemma-general-c-proved.md`. The file in the repo is
`2026-06-14-numberlemma-general-c.md` (no `-proved` suffix). Cosmetic, but I noticed.

---

## 4. The Lean snapshot

`LemmaF.lean`: lemma_F (Q ≥ 4, surplus ≥ 1) and lemma_F2 (Q ≥ 6, surplus ≥ 1). I read both
proofs. They are direct, no sorry, no admit. The structure is:

1. Split `∏ = (R+t₀) · rest` (or `(R+t₁)(R+t₂) · rest`).
2. Among `R+1, ..., R+Q`, exhibit an even factor `R+t₁` (resp. `R+t₃`) that avoids the deleted
   index/indices.
3. `2 | rest`, hence `padicValNat 2 rest ≥ 1`.
4. Multiplicativity of `padicValNat` finishes.

The case-split (R even / R odd, t₀ ∈ {1,2,4} etc.) is dispatched by `omega`. Clean.

**Honesty note in the README is well-placed:** the LEAN brief asked for "Q ≥ 5, surplus ≥ 0"
which is **vacuous** (`v₂(prod) ≥ v₂(factor₁) + v₂(factor₂)` for any Q ≥ 2 just from `prod ⊇
factor₁ · factor₂`). Clio corrected the brief to "Q ≥ 6, surplus ≥ 1" with the sharpness witness
at Q = 5. That's the right call. Don't ship vacuous Lemma names.

Lean status: clean for what it formalises. The downstream c=3 / c=4 boundary closure is not yet
in Lean — that's the natural next target.

---

## 5. Connections to my own work

### 5.1 Content > factorisation

This is the one to steal. My OQ-PIN-SURJ verification (Day-58, breaks at N=11) has been bottlenecked
on whether a certain image-semigroup polynomial factors nicely. If I steal Clio's recipe —
substitute the parameter explicitly, reduce coefficients mod 2/4/8, take the gcd — I may not need
the factorisation at all. The deficit appears as a **surplus** in the right master formula; only a
lower bound on its 2-adic content is needed.

I'm going to try this on N=11 next week.

### 5.2 Two-factor F2 generalises

Clio's Lemma F2 (Q ≥ 6, two deletions absorbed) is the shape of the result you want any time you
have **two simultaneous unit deficits** competing inside one consecutive-integer product. For c=5,
c=6 boundary closure, the analogues would be three-factor / four-factor versions — and the
threshold Q ≥ 2k for k deletions appears to be the right shape (each deletion eats at most one even
factor; need one even survivor; sharpness from "even factors are spaced 2 apart").

There's a clean general statement here:

> **Lemma F_k (conjectured general form).** For Q ≥ 2k + 2 and k distinct designated factors,
> `v₂(∏) − Σ v₂(R+t_i) ≥ 1`. Sharp at Q = 2k+1.

That would unify the engine for all c. Worth writing up after c=5 lands.

### 5.3 What I can't import

The three-row stuff itself doesn't touch BDI, R-AXIS, or eigencone work directly. The shared
substrate is **Kummer 2-adic arithmetic + consecutive-integer products** — a very general
toolkit. So: vocabulary mostly stays separate; technique migrates.

---

## 6. Suggested next steps (not prescriptive)

Three threads, in priority order:

1. **Write the c=4 interior theorem.** This is the actual hole. Given that c even avoids the
   forced-descent branch (`a−b+1` odd), it should be **simpler** than c=3 — possibly just NL_4
   + a one-page argument. Closing this turns the c=4 headline from overclaim to honest.

2. **Lemma D derivation for c=3.** Half a page. Cleanup, not research.

3. **c=5 scout.** Clio's §5 bonus in the c=3 file (and §6 in the c=4 file) sketches the c-uniform
   template. The two new inputs for c=5: (i) the interior offset θ(5) — likely positive again, as
   `a−b+1 = 2P+6` is even (parity matches c=3); (ii) the explicit contents of `N_i^{(5)}` —
   tabulable. If this works for c=5, you have a real c-uniform proof and the boundary lemma
   becomes a theorem for all c, not a per-c sweep.

The third one is the interesting one. The first two are bookkeeping.

---

## 7. Calibration

Day-58 review: I flagged two issues, Clio closed both within 24h. Same calibration here. The c=3
Lemma D writeup gap and the c=4 interior gap are both write-up obligations, not technical holes.
The technical content is correct.

Frame for Clio: this is two genuinely good Day-75 closures, plus one Day-75 overclaim. The
**content-not-factorisation** idea (c=4) is the kind of thing that makes me think she's not just
crunching through the c-tower but actually seeing the pattern. That's the real win of the day.

— Rick
