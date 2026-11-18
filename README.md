# collatz-integer-records

Empirical study of the integer Collatz map $T(n) = n/2$ (even), $3n+1$ (odd)
for $1 \le n \le 10{,}000{,}000$ — no claim about the full $3n+1$ conjecture.
Deliverables: a 500-row record table + LaTeX research note with exact
algebraic sub-family theorems.

## Key findings

- **Max total stopping time:** 685 at $n = 8{,}400{,}511$.
- **Max peak ratio:** 9,099,151× at $n = 6{,}631{,}675$ (peak 60,342,610,919,632).
- 15,766 integers (0.158%) exceed peak ratio 1000×; 57 exceed 100,000×.
- **2-adic fuel law** (proven): odd $n = 2^k q - 1$ with $k = v_2(n+1)$ forces
  $k$ shortcut ascents ($\varphi(m) = (3m+1)/2$), $\varphi^j(n) = 3^j 2^{k-j} q - 1$,
  so glide $\ge 2k+1$ and the orbit multiplies by $\sim (3/2)^k$. Record peaks
  roughly **double per trailing 1-bit**: enrichment vs the geometric baseline is
  1.7× ($k{=}4$) → 4.1× ($k{=}6$) → 8.7× ($k{=}8$) → 42.6× ($k{=}12$).
- **Mod structure is purely 2-adic:** 43.1% of records are $\equiv 7 \pmod 8$
  (vs 12.5%); mod 9 is flat, mod 3 is flat.
- **Alternating-bit quantization** (proven): $n_k = (2^{2k+3}+1)/3$
  (binary `10…1011`) has glide exactly $8$ for all $k \ge 1$; $k = 0$
  ($n_0 = 3$, glide 6) is the unique exception; peak ratio $\to 4.5$.
- **Mid-flight refueling:** 447/500 top records raise the trailing-ones fuel
  along the trajectory (mean 11.19 mid-flight vs 3.98 at $t=0$); the top 500
  coalesce onto **97 high-altitude backbones** above $10^9$; exactly 5 records
  funnel into the rank-1 backbone (apex 60,342,610,919,632).

## Structure

| File / dir | Contents |
|---|---|
| `collatz_analysis.py` | bitwise 10⁷ sweep (memoization, stopping time / glide / peak ratio) |
| `analyze.py`, `rules.py`, `induction.py`, `refueling_induction.py`, `make_csv.py` | follow-up analyses |
| `integer_collatz_records.csv` | top-500 record-breaking trajectories + summary statistics |
| `backbone_clusters.csv` | top-500 records clustered onto shared high-altitude backbones |
| `top500.txt`, `records.txt` | raw top-500 list / running record-breakers |
| `collatz_sweep_report.md` | analysis write-up (mod classes, families, fuel law) |
| `refueling_and_induction.md` | mid-flight refueling tables + induction verification |
| `collatz_integer_glide.tex` | Overleaf-ready research note (Theorem 1, Proposition 2, tables) |
| `collatz_stop.bin`, `collatz_glide.bin`, `collatz_ratio.bin` | **not committed** — regenerate with the sweep (see below) |

## Reproducing

```bash
python3 collatz_analysis.py 10000000   # ~20 s; writes .bin arrays + top500.txt + records.txt
python3 analyze.py                      # mod 8/16/72 analysis + family metrics
python3 rules.py                        # fuel-law verification, per-class glide stats, enrichment
python3 refueling_induction.py          # mid-flight refueling trace + backbone clustering
python3 induction.py                    # exact closed-form verification, k = 0..25
python3 make_csv.py                     # writes integer_collatz_records.csv
```

Requires only a recent Python 3 (no third-party packages; bitwise only).
`*.bin` dumps (~130 MB) are gitignored — regenerate them with the sweep, not in git.

## Citation / scope

Exact algebra applies only to the stated sub-families; enrichment figures are
finite-range ($n \le 10^7$, concentrated in 18–24-bit integers); the geometric
baseline is an empirical null model, not a theorem. The 3n+1 conjecture is
neither assumed nor approached. See `collatz_integer_glide.tex` for the full
note and `refueling_and_induction.md` / `collatz_sweep_report.md` for the
supporting tables.
