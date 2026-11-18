# Integer Collatz map, 1 ≤ n ≤ 10,000,000 — structural predictors

Sweep code: `collatz_analysis.py` (bitwise `n & 1` / `n >> 1` descent + memoized
stopping times / peaks cached for all visited values < 2^24; runs in ~20 s).
Arrays persisted to `collatz_stop.bin` / `collatz_glide.bin` / `collatz_ratio.bin`.
Deliverable table: `integer_collatz_records.csv` (500 record rows by peak ratio +
summary statistics section).

## Headline numbers
- Max total stopping time: **685** at n = 8,400,511.
- Max peak ratio: **9,099,151×** at n = 6,631,675 (peak 60,342,610,919,632).
- 15,766 integers (0.158%) have peak ratio > 1000; 57 have > 100,000.
- 23 running record-breakers overall. The top-5 records all exceed
  60,342,610,919,632 — they funnel through one shared high-peak trajectory.
- Mean / median total stopping time: 155.3 / 150. Mean glide 5.24 (median 1;
  half the integers are even, hence glide 1).

## Task 1 — binary & modulo structure of peak-ratio > 1000 records
- **43.1% of the 15,766 records are ≡ 7 (mod 8)** (6,801), vs 12.5% expected.
  Within mod 16, the enriched classes are **15** (5,170; 32.8% of all records)
  and **7** (1,631). Within mod 72, *all nine* classes ≡ 7 (mod 8)
  (7, 15, 23, …, 71) are enriched uniformly (727–779 each vs 219 expected) and
  every other class sits at baseline — i.e. the signal is purely 2-adic;
  **mod 9 contributes nothing** (mod 3 is uniform: 5,259 / 5,287 / 5,220).
- Odd records (12,020) by exact trailing-ones count k = v₂(n+1) vs the geometric
  distribution (each class half of the previous):

  | k | records | geom. expect. | enrichment |
  |---|---------|----------------|------------|
  | 1 | 2,908 | 6,010 | 0.48× |
  | 2 | 2,311 | 3,005 | 0.77× |
  | 3 | 1,631 | 1,503 | 1.09× |
  | 4 | 1,264 | 751 | 1.68× |
  | 5 | 974 | 376 | 2.59× |
  | 6 | 768 | 188 | 4.09× |
  | 7 | 557 | 94 | 5.93× |
  | 8 | 408 | 47 | 8.69× |
  | 9 | 314 | 24 | 13.4× |
  | 10 | 216 | 12 | 18.4× |
  | 11 | 174 | 6 | 29.7× |
  | 12 | 125 | 3 | 42.6× |
  | 13–23 | 91…1 | ≈1.5…0 | 62×–698× |

  43.0% of odd records have k ≥ 4 vs 12.5% geometric baseline; enrichment
  roughly **doubles per additional trailing one**. Even records (3,746, glide
  trivially 1) are mostly 2·m with m having ≥ 2 trailing ones (e.g. 565 ×
  ending 0b1110, 0b111100, …): after stripping factors of 2 the same odd-core
  mechanism drives the excursion.
- Top-500 (by peak ratio): bit length 18–24, mean popcount 13.6 (baseline
  8.15), mean trailing ones 3.98 (odd-number baseline 2.0), 85% odd.

## Task 2 — glide time across structured families
Computed directly with `collatz_metrics` (≤ 1e7):

- **Mersenne 2^k − 1** (all ones): glide 6, 11, 11, 91, 88, 24, 21, 29, 29, 94,
  83, 70, 70, 83, 78, **163**, 145, 91, 88, 104, 88, **223**; stopping time
  grows to 473; peak ratio climbs erratically but reaches **22,446×** at
  2^23−1 — overwhelmingly the richest structured family, exactly as the
  trailing-ones theory predicts.
- **Repunits R_k (base 10)**: glide 0, 8, 50, 8, 32, 11, 21 — no scaling law;
  moderate stopping times (14…165); peak ratios ≤ 84.
- **Alternating evens** 1010…10 (2^r·(...)): glide identically 1, peak ratio
  → 1.5, stopping time grows by 2 per bit.
- **Alternating odds** 1010…101: glide identically **3**, peak ratio → 3.0.
- **Alternating 1011-type** ((10)*k+11, i.e. 3, 11, 43, 171, 683, …): glide
  identically **8** for every member (a rigid invariant), stopping time
  erratic (14…169), peak ratios ≤ 54.

So Mersenne (all-ones) numbers supply extreme glide/peak; repunits do not;
alternating-bit families exhibit rigid quantized glide constants (1, 3, 8).

## Task 3 — congruence rules forcing long upward streaks
**Verified forcing rule.** If n is odd with k = v₂(n+1) trailing ones, write
n = 2^k·q − 1. Under the shortcut map φ(m) = (3m+1)/2, for every j ≤ k:

    φ^j(n) = 3^j·2^{k−j}·q − 1,  which is odd and ≡ −1 (mod 2^{k−j}).

Proof: induction, φ(3^j 2^{k−j} q − 1) = (3^{j+1}·2^{k−j} q − 2)/2
= 3^{j+1}·2^{k−j−1} q − 1. Each factor 2^{k−j}·q·3^j is even for j < k, so the
value is odd; φ is strictly increasing (φ(m) > m ⇔ m+1 > 0). Hence the first
2k Collatz steps are strictly increasing and multiply the value by
≈ (3/2)^k — **the first downward glide cannot occur before step 2k+1**. Across
all odd n ≤ 1e7, the minimum glide per class is 6, 8, 11, 13, 16, 19, 21, 24,
26, 29, … (≈ 2.3–2.7·k), comfortably above the forced bound; medians grow
≈ 5·k; and the record enrichment doubles per trailing one (table above).
The rule was verified computationally on samples (n = 31, 63, 95, 127, 159,
191, 223, 255 — all rule_holds = True, actual multiplier ≈ (3/2)^k).

**Corollaries / caveats.**
- Mersenne numbers n = 2^k − 1 are the q = 1 extremals: forced (3/2)^k ascent.
- The global maximum-ratio number 6,631,675 has only k = 2 trailing ones;
  trailing ones are a strong bias, not a necessary condition — a few high-peak
  trajectories route through rare high-value odd cores (top-5 records all
  exceed 6.03×10^13).
- No mod-3 / mod-9 (i.e. mod 72 beyond the 2-adic part) invariant plays any
  role; the divisibility structure is entirely 2-adic.
