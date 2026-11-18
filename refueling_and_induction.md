# Mid-flight refueling & the `(10)*k + 11` induction

Follow-up to `integer_collatz_records.csv` (top 500 by peak ratio, n ≤ 10^7).
No sweep re-run was performed; trajectories were re-traced from cached record
data (each trace shares its endpoint with the recorded peak, asserted).
Deliverable cluster table: `backbone_clusters.csv` (one row per record, with
t=0 vs mid-flight trailing-ones, cluster id/size, and backbone flags).

## Task 1a — mid-trajectory trailing ones vs at t = 0

`t0_to` = v₂(n+1) (number of trailing 1-bits) at the start (0 for even n).
`max_mid_to` = maximum v₂(m+1) over odd iterates T^t(n), t ≥ 1. For even n a
long upward streak happens later in the trajectory, so t0 = 0 says nothing
about the excursion.

**Summary over the top 50:** 46 of 50 have `max_mid_to` > `t0_to`. Top-50
aggregates: max t0 = 15, max mid = 18; mean t0 = 4.82 → mean max-mid = 11.14.
The four exceptions (mid ≤ t0): rank 10 (n=9158655, 14→13), rank 20
(n=8765439, 14→13), rank 43 (n=6646783, 10→9), rank 47 (n=1212415, 15→14) —
they start already optimally fueled and never refuel above that level.
**Across all 500: 447/500 refuel mid-trajectory;** mean t0 = 3.98 → mean
max-mid = **11.19**; highest mid-flight refuel observed is v₂(m+1) = 18
(ranks 19, 38, 45 — all on the 622717901620 backbone), versus 15 maximum at
t = 0.

Every one of the top 50 backbones passes through values with ≥ 7 trailing
ones en route to the apex, e.g. rank 1 (n = 6,631,675): t0 = 2 but reaches
v₂(m+1) = 13 mid-trajectory — the excursion is *earned* on the backbone, not
carried from the start. Detail rows:

| rank | n | t0 | max mid | peak ratio | apex |
|------|---|----|---------|------------|------|
| 1 | 6,631,675 | 2 | 13 | 9,099,151× | 60,342,610,919,632 |
| 2 | 7,460,635 | 2 | 13 | 8,088,133× | 60,342,610,919,632 |
| 3 | 8,393,215 | 9 | 13 | 7,189,451× | 60,342,610,919,632 |
| 4 | 8,842,233 | 1 | 13 | 6,824,363× | 60,342,610,919,632 |
| 5 | 9,947,513 | 1 | 13 | 6,066,100× | 60,342,610,919,632 |
| 6 | 7,553,535 | 9 | 12 | 1,262,345× | 9,535,170,024,016 |
| 7 | 7,202,815 | 11 | 14 | 934,016× | 6,727,544,495,440 |
| 8 | 6,416,623 | 4 | 9 | 748,057× | 4,799,996,945,368 |
| 9 | 9,603,753 | 1 | 14 | 700,512× | 6,727,544,495,440 |
| 10 | 9,158,655 | 14 | 13 | 599,121× | 5,487,141,897,520 |
| 19 | 3,041,127 | 3 | **18** | 204,766× | 622,717,901,620 |
| 30 | 9,275,958 | 0 | 9 | 142,174× | 1,318,802,294,932 |
| 47 | 1,212,415 | 15 | 14 | 115,181× | 139,646,736,808 |
| 50 | 7,747,070 | 0 | 9 | 110,823× | 858,555,169,576 |

## Task 1b — how many of the top 500 funnel into the same backbone

Clustering by values shared above 10^9 (all pairs merge before their common
apex; merging sets are identical thereafter). Each component shares one exact
apex value:

- **97 unique apex backbones** among the 500 records; **464/500** records
  share an apex with at least one other record (403 records beyond one per
  backbone).
- Exact-apex groups: 24,648,077,896 → **28 records**, 156,914,378,224 →
  **28 records**, 352,617,812,944 → 24, 90,239,155,648 → 23, 139,646,736,808 →
  20, 151,629,574,372 → 19, 294,475,592,320 → 19, 17,202,377,752 → 17.
- **Rank-1 backbone (apex 60,342,610,919,632): exactly 5 records** — ranks
  1–5 (n = 6,631,675, 7,460,635, 8,393,215, 8,842,233, 9,947,513). All would
  print `on_rank1_backbone=yes` in `backbone_clusters.csv`.
- Component-size distribution: {1: 36, 2: 12, 3: 12, 4: 5, 5: 4, 6: 4, 7: 1,
  8: 3, 9: 5, 10: 2, 11: 2, 12: 1, 16: 2, 17: 1, 19: 2, 20: 1, 23: 1, 24: 1,
  28: 2} — i.e. 36 singletons; the rest funnel into ≥ 2-record backbones.
  Note the cluster populates small niche integers (e.g. 270,271… provenance)
  and large 23–24-bit numbers equally; backbone membership is not a function
  of bit length.

## Task 2 — exact induction for n_k = (2^(2k+3) + 1)/3, k = 0…25

Binary: `n_k = 0b1010...1011` = (10)*k + 11. Algebraic chain (exact for k ≥ 1,
verified symbolically and numerically for k = 0…25, including n_k > 10^7 for
k ≥ 11):

| step | exact expression | parity |
|------|------------------|--------|
| T⁰ | n_k = (2^(2k+3) + 1)/3 | odd |
| T¹ | 3n+1 = 2^(2k+3) + 2 = 2·(2^(2k+2) + 1) | even |
| T² | (2^(2k+3)+2)/2 = 2^(2k+2) + 1 | odd |
| T³ | 3·(2^(2k+2)+1) + 1 = 3·2^(2k+2) + 4 = 4·(3·2^(2k) + 1) | even (v₂ = 2) |
| T⁴ | = 3·2^(2k+1) + 2 = 2·(3·2^(2k) + 1) | even (v₂ = 1) |
| T⁵ | = 3·2^(2k) + 1 | odd |
| T⁶ | 3·(3·2^(2k)+1) + 1 = 9·2^(2k) + 4 = 4·(9·2^(2k-2) + 1) | even (v₂ = 2) |
| T⁷ | = 9·2^(2k-1) + 2 | even |
| T⁸ | = 9·2^(2k-2) + 1 | — |

**Claim:** T⁸(n_k) < n_k ⟺ 9·2^(2k-2) + 1 < (2^(2k+3) + 1)/3 ⟺ 2 < 5·2^(2k-2) ⟺ **k ≥ 1**.

Verified numerically (exact big-int arithmetic) for every k = 1…25:
closed forms hold (T², T⁵, T⁸ match the expressions above) and T⁸ < n always;
glide = 8 identically (T¹…T⁷ > n, T⁸ < n — the excursion and glide are both
forced). k ≥ 11 members exceed the 10^7 sweep range but the verification is
algebraic and exact, so it applies identically. For completeness k = 25:
n = 3,002,399,751,580,331 → T⁸ = 2,533,274,790,395,905.

| k | n_k | T⁸ | T⁸<n | glide |
|-----|----|------------------------|------------------------|------|
| 0 | 3 | — | **False** | 6 |
| 1 | 11 | 10 | True | 8 |
| 2 | 43 | 37 | True | 8 |
| 3 | 171 | 145 | True | 8 |
| 4 | 683 | 577 | True | 8 |
| 5 | 2,731 | 2,305 | True | 8 |
| 6 | 10,923 | 9,217 | True | 8 |
| 7 | 43,691 | 36,865 | True | 8 |
| 8 | 174,763 | 147,457 | True | 8 |
| 9 | 699,051 | 589,825 | True | 8 |
| 10 | 2,796,203 | 2,359,297 | True | 8 |
| 11 | 11,184,811 | 9,437,185 | True | 8 |
| 12 | 44,739,243 | 37,748,737 | True | 8 |
| 13 | 178,956,971 | 150,994,945 | True | 8 |
| 14 | 715,827,883 | 603,979,777 | True | 8 |
| 15 | 2,863,311,531 | 2,415,919,105 | True | 8 |
| 16 | 11,453,246,123 | 9,663,676,417 | True | 8 |
| 17 | 45,812,984,491 | 38,654,705,665 | True | 8 |
| 18 | 183,251,937,963 | 154,618,822,657 | True | 8 |
| 19 | 733,007,751,851 | 618,475,290,625 | True | 8 |
| 20 | 2,932,031,007,403 | 2,473,901,162,497 | True | 8 |
| 21 | 11,728,124,029,611 | 9,895,604,649,985 | True | 8 |
| 22 | 46,912,496,118,443 | 39,582,418,599,937 | True | 8 |
| 23 | 187,649,984,473,771 | 158,329,674,399,745 | True | 8 |
| 24 | 750,599,937,895,083 | 633,318,697,598,977 | True | 8 |
| 25 | 3,002,399,751,580,331 | 2,533,274,790,395,905 | True | 8 |

**k = 0 is the lone exception**, not a failure of the algebra in spirit: the
parity chain breaks at T⁵ (3·2⁰ + 1 = 4 is even, so the half-chain splits),
the true trace is 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 (reaches the cycle in 7
steps), and T⁸(3) = T(1) = 4 > 3 with glide 6. The identity T⁸(n_k) < n_k
with glide exactly 8 holds for all k ≥ 1; k = 0 is absorbed by the trivial
3 → 1 cycle. Also note the family's global apex is the in-window T³ value:
peak ratio → 9/2 = 4.50 exactly for k ≥ 4 (verified k = 4…13, all 4.50; the
k = 3 outlier 53.99 re-peaks after the glide). So `(10)*k + 11` produces a
*rigid glide window* with a flat 4.50 peak-ratio ceiling, which is why these
members never appear in the peak-ratio top 500.
