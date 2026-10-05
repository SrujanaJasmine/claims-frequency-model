import duckdb

con = duckdb.connect("data/claims.duckdb", read_only=True)

def run(title, sql):
    print(f"\n=== {title} ===")
    print(con.execute(sql).df().to_string(index=False))

run("1. Row count vs unique policy IDs", """
    SELECT COUNT(*) AS rows, COUNT(DISTINCT IDpol) AS unique_ids FROM raw_freq
""")

run("2. Missing values per column", """
    SELECT
      SUM((ClaimNb IS NULL)::INT)   AS claimnb_null,
      SUM((Exposure IS NULL)::INT)  AS exposure_null,
      SUM((DrivAge IS NULL)::INT)   AS drivage_null,
      SUM((VehAge IS NULL)::INT)    AS vehage_null,
      SUM((Area IS NULL)::INT)      AS area_null,
      SUM((Region IS NULL)::INT)    AS region_null
    FROM raw_freq
""")

run("3. Numeric ranges", """
    SELECT MIN(Exposure) min_exp, MAX(Exposure) max_exp,
           MIN(DrivAge) min_driv, MAX(DrivAge) max_driv,
           MIN(VehAge) min_veh, MAX(VehAge) max_veh,
           MIN(BonusMalus) min_bm, MAX(BonusMalus) max_bm,
           MAX(ClaimNb) max_claims
    FROM raw_freq
""")

run("4. Policies with Exposure > 1 (impossible for a 1-year window)", """
    SELECT COUNT(*) AS n_exposure_gt_1 FROM raw_freq WHERE Exposure > 1
""")

run("5. Claim count distribution", """
    SELECT ClaimNb, COUNT(*) AS policies,
           ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 3) AS pct
    FROM raw_freq GROUP BY ClaimNb ORDER BY ClaimNb
""")

run("6. Tiny exposure with claims (inflates claims/exposure)", """
    SELECT COUNT(*) AS n FROM raw_freq WHERE Exposure < 0.02 AND ClaimNb > 0
""")

run("7. Frequency vs severity consistency", """
    WITH s AS (SELECT IDpol, COUNT(*) AS n_sev FROM raw_sev GROUP BY IDpol)
    SELECT
      CASE
        WHEN f.ClaimNb > 0 AND s.n_sev IS NULL THEN 'claims in freq, none in sev'
        WHEN f.ClaimNb = 0 AND s.n_sev IS NOT NULL THEN 'no claims in freq, rows in sev'
        WHEN f.ClaimNb <> s.n_sev THEN 'count mismatch'
        ELSE 'consistent'
      END AS status,
      COUNT(*) AS policies
    FROM raw_freq f LEFT JOIN s USING (IDpol)
    GROUP BY 1 ORDER BY 2 DESC
""")

run("8. Severity rows whose policy is missing from freq (orphans)", """
    SELECT COUNT(*) AS orphans FROM raw_sev
    WHERE IDpol NOT IN (SELECT IDpol FROM raw_freq)
""")

run("9. Claim amount distribution", """
    SELECT COUNT(*) n, MIN(ClaimAmount) mn,
           QUANTILE_CONT(ClaimAmount, 0.5) median,
           QUANTILE_CONT(ClaimAmount, 0.99) p99,
           MAX(ClaimAmount) mx
    FROM raw_sev
""")