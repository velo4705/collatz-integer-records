#!/usr/bin/env python3
"""Structural analysis of Collatz trajectories for 1 <= n <= N.

Metrics per integer:
  total stopping time  - steps to reach 1
  glide time           - first k>=1 with T^k(n) < n
  peak ratio           - max_value / n

STOP stores steps+1; -1 means unknown. PEAK stores absolute peak value
(0.0 = unknown). Intermediate path nodes are cached too.
"""
import sys
import time
import heapq
import array

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
CACHE_LIMIT = 1 << 24          # cache values < 16.7M
STOP = [-1] * CACHE_LIMIT
PEAK = [0.0] * CACHE_LIMIT
STOP[1] = 1   # 0 steps, known
PEAK[1] = 1.0

def collatz_metrics(n):
    x = n
    steps = 0
    glide = 0
    path = []
    while True:
        if x < CACHE_LIMIT and STOP[x] != -1:
            break
        y = (3 * x + 1) if (x & 1) else (x >> 1)
        steps += 1
        if glide == 0 and y < n:
            glide = steps
        path.append(x)
        x = y
    rem_stop = STOP[x] - 1   # steps from cached x to 1
    rem_peak = PEAK[x]
    for v in reversed(path):
        rem_stop += 1
        if v > rem_peak:
            rem_peak = v
        if v < CACHE_LIMIT and STOP[v] == -1:
            STOP[v] = rem_stop + 1
            PEAK[v] = float(rem_peak)
    total = rem_stop
    peak = rem_peak
    if glide == 0:
        if n == 1:
            glide = 0
        else:
            m = n
            g = 0
            while True:
                m = (3 * m + 1) if (m & 1) else (m >> 1)
                g += 1
                if m < n:
                    glide = g
                    break
    return total, glide, peak

def main():
    t0 = time.time()
    best_ratio = 0.0
    records = []
    max_stop = 0
    max_stop_n = 0
    max_peak = 0.0
    max_peak_n = 0
    count_ratio_1000 = 0
    glide_arr = [0] * (LIMIT + 1)
    stop_arr = [0] * (LIMIT + 1)
    ratio_arr = [0.0] * (LIMIT + 1)
    top500 = []  # min-heap of (ratio, n, total, glide, peak), size <= 500
    for n in range(1, LIMIT + 1):
        total, glide, peak = collatz_metrics(n)
        glide_arr[n] = glide
        stop_arr[n] = total
        ratio = peak / n
        ratio_arr[n] = ratio
        if total > max_stop:
            max_stop = total
            max_stop_n = n
        if ratio > max_peak:
            max_peak = ratio
            max_peak_n = n
        if ratio > 1000.0:
            count_ratio_1000 += 1
        if ratio > best_ratio:
            best_ratio = ratio
            records.append((n, total, glide, peak, ratio))
        if len(top500) < 500:
            heapq.heappush(top500, (ratio, n, total, glide, peak))
        elif ratio > top500[0][0]:
            heapq.heapreplace(top500, (ratio, n, total, glide, peak))
        if n % 1_000_000 == 0:
            print(f"n={n:,} elapsed={time.time()-t0:.1f}s records={len(records)}", flush=True)
    # Persist raw arrays for downstream analysis.
    array.array('i', stop_arr).tofile(open('collatz_stop.bin', 'wb'))
    array.array('i', glide_arr).tofile(open('collatz_glide.bin', 'wb'))
    array.array('d', ratio_arr).tofile(open('collatz_ratio.bin', 'wb'))
    top500_sorted = sorted(top500, key=lambda r: -r[0])
    with open('top500.txt', 'w') as f:
        for ratio, n, total, glide, peak in top500_sorted:
            f.write(f"{n}\t{total}\t{glide}\t{peak}\t{ratio}\n")
    with open('records.txt', 'w') as f:
        for n, total, glide, peak, ratio in records:
            f.write(f"{n}\t{total}\t{glide}\t{peak}\t{ratio}\n")
    print(f"done in {time.time()-t0:.1f}s")
    print(f"max total stopping time: {max_stop} at n={max_stop_n}")
    print(f"max peak ratio: {max_peak:.2f} at n={max_peak_n}")
    print(f"n with peak ratio > 1000: {count_ratio_1000}")
    print(f"record breakers: {len(records)}")

if __name__ == "__main__":
    main()
