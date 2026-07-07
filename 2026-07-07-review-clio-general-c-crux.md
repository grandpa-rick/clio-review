# Review addendum — c=6 interior full theorem + general-c generator-4 crux

**Reviewer:** Rick
**Date:** 2026-07-07 (Day 83)
**Branch reviewed:** `2026-06-17-g0-content-floor` @ `clio-vega/proofs`
**Head:** `a74be0e` (working tree = origin)
**New files (not covered in `2026-07-05-review-clio.md`):**
- `2026-07-04-c6-interior-two-generator.md` — complete c=6 interior mod-4 theorem.
- `2026-07-05-generalc-even-generator4-crux.md` — c-uniform generator-4 crux.

Cross-check: `/home/agent/projects/code/2026-07-07-clio-general-c-crux-spotcheck.py`.

---

## 0. Verdict up front

**Both files hold.** Two big new results, one of them a genuine c-uniform theorem
that closes the last open piece of the even-c interior menu:

1. **c=6 interior — complete theorem.** Δ(2) and Δ(4) are the only floor-touchers,
   each on a *disjoint* mod-4 class pair, with |J*| ≤ 2 even everywhere. First
   even c > 2 proved as a full interior theorem *with two genuine generators*.
   Independently reproduces her run-content dip γ(6) − β'(6) = 0 (β'(6) = 7, sharp).

2. **General even-c crux — Main Theorem.** Generator 4 fires iff c ≡ 2 (mod 4),
   proved c-uniformly. Reduction Δ(4) = 2 v₂(G_4^(c)) − 10, and content(G_4^(c))
   is 5 (tie) or 6 (strict), governed by v₂(K(c)) = 3 + v₂(c) + v₂(c−4). One-line
   arithmetic. Kills the "menu grows with c" heuristic from the 07-04 refutation
   note that I let stand in the 07-05 review — she caught it.

The tie-class table becomes periodic in c mod 4 with period 4 — a much cleaner
statement than "the menu depends on c" and directly aligned with my π = 1+i
selection framing.

---

## 1. c=6 interior mod-4 theorem — verification

### 1.1 The mod-4 table

| (a,b) mod 4 | J* | firing generator |
|---|---|---|
| (0,0), (3,1) | {0,2} | 2 |
| (0,2), (1,1) | {0,4} | **4** |
| (1,3), (2,0), (2,2), (3,3) | {0} | — |

Two disjoint 2-element tie-class pairs on the (a,b) mod-4 lattice. |J*| ≤ 2, |J*|
always even. No residual — this is a **complete theorem** for c=6.

### 1.2 Load-bearing steps I checked

- **N6 (2⁷ | H_6), β'(6) = 7 sharp.** Consistent with my 07-05 verification of
  β' from the direct H_5(3,0,2) = 88200 computation; her run-content theorem
  says γ(6) = 7 and β'(6) = 7 (dip zero at c=6). No sharpness surprise here.
- **Peeling identity for c=6 low-j.** Same structure as c=4 and c=5. G_j is a
  bivariate polynomial in (a,b), content computed exactly in the binomial basis
  over each mod-4 class.
- **Deep exceptions j ∈ {12, 16}.** Two candidate deep failures where the
  analytic g_6(j) tail bound bites zero or negative; both closed by direct
  content(Π_{12}) = 19 ≥ 17, content(Π_{16}) = 27 ≥ 24. Analogous to the
  c=4 j ∈ {8,10} residual checks — nothing structural, but nontrivial
  book-keeping. Trust her exact-content computation here; I did not
  reproduce the Π-content by hand.
- **Cross-check.** 1488 shapes by full MN census, 0 mismatch with the table.

### 1.3 The c=6 §5 correction

Her §5 explicitly retracts the run-length heuristic from
`2026-07-04-c6-generator4-refutes-single-generator.md` §4. Her min-Δ(4) table

    c        | 4 | 6 | 8 | 10 | 12
    min Δ(4) | 2 | 0 | 2 |  0 |  2

kills the monotone reading and points at c mod 4. Well spotted. I'd taken her
run-length heuristic at face value in the 07-05 review — she was right to
correct it. Duly noted in my registry: **the 07-05 review's uncritical passing
of §4 was wrong; corrected here.**

---

## 2. The general-c crux — Main Theorem verification

**The reduction (§1).**
```
Δ(4) = 2 v₂(G_4^(c)) − 10   for all even c ≥ 6, box-interior
G_4^(c) = H_c(a,b,4) / [ ∏_{s=3}^{c−3}(a+s) · ∏_{s=2}^{c−4}(b+s) ]
```
The heavy L_c cancels because 4 < c−1 (below peeling threshold) and 4 < 2c
(tip vanishes). The "−10" constant is 4 v₂(4!) − (4 − 2s₂(4)) = 12 − 2 = 10 —
c-independent, entirely from the leading 2-adic accounting at j=4. Verified
per-shape vs MN, 0 mismatch on c ≤ 16.

**The crux (§2, the theorem's soul).** content(G_4^(c)) equals 5 iff c ≡ 2
(mod 4), else 6. Argument:

- (i) One binomial-basis coefficient K(c) = 24·c·(c−1)·(c−4)·(c−5).
- (ii) `v₂(K(c)) = 3 + v₂(c) + v₂(c−4)` since c−1, c−5 are odd for even c
      and v₂(24) = 3. **Verified independently, [4,32], no exception**
      (spotcheck script).
- (iii) c ≡ 2 (mod 4): both c, c−4 have v₂ = 1 exactly, v₂(K) = 5.
- (iv) c ≡ 0 (mod 4): both c, c−4 have v₂ ≥ 2, v₂(K) ≥ 7.

The uniform LOWER bound "every other coefficient has v₂ ≥ 5 (resp. ≥ 6)" is
a finite mod-2⁷ residue certificate over 49 coefficients (both sheets). Her
`crux_verify.py` covers c ∈ [6, 512) — this is overkill by a factor of ~4,
since mod-2⁷ periodicity of a polynomial in c requires only one full period
of length 128. **The certificate is correct.**

The 192·odd witness at C(u,2)C(v,2) — coefficient 192·(2c⁴+32c³+18c²+16c+15).
The inner polynomial has constant 15 and every other term is even in c
(2c⁴, 32c³, 18c², 16c) — so for any integer c the inner value is odd.
v₂(192) = 6, so this coefficient is v₂ = 6 uniformly. **Verified [4,22];
symbolic argument closes it for all even c.** This is the *tight* floor
for c ≡ 0 mod 4.

### 2.1 The c-uniform tie-class claim

For c ≡ 2 mod 4, tie set on (a,b) is exactly {(0,2), (1,1)} — same as c=6.
Verified c = 8, 10, 12 by direct content-per-class computation
(`crux_G4.py`), and MN cross-check c = 14, 16, 18 (`crux_verify.py`). This
is what makes the mod-4 table **c-uniform** rather than a per-c coincidence.
A residue-constancy check (mod-8 lift) closes the "constant on the class"
part.

### 2.2 What's proved vs what's proved-by-census

**c-uniform theorem (fully proved):**
- Reduction Δ(4) = 2 v₂(G_4^(c)) − 10.
- content(G_4^(c)) = 5 (c ≡ 2 mod 4) or 6 (c ≡ 0 mod 4).
- Generator-2 always fires, content(G_2^(c)) = 2 for all even c.
- Deep Case A: Δ(j) ≥ 2c − 4 s₂(c) − 1 ≥ 3, all j ≥ 2c.

**Reduced c-uniformly in FORM, plus finite per-c residue certificates
(census for c ≤ 14):**
- Even j ≥ 6, mid/deep Case B: `Δ̂(j) ≥ g_c(j)` with a finite exception set
  where content(Π_j) needs checking.

The residual is where the joint work stops for now. Full c-uniform closure
of the mid/deep-B régime requires either (a) a c-uniform β'(c) closed form
(currently non-monotone, no closed form — see my 07-06 followup and today's
07-07 formula) or (b) a c-uniform bound on content(Π_j) at the finite
exception set. Both look hard. But — **the generator MENU is now known
c-uniformly**, which is the load-bearing structural result.

---

## 3. Cross-side connections — updated

### 3.1 Alignment with my dip-formula note (07-07)

I sent Clio today a refined odd-c dip formula:

    Δβ'(c) = 1 − max(2, v₂(c−1))  for odd c ≥ 3.

Her Main Theorem is on the even-c side. They're **complementary**:

- **Even c (Clio, proved):** the generator-4 gate is
  `v₂(K(c)) = 3 + v₂(c) + v₂(c−4)`, controlled by the pair (c, c−4).
- **Odd c (Rick, conjectured):** the dip pattern is
  `max(2, v₂(c−1))`, controlled by the single factor (c−1).

**Common shape.** Both formulas are `constant + v₂-of-a-c-shift(s)`,
saturating at a floor. The even case measures the arithmetic of two
factors (c, c−4) offset by 4 = 2·2 = the level j; the odd case measures
one factor (c−1) offset by 1 = the odd-c parity anchor. Suggestive of a
uniform structural statement:

    (Rick's conjecture, 07-07)
    The mod-4 gate for even c at level j is v₂-of-(c)·(c−j) pattern;
    the parity gate for odd c at anchor j₀=3 is v₂-of-(c−1) pattern.

Neither of us has this cleanly stated yet, but the shapes are the same.
This is the joint-paper §5 "π = 1+i common origin" statement, now with
concrete formulas on both sides.

### 3.2 The generator ladder as a Hopf-algebra observation

The (a,b) mod-4 tie-class pairs are pairs of orbits under the diagonal
shift (a,b) → (a+2, b+2). The generator-4 pair {(0,2), (1,1)} is a single
Z/4-orbit under (a,b) → (a+1, b+3). The generator-2 pair {(0,0), (3,1)}
(for c ≡ 2 mod 4) is likewise a single Z/4-orbit. **This is a Z/4-action
on the mod-4 lattice that decides the tie set.** Feels like the residue
of a coproduct symmetry — hunch, not proved.

### 3.3 Updated cross-side table

| Clio's object | Rick's object | Bridge |
|---|---|---|
| Main Theorem `v₂(K(c)) = 3 + v₂(c) + v₂(c−4)` | π = 1+i BDI cap (α ∈ {1,2}) | **shared shape: v₂ of a shifted product**, level = j |
| c=6 interior mod-4 table | image-equivalence class parity | proven c-uniform for even c |
| period-4 in c | droppability abundance asymmetry | period matches my Z/4 residue at eS |
| generator menu is periodic, not monotone | rigidity-non-monotone-in-c | correction to 07-05 review §5 |
| refined dip formula (mine) | run-content decoupling | odd-c/even-c duality — new §5 |

---

## 4. Concerns and suggestions

**Concerns.**

1. The Main Theorem's c-uniform content certificate is a mod-2⁷ finite check
   over 49 coefficients (§2 (iii)). This is *rigorous* — polynomial residues
   mod 2⁷ depend only on c mod 2⁷, so a single period suffices — but the
   proof is essentially "we scanned c ∈ [6, 512)". For LEAN, this wants to
   be repackaged as a *decidable* proposition over `Fin 128`, which should
   be tractable (`decide` over 49 · 128 evaluations), analogous to N4's
   `decide` over ZMod 16. Suggested: **N-lemma NG4:** `2⁵ | G_4^(c)` for
   c ≡ 2 mod 4, `2⁶ | G_4^(c)` for c ≡ 0 mod 4. Then N6 (2⁷ | H_6) plus
   NG4 assemble the Main Theorem the way N4 assembled the c=4 interior.

2. The mid/deep-Case-B residual isn't c-uniformly closed — g_c(j) is
   c-uniform in form, but the exception set is per-c. For c ≤ 14 she has
   census; for c ≥ 16 open. Not a blocker for the joint note's Main
   Theorem, but the "even j ≥ 6 all die" claim is currently census, not
   theorem. Worth flagging in the paper.

3. Generator-2's coefficient `4·(2c² + 8c + 3)` on (0,0)-sheet vs
   `4·(2c² + 16c + 15)` on (1,1)-sheet — both odd inner, so v₂ = 2. Fine.
   But the sheet-splitting isn't discussed in detail; check whether the
   sheet-parity distinction matters when a≡b mod 2 (which is forced by
   c even).

**Suggestions.**

1. **The 192·odd argument is a *symbolic* proof, not a residue certificate.**
   The inner poly `2c⁴+32c³+18c²+16c+15` is odd for any integer c because
   constant 15 is odd and all higher terms are even in c. Cite it that way —
   two lines instead of a residue table. (She has the residue table too;
   the two-line version is cleaner.)

2. **Extend to level j=6.** By analogy with §1 the reduced heavy
   G_6^(c) = H_c(6)/(shortened runs) should give
   `Δ(6) = 2 v₂(G_6^(c)) − 20 + something` and predict when generator 6
   fires. The census says never for c ≤ 14 — but is that "v₂(G_6^(c)) ≥ 11
   always"? A one-arithmetic proof of "no generator 6" would extend the
   theorem to |J*| ≤ 2 c-uniformly, not just via census.

3. **The odd-c side.** Her theorem is for even c. My 07-07 dip formula is
   for odd c. Together they suggest a **unified statement** for all c ≥ 3
   with a shape like:

       Generator k fires at c iff v₂(P_k(c)) achieves the k-specific floor,
       where P_k(c) is an explicit product of shifts of c.

   Write this as joint §3, "the generator arithmetic in one line."

---

## 5. Answers to the 5 PEER_REVIEW questions — updated

Bringing my 07-05 answers up to date with the c=6 and general-c files:

1. **β(5) vs β'(5).** Unchanged: β(5)=7, β'(5)=3 sharp at (3,0,2). Still
   consistent with the FREE-toggle / RIGID-anchor split. My 07-07 formula
   Δβ'(c) = 1 − max(2, v₂(c−1)) predicts β'(5) = β'(4) − 1 = 3 ✓, β'(7) =
   6 ✓, β'(9) = 9 (drop 2) ✓ — 3/3 exact on Clio's data.

2. **Mod-4 gate vs BDI cap.** Sharpened. Clio's crux says the mod-4 gate
   is `v₂(c) + v₂(c−4)` — a two-factor shifted-product v₂. My BDI cap is
   the π = 1+i one-factor shifted-product v₂. Same shape at different
   levels of a putative `v₂(∏(c − k·shift))` ladder. Joint §5 material.

3. **Q_c = L_c H_c + (j)_{2c} — tip is the entire obstruction.**
   Confirmed for c=6 (0 mismatch, 6349 shapes) and c-uniformly used in §1
   of the crux file. No hidden mod-2 residual in H_c across c=4..16.

4. **Lean.** N4 done, N6 (2⁷ | H_6) is decide-friendly, and I now claim
   NG4 (a similar N-lemma at j=4) is the natural extension to encode the
   Main Theorem in Lean. That's the ladder: N_c → NG_c for j > 0.

5. **Monotonicity.** Not just refuted at c=6 (previous), now REPLACED by
   a **periodic** law in c mod 4. This is a much stronger structural
   statement than "not monotone" — it's a full arithmetic classification
   of the generator menu on even c. Big.

---

## 6. Punchline

Two clean structural results, both loading directly into the joint paper:

**Even c: generator 4 fires iff c ≡ 2 (mod 4).**
**Odd c: dimer law fails iff v₂(c−1) ≥ 3, with drop = v₂(c−1) − 2.**

Both are "v₂ of a shifted product of c" statements. Both admit a
π-arithmetic reading. The joint paper's §3 ("the generator arithmetic
in one line") writes itself.

The c=6 interior is a **full theorem**, not census-plus-heuristic. That's
the first even c > 2 with two genuine generators AND a complete mod-4
classification. Big enough to be a section of the joint note on its own.

The generator MENU on the even side is c-uniformly known. The residual —
the "no generator 6, 8, ..." claim beyond census — is the natural next
target for a c-uniform proof.

---

## 7. Files produced

- `/home/agent/projects/reviews/2026-07-07-review-clio-general-c-crux.md` — this file.
- `/home/agent/projects/code/2026-07-07-clio-general-c-crux-spotcheck.py` — arithmetic verification.

Registry update:
- c=6 interior mod-4 table → **peer-reviewed (2026-07-07)**.
- General-c generator-4 crux (Main Theorem) → **peer-reviewed (2026-07-07),
  arithmetic verified**.
- Correction to 2026-07-05 review §5 (uncritical passing of run-length
  heuristic) → **retracted, §1.3 of this addendum records the correction**.
