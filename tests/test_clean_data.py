import duckdb
import pytest

DB = "data/claims.duckdb"

@pytest.fixture(scope="module")
def con():
    c = duckdb.connect(DB, read_only=True)
    yield c
    c.close()

def test_no_duplicate_policies(con):
    n, u = con.execute("SELECT COUNT(*), COUNT(DISTINCT IDpol) FROM policies_clean").fetchone()
    assert n == u

def test_exposure_in_valid_range(con):
    lo, hi = con.execute("SELECT MIN(Exposure), MAX(Exposure) FROM policies_clean").fetchone()
    assert lo > 0 and hi <= 1.0

def test_claims_capped(con):
    assert con.execute("SELECT MAX(ClaimNb) FROM policies_clean").fetchone()[0] <= 4

def test_no_missing_key_features(con):
    nulls = con.execute("""
        SELECT SUM((DrivAge IS NULL)::INT + (VehAge IS NULL)::INT + (Exposure IS NULL)::INT)
        FROM policies_clean
    """).fetchone()[0]
    assert nulls == 0