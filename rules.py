#!/usr/bin/env python3
"""Task 3: modular congruence rules forcing long upward streaks."""
import math
from array import array
from collatz_analysis import collatz_metrics

LIMIT = 10_000_000
glide_arr = array('i'); glide_arr.fromfile(open('collatz_glide.bin','rb'), LIMIT+1)
ratio_arr = array('d'); ratio_arr.fromfile(open('collatz_ratio.bin','rb'), LIMIT+1)
stop_arr = array('i'); stop_arr.fromfile(open('collatz_stop.bin','rb'), LIMIT+1)

def v2(x):
    c = 0
    while x and (x & 1) == 0:
        c += 1
        x >>= 1
    return c

def trailing_ones(x):
    c = 0
    while x & 1:
        c += 1
        x >>= 1
    return c

# 1) glide distribution per trailing-ones class (full sweep)
print("glide stats per v2(n+1) class (full 1..1e7):")
from collections import defaultdict
buckets = defaultdict(list)
for n in range(1, LIMIT+1, 1):
    if n & 1:  # odd only; glide meaningful everywhere but odd is the interesting case
        buckets[trailing_ones(n)].append(glide_arr[n])
for k in sorted(buckets):
    b = buckets[k]
    b2 = sorted(b)
    n_ = len(b2)
    print(f"  v2(n+1)={k:2d}: count={n_:7d} min={b2[0]} p25={b2[n_//4]} med={b2[n_//2]} p90={b2[int(n_*0.9)]} max={b2[-1]}")

# 2) Verify the algebraic rule: if v2(n+1)=k then k consecutive (3m+1)/2 ascents
#    with n_j ≡ -1 mod 2^{k-j}, all values increasing.
print("\nrule verification on samples with high v2(n+1):")
checked = 0
for n in range(3, 300000, 2):
    k = trailing_ones(n)
    if k < 5:
        continue
    m = n
    ok = True
    vals = [m]
    for j in range(k):
        if m & 1 == 0:
            ok = False; break
        m3 = (3 * m + 1) >> 1
        # after j+1 odd steps, value should ≡ -1 mod 2^{k-j-1}
        if (m3 + 1) % (1 << (k - j - 1)) != 0:
            ok = False; break
        m = m3
        vals.append(m)
    mult = vals[-1] / n
    print(f"  n={n} v2(n+1)={k}: rule_holds={ok} shortcut_ratio=(3/2)^{k}={(1.5)**k:.2f} actual={mult:.2f}")
    checked += 1
    if checked >= 8:
        break

# 3) Fraction of ratio>1000 records by trailing-ones class vs baseline
big1000 = [n for n in range(1, LIMIT+1) if ratio_arr[n] > 1000.0]
tally = defaultdict(int)
for n in big1000:
    if n & 1:
        tally[trailing_ones(n)] += 1
total_odd_records = sum(tally.values())
print(f"\nratio>1000 odd records={total_odd_records}; by trailing-ones class:")
odd_count = (LIMIT + 1) // 2
for k in sorted(tally):
    # baseline frequency of odd n with trailing-ones exactly k is 1/2^{k+1}
    base = odd_count / (1 << (k + 1))
    print(f"  k={k:2d}: records={tally[k]:5d}  baseline={base:9.1f}  enrichment={tally[k]/base:5.2f}x")

# 4) same for top records (ratio > 1e5)
top_rec = [n for n in range(1, LIMIT+1) if ratio_arr[n] > 100000.0]
tally = defaultdict(int)
for n in top_rec:
    if n & 1:
        tally[trailing_ones(n)] += 1
print(f"\nratio>1e5 odd records={len(top_rec)}; enrichment vs baseline:")
for k in sorted(tally):
    base = odd_count / (1 << (k + 1))
    print(f"  k={k:2d}: records={tally[k]:4d}  enrichment={tally[k]/base:6.2f}x")

# 5) even records: what are they? (glide==1 always for even n)
even_rec = [n for n in big1000 if n % 2 == 0]
print(f"\neven records (glide==1 but ratio>1000): {len(even_rec)}")
from collections import Counter
low = Counter(n & 0xff for n in even_rec)
print("most common low bytes:", low.most_common(8))
# check: even record = 2^j * (odd with many trailing ones)?
def strip_twos(n):
    j = 0
    while n & 1 == 0:
        n >>= 1; j += 1
    return j, n
tally2 = defaultdict(int)
for n in even_rec:
    j, m = strip_twos(n)
    tally2[(j, trailing_ones(m) if m & 1 else 0)] += 1
print("(v2 even prefix, trailing ones of odd part) counts:")
for key in sorted(tally2, key=lambda k: -tally2[k])[:12]:
    print(f"  {key}: {tally2[key]}")

# 6) mod 3 check within record set, and (n mod 72) for trailing-1-heavy classes
print("\nmod 3 for ratio>1000:", [sum(1 for n in big1000 if n%3==r) for r in range(3)])
