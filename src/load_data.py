import duckdb

DB = "data/claims.duckdb"

def main():
    con = duckdb.connect(DB)
    con.execute("""
        CREATE OR REPLACE TABLE raw_freq AS 
        SELECT * FROM read_csv_auto('data/raw/freMTPL2freq.csv', header = true),
    """)
    con.execute("""
        CREATE OR REPLACE TABLE raw_sev AS
        SELECT * FROM read_csv_auto('data/raw/freMTPL2sev.csv', header=true);
    """)
    for t in ["raw_freq", "raw_sev"]:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n:,} rows")
    print(con.execute("DESCRIBE raw_freq").df())
    con.close()

if __name__ == "__main__":
    main()