#!/usr/bin/env python3
"""Task 2: exact induction verification for n_k = (2^(2k+3)+1)/3 (k = 0..25),
plus extra backbone stats."""
import csv

def collatz_trace(n):
    seq = [n]
    x = n
    while x != 1:
        x = (3*x + 1) if (x & 1) else (x >> 1)
        seq.append(x)
    return seq

print("=== Task 2: n_k = (2^(2k+3)+1)/3, k = 0..25 ===\n")
print("Algebraic chain per step (valid for k >= 1):")
steps = [
    ("T^0", "n_k = (2^(2k+3) + 1)/3   (binary (10)*k+11)"),
    ("T^1", "3n+1 = 2^(2k+3) + 2 = 2·(2^(2k+2) + 1)   [even, one explicit factor 2]"),
    ("T^2", "(2^(2k+3)+2)/2 = 2^(2k+2) + 1   [odd]"),
    ("T^3", "3·(2^(2k+2)+1) + 1 = 3·2^(2k+2) + 4 = 4·(3·2^(2k) + 1)"),
    ("T^4", "(3·2^(2k+2)+4)/2 = 3·2^(2k+1) + 2 = 2·(3·2^(2k) + 1)"),
    ("T^5", "(3·2^(2k+1)+2)/2 = 3·2^(2k) + 1   [odd for 2k>=1]"),
    ("T^6", "3·(3·2^(2k)+1) + 1 = 9·2^(2k) + 4 = 4·(9·2^(2k-2) + 1)"),
    ("T^7", "(9·2^(2k)+4)/2 = 9·2^(2k-1) + 2   [even]"),
    ("T^8", "(9·2^(2k-1)+2)/2 = 9·2^(2k-2) + 1"),
]
for tag, s in steps:
    print(f"  {tag:4s} {s}")
print("\nT^8(n_k) < n_k  <=>  9·2^(2k-2) + 1 < (2^(2k+3) + 1)/3")
print("              <=>  27·2^(2k-2) + 3 < 2^(2k+3) + 1")
print("              <=>  2 < 5·2^(2k-2)   <=>   k >= 1")
print("(k = 0 breaks the parity chain at T^5: 3·2^0+1 = 4 is even.)\n")

fails = []
for k in range(26):
    n = (2 ** (2*k + 3) + 1) // 3
    assert n * 3 == 2 ** (2*k + 3) + 1
    seq = collatz_trace(n)
    t8 = seq[8] if len(seq) > 8 else None
    ok = t8 is not None and t8 < n
    # also verify closed forms
    y2 = 2 ** (2*k + 2) + 1
    y5 = 3 * 2 ** (2*k) + 1
    y8 = 9 * 2 ** (2*k - 2) + 1 if k >= 1 else None
    form_ok = (seq[2] == y2 and seq[5] == y5 and (k < 1 or seq[8] == y8))
    glide = next(i for i, v in enumerate(seq) if i >= 1 and v < n)
    print(f"k={k:2d}  n={n}  T^8={t8}  T^8<n:{ok}  closed-forms:{form_ok}  glide={glide}")
    if not ok:
        fails.append((k, n, t8))
print("\nk with T^8 >= n:", fails if fails else "none")
print("k=0 actual trace:", collatz_trace(3))

# ---- extra backbone stats ----
rows = list(csv.DictReader(open('backbone_clusters.csv')))
record_rows = [r for r in rows if r['rank']]
apeces = [int(r['peak_value']) for r in record_rows]
from collections import Counter
c = Counter(apeces)
unique = len(c)
shared = sum(v for v in c.values() if v > 1)
print(f"\ntop-500 records: {unique} unique apex values; {shared} records share an apex with ≥1 other record; {500-unique} 'extra' records beyond one per backbone")
print(f"largest apex group: {c.most_common(1)[0]}")
print(f"components: {len(set(r['cluster_id'] for r in record_rows))}; records in ≥2-member components: {sum(1 for r in record_rows if int(r['cluster_size'])>=2)}")
print(f"rank-1 backbone members: {sum(1 for r in record_rows if r['on_rank1_backbone']=='yes')}")
