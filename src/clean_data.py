import duckdb

con = duckdb.connect("data/claims.duckdb")

con.execute("""
CREATE OR REPLACE TABLE policies_clean AS
WITH s AS (SELECT IDpol, COUNT(*) AS n_sev FROM raw_sev GROUP BY IDpol)
SELECT
    f.IDpol,
    LEAST(f.ClaimNb, 4)                AS ClaimNb,        -- cap rare extremes
    LEAST(f.Exposure, 1.0)             AS Exposure,       -- max 1 year
    f.Area,
    f.VehPower,
    LEAST(f.VehAge, 20)                AS VehAge,
    LEAST(f.DrivAge, 90)               AS DrivAge,
    f.BonusMalus,
    f.VehBrand,
    f.VehGas,
    f.Density,
    f.Region,
    (f.ClaimNb <> COALESCE(s.n_sev, 0)) AS flag_freq_sev_mismatch,
    (f.Exposure > 1)                    AS flag_exposure_capped,
    (f.ClaimNb > 4)                     AS flag_claims_capped
FROM raw_freq f
LEFT JOIN s USING (IDpol);
""")

print(con.execute("""
    SELECT COUNT(*) AS rows,
           SUM(flag_freq_sev_mismatch::INT) AS mismatches,
           SUM(flag_exposure_capped::INT)  AS exp_capped,
           SUM(flag_claims_capped::INT)    AS claims_capped,
           SUM(ClaimNb) / SUM(Exposure)    AS overall_frequency
    FROM policies_clean
""").df().to_string(index=False))
con.close()