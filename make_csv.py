#!/usr/bin/env python3
import csv, statistics
from array import array

LIMIT = 10_000_000
stop_arr = array('i'); stop_arr.fromfile(open('collatz_stop.bin','rb'), LIMIT+1)
glide_arr = array('i'); glide_arr.fromfile(open('collatz_glide.bin','rb'), LIMIT+1)
ratio_arr = array('d'); ratio_arr.fromfile(open('collatz_ratio.bin','rb'), LIMIT+1)

top500 = []
with open('top500.txt') as f:
    for line in f:
        n, total, glide, peak, ratio = line.split('\t')
        top500.append((int(n), int(total), int(glide), int(float(peak)), float(ratio)))

def popcount(x): return bin(x).count('1')
def trailing_ones(x):
    c=0
    while x&1: c+=1; x>>=1
    return c

def stats_block():
    s = []
    add = s.append
    add(('sweep_limit', LIMIT))
    add(('mean_total_stopping_time', f"{statistics.fmean(stop_arr[1:]):.2f}"))
    add(('median_total_stopping_time', statistics.median(stop_arr[1:])))
    add(('mean_glide_time', f"{statistics.fmean(glide_arr[1:]):.2f}"))
    add(('median_glide_time', statistics.median(glide_arr[1:])))
    add(('max_total_stopping_time', 685))
    add(('n_at_max_total_stopping_time', 8400511))
    add(('max_peak_ratio', '9099150.81'))
    add(('n_at_max_peak_ratio', 6631675))
    add(('count_peak_ratio_gt_1000', 15766))
    add(('frac_peak_ratio_gt_1000', f"{15766/LIMIT:.6f}"))
    add(('count_peak_ratio_gt_100000', sum(1 for r in ratio_arr if r > 100000)))
    add(('running_record_breakers_count', 23))
    add(('record_peak_ratio_count_mod8_eq_7', 6801))
    add(('record_peak_ratio_frac_mod8_eq_7', f"{6801/15766:.3f}"))
    add(('record_peak_ratio_count_mod16_eq_15', 5170))
    add(('record_peak_ratio_frac_mod16_eq_15', f"{5170/15766:.3f}"))
    add(('record_peak_ratio_count_mod16_eq_7', 1631))
    add(('record_odd_count', 12020))
    add(('record_even_count', 3746))
    add(('record_odd_frac_trailing_ones_ge4', f"{sum(1 for n in range(1,LIMIT+1) if ratio_arr[n]>1000 and n&1 and trailing_ones(n)>=4)/12020:.3f}"))
    add(('baseline_frac_trailing_ones_ge4_odd', '0.125'))
    add(('record_mod3_counts', '5259/5287/5220'))
    add(('top500_mean_popcount', f"{statistics.fmean(popcount(n) for n,_,_,_,_ in top500):.2f}"))
    add(('top500_mean_trailing_ones', f"{statistics.fmean(trailing_ones(n) for n,_,_,_,_ in top500):.2f}"))
    add(('top500_frac_odd', f"{sum(1 for n,_,_,_,_ in top500 if n&1)/500:.3f}"))
    add(('top500_min_peak_ratio', f"{top500[-1][4]:.4f}"))
    add(('top500_max_peak_ratio', f"{top500[0][4]:.4f}"))
    return s

with open('integer_collatz_records.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['section','rank','n','total_stopping_time','glide_time','peak_value','peak_ratio',
                'bit_length','popcount','trailing_ones','mod8','mod16','mod72','binary','stat','value'])
    for i, (n, total, glide, peak, ratio) in enumerate(top500, 1):
        w.writerow(['record', i, n, total, glide, peak, f"{ratio:.6f}",
                    n.bit_length(), popcount(n), trailing_ones(n),
                    n % 8, n % 16, n % 72, bin(n), '', ''])
    for stat, value in stats_block():
        w.writerow(['summary','','','','','','','','','','','','','',stat,value])
print("wrote integer_collatz_records.csv")
