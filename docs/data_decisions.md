# Data Quality Decisions

| # | Issue found | How many rows | Decision | Rationale |
|---|-------------|---------------|----------|-----------|
| 1 | Exposure > 1 | 1224 | Cap at 1.0, flag | A policy can't be observed for more than a year |
| 2 | ClaimNb > 4 | 9  | Cap at 4, flag | Very few policies, would dominate Poisson fit |
| 3 | Freq/severity mismatch | 1 | Keep rows, flag | Frequency model uses freq table; revisit for severity |
| 4 | Very short exposure | 0.003 | Keep, handled via offset | Poisson with log(exposure) offset handles this |
| 5 | Extreme VehAge / DrivAge | 100/100 | Cap, flag | Sparse tails give unstable estimates |