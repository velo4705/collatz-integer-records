#!/usr/bin/env python3
"""Follow-up 1+2: trace top-500 peak-ratio records; induction for (10)*k+11."""
import csv, sys
from collections import Counter, defaultdict

def trailing_ones(x):
    c = 0
    while x & 1:
        c += 1
        x >>= 1
    return c

def trace(n):
    """Return (trajectory values list, max trailing ones at t>=1)."""
    vals = [n]
    x = n
    max_mid = 0
    t = 0
    while x != 1:
        x = (3 * x + 1) if (x & 1) else (x >> 1)
        t += 1
        vals.append(x)
        if (x & 1):
            to = trailing_ones(x)
            if to > max_mid:
                max_mid = to
    return vals, max_mid

records = []
with open('integer_collatz_records.csv') as f:
    for row in csv.DictReader(f):
        if row['section'] != 'record':
            continue
        records.append({'rank': int(row['rank']), 'n': int(row['n']),
                        'total_stopping_time': int(row['total_stopping_time']),
                        'glide_time': int(row['glide_time']),
                        'peak_value': int(row['peak_value']),
                        'peak_ratio': float(row['peak_ratio'])})
records.sort(key=lambda r: r['rank'])
print(f"loaded {len(records)} records")

# ---- Task 1a: mid-trajectory refueling for top 50 ----
print("\nrank  n          t0_to  max_mid_to  ratio        peak")
n_refuel_gt = 0
for r in records[:50]:
    vals, max_mid = trace(r['n'])
    r['max_mid_to'] = max_mid
    r['t0_to'] = trailing_ones(r['n']) if (r['n'] & 1) else 0
    assert max(vals) == r['peak_value'], (r['n'], max(vals), r['peak_value'])
    if max_mid > r['t0_to']:
        n_refuel_gt += 1
    print(f"{r['rank']:4d}  {r['n']:<10d} {r['t0_to']:5d}  {max_mid:10d}  {r['peak_ratio']:<12.1f} {r['peak_value']}")

mid_track = {}
for r in records[50:]:
    vals, max_mid = trace(r['n'])
    r['max_mid_to'] = max_mid
    r['t0_to'] = trailing_ones(r['n']) if (r['n'] & 1) else 0
    assert max(vals) == r['peak_value']
top50 = records[:50]
print(f"\ntop-50: records where max mid-trajectory trailing-ones ({sum(1 for r in top50 if r['max_mid_to']>r['t0_to'])}) exceeds t0; "
      f"aggregate: t0 max={max(r['t0_to'] for r in top50)}, mid max={max(r['max_mid_to'] for r in top50)}")
all500 = records
print(f"top-500: mean t0 trailing-ones={sum(r['t0_to'] for r in all500)/500:.2f}, "
      f"mean max mid={sum(r['max_mid_to'] for r in all500)/500:.2f}, "
      f"records with mid>t0: {sum(1 for r in all500 if r['max_mid_to']>r['t0_to'])}/500")

# ---- Task 1b: backbone clustering via shared high-altitude values ----
HI = 1_000_000_000  # 1e9
parent = list(range(len(records)))
def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i
def union(i, j):
    ri, rj = find(i), find(j)
    if ri != rj:
        parent[ri] = rj

owner = {}
for idx, r in enumerate(records):
    vals, _ = trace(r['n'])
    seen = set()
    for v in vals:
        if v > HI and v not in seen:
            seen.add(v)
            if v in owner:
                union(idx, owner[v])
            else:
                owner[v] = idx
    r['hi_values'] = seen
clusters = defaultdict(list)
for idx in range(len(records)):
    clusters[find(idx)].append(idx)
cl_sizes = Counter(len(c) for c in clusters.values())
big = sorted(clusters.values(), key=len, reverse=True)
print("\ncluster size distribution (values > 1e9 shared):", dict(sorted(cl_sizes.items())))
for ci, comp in enumerate(big):
    if len(comp) >= 2:
        ns = sorted(records[i]['n'] for i in comp)
        print(f"cluster {ci}: size={len(comp)} members={ns}")
# cluster of the max-ratio record (6631675, rank 1)
top_cluster = None
for comp in big:
    if any(records[i]['rank'] == 1 for i in comp):
        top_cluster = comp
        break
print(f"\nrecords funneling into the rank-1 backbone (n=6631675): {len(top_cluster)}")
print("members:", sorted(records[i]['n'] for i in top_cluster))

# exact-peak apex groups
peak_counts = Counter(r['peak_value'] for r in records)
top_apex = peak_counts.most_common(8)
print("\nexact-apex groups (peak value, count):")
for apex, c in top_apex:
    print(f"  {apex}: {c} records")
apex63 = peak_counts[60342610919632]
print(f"records sharing apex 60342610919632: {apex63}")

# assign cluster ids stable by size rank
comp_list = sorted(clusters.values(), key=len, reverse=True)
comp_id = {}
for ci, comp in enumerate(comp_list):
    for i in comp:
        comp_id[i] = ci + 1
comp_size = Counter(comp_id.values())

with open('backbone_clusters.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','n','total_stopping_time','glide_time','peak_value','peak_ratio',
                't0_trailing_ones','max_mid_trajectory_trailing_ones','cluster_id','cluster_size',
                'on_rank1_backbone','shares_apex_60342610919632'])
    rank1_set = set(top_cluster)
    for i, r in enumerate(records):
        w.writerow([r['rank'], r['n'], r['total_stopping_time'], r['glide_time'],
                    r['peak_value'], f"{r['peak_ratio']:.6f}",
                    r['t0_to'], r['max_mid_to'],
                    comp_id[i], comp_size[comp_id[i]],
                    'yes' if i in rank1_set else 'no',
                    'yes' if r['peak_value'] == 60342610919632 else 'no'])
print("\nwrote backbone_clusters.csv")
