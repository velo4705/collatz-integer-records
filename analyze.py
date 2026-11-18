#!/usr/bin/env python3
"""Downstream structural analysis for the Collatz 1..1e7 sweep."""
import sys
import math
from array import array
from collatz_analysis import collatz_metrics

LIMIT = 10_000_000
stop_arr = array('i'); stop_arr.fromfile(open('collatz_stop.bin','rb'), LIMIT+1)
glide_arr = array('i'); glide_arr.fromfile(open('collatz_glide.bin','rb'), LIMIT+1)
ratio_arr = array('d'); ratio_arr.fromfile(open('collatz_ratio.bin','rb'), LIMIT+1)

top500 = []
with open('top500.txt') as f:
    for line in f:
        n, total, glide, peak, ratio = line.split('\t')
        top500.append((int(n), int(total), int(glide), int(float(peak)), float(ratio)))

big1000 = [n for n in range(1, LIMIT+1) if ratio_arr[n] > 1000.0]
print(f"total n: {LIMIT}, ratio>1000: {len(big1000)}")

def mod_table(ns, mod):
    t = [0]*mod
    for n in ns:
        t[n % mod] += 1
    return t

for mod in (8, 16, 72):
    t = mod_table(big1000, mod)
    exp = len(big1000)/mod
    print(f"\nmod {mod} (ratio>1000, expected {exp:.1f} per class):")
    for i, c in enumerate(t):
        mark = ' *' if c > 1.5*exp else ('  ' if c > exp else '')
        print(f"  {i:2d}: {c:5d}{mark}")

# binary features of top 500 vs baseline sample
def popcount(x): return bin(x).count('1')
def trailing_ones(x):
    c = 0
    while x & 1:
        c += 1
        x >>= 1
    return c

top_n = [r[0] for r in top500]
print("\nTop 500 by peak ratio:")
print("  bit length range:", min(n.bit_length() for n in top_n), "-", max(n.bit_length() for n in top_n))
import statistics
print(f"  mean popcount={statistics.mean(popcount(n) for n in top_n):.2f}, baseline(all<1e7)={statistics.mean(popcount(n) for n in range(1,100001)):.2f}")
print(f"  mean trailing-ones v2(n+1)={statistics.mean(trailing_ones(n) for n in top_n):.2f}, baseline(sample 1e5)={statistics.mean(trailing_ones(n) for n in range(1,100001)):.2f}")
print(f"  fraction odd: {sum(1 for n in top_n if n&1)/len(top_n):.3f}")

t72 = mod_table(top_n, 72)
print("\ntop-500 mod 72 histogram (nz only):")
for i, c in enumerate(t72):
    if c:
        print(f"  {i:2d}: {c}  (binary {bin(i)[2:]})")

# ---- Families ----
def fam_rows():
    rows = []
    # repunits base 10
    for k in range(1, 8):
        n = (10**k - 1)//9
        if 1 <= n <= LIMIT:
            rows.append(('repunit10', f'R_{k}', n))
    # Mersenne
    for k in range(2, 24):
        n = (1 << k) - 1
        if n <= LIMIT:
            rows.append(('mersenne', f'2^{k}-1', n))
    # alternating bit strings: '10'*k and '01'*k+'1' style, value <= LIMIT
    L = 1
    val1 = 0b1   # '1','101','10101',... odd alternating starting with 1
    while val1 <= LIMIT:
        val1 = (val1 << 2) | 0b101  # not exactly; build properly below
        break
    for k in range(1, 13):
        a = int('10'*k, 2)          # even alternating 1010...10
        b = int('10'*k + '1', 2)    # odd alternating 1010...101
        c = int('01'*k + '1', 2)    # 0101...01 = (4^k-1)/3
        for name, v in ((f'alt_10^{k}', a), (f'alt_101^{k}', b), (f'alt_01^{k}+1', c)):
            if 1 <= v <= LIMIT:
                rows.append(('alternating', name, v))
    return rows

print("\nFamily metrics:")
print(f"{'family':12s} {'member':12s} {'n':>10s} {'stop':>5s} {'glide':>6s} {'ratio':>12s}")
for fam, name, n in fam_rows():
    total, glide, peak = collatz_metrics(n)
    print(f"{fam:12s} {name:12s} {n:>10d} {total:>5d} {glide:>6d} {peak/n:>12.1f}")

# ---- Invariants / congruence tests ----
print("\nHeuristic rules among ratio>1000 set:")
def v2(x):
    c = 0
    while x and (x & 1) == 0:
        c += 1
        x >>= 1
    return c

# Rule A: long ascent correlates with many trailing 1s (n ≡ 2^k - 1 mod 2^k)
t1 = [trailing_ones(n) for n in big1000]
print(f"ratio>1000: mean trailing-ones={statistics.mean(t1):.2f}, max={max(t1)}")
print(f"ratio>1000: frac with trailing-ones>=4: {sum(1 for v in t1 if v>=4)/len(t1):.3f} (baseline P ~ 1/8 = 0.125)")

# Rule B: record peaks require odd n of form (2^{2k}-1)/3 etc. Check low-bit patterns
from collections import Counter
low8 = Counter(n & 0xff for n in big1000)
print("\nmost common n & 0xff among ratio>1000:")
for bits, c in low8.most_common(12):
    print(f"  {bits:3d} ({bits:#010b}): {c}")

# Rule C: n mod 3
t3 = [0,0,0]
for n in big1000:
    t3[n % 3] += 1
print(f"\nratio>1000 mod 3: {t3} (baseline ~{len(big1000)/3:.0f} each)")

# glide vs v2(n+1) correlation-ish check on sample
sample = range(1, LIMIT+1, 997)
gs = [(trailing_ones(n), glide_arr[n]) for n in sample]
byk = {}
for k, g in gs:
    byk.setdefault(k, []).append(g)
print("\nmean glide by trailing-ones count (sampled every 997):")
for k in sorted(byk):
    if len(byk[k]) > 20:
        print(f"  v2(n+1)={k}: mean glide={statistics.mean(byk[k]):.1f} (n={len(byk[k])})")
