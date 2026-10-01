---
title: DataFrame 101
description: Essential pandas DataFrame operations for inspecting, filtering, reshaping, and exporting extraction results.
#icon: material/table
keywords:
  - pandas
  - dataframe
  - filtering
  - groupby
  - merge
  - results
---

**The DataFrame is the "common currency" of this package.** Every extractor returns its
results as a pandas DataFrame (typically `results["results_df"]`), and entities are loaded
in from DataFrames too. Whatever you extract — vegetation indices, weather, crop detection,
disease risk — comes back as rows and columns you inspect, filter, reshape, and export with
the operations below. Learn these once and they apply across every extractor.



---
# DataFrame 101 — Quick Reference

A **Pandas DataFrame** is a two-dimensional, size-mutable, and potentially heterogeneous tabular data structure with labeled axes (rows and columns). It is the primary data structure used in the pandas library for data manipulation and analysis in Python.

Essential pandas DataFrame operations for working with extraction results are detailed in the following sections.



## Inspect

```python
df.shape                  # (rows, columns) tuple
df.columns.tolist()       # list of column names
df.dtypes                 # data type of each column
df.info()                 # columns, types, non-null counts, memory
df.head(10)               # first 10 rows
df.tail(5)                # last 5 rows
df.sample(5)              # 5 random rows
df.describe()             # stats for numeric columns (count, mean, std, min, max, quartiles)
```

---

## Row & Column Counts

```python
len(df)                   # number of rows
df.shape[0]               # number of rows (same)
df.shape[1]               # number of columns
df["col"].count()         # non-null count for one column
df.count()                # non-null count per column
```

---

## Column Operations

```python
# List columns
df.columns.tolist()

# Select one column (returns Series)
df["crop"]

# Select multiple columns (returns DataFrame)
df[["id", "date", "ndvi"]]

# Rename columns
df.rename(columns={"old_name": "new_name", "crop.id": "crop"})

# Add a new column
df["area_ha"] = df["area_sqm"] / 10000

# Drop columns
df.drop(columns=["unwanted_col", "another"])

# Reorder columns
df = df[["id", "date", "value", "crop"]]
```

---

## Unique Values

```python
df["crop"].unique()              # array of unique values
df["crop"].nunique()             # count of unique values
df["crop"].value_counts()        # count per unique value (sorted desc)

# Unique combinations of multiple columns
df[["crop", "year"]].drop_duplicates()
```

---

## Filter Rows

```python
# Single condition
df[df["crop"] == "CORN"]
df[df["ndvi"] > 0.5]
df[df["date"] >= "2025-01-01"]

# Multiple conditions (use & for AND, | for OR, wrap each in parentheses)
df[(df["crop"] == "CORN") & (df["ndvi"] > 0.5)]
df[(df["crop"] == "CORN") | (df["crop"] == "SOYBEAN")]

# Filter by list of values
df[df["crop"].isin(["CORN", "SOYBEAN", "WHEAT"])]

# Exclude values
df[~df["crop"].isin(["OTHERS"])]

# Filter nulls
df[df["ndvi"].isna()]        # rows where ndvi is NaN
df[df["ndvi"].notna()]       # rows where ndvi is not NaN

# String contains
df[df["name"].str.contains("North", na=False)]
```

---

## Sort

```python
df.sort_values("date")                          # ascending
df.sort_values("ndvi", ascending=False)         # descending
df.sort_values(["crop", "date"])                # multi-column sort
```

---

## Group & Aggregate

```python
# Count rows per group
df.groupby("crop").size()

# Aggregate one column
df.groupby("crop")["ndvi"].mean()

# Multiple aggregations
df.groupby("crop")["ndvi"].agg(["count", "mean", "std", "min", "max"])

# Multiple columns, multiple aggregations
df.groupby("crop").agg(
    ndvi_mean=("ndvi", "mean"),
    ndvi_count=("ndvi", "count"),
    temp_avg=("avg_temperature", "mean"),
)

# Group by multiple columns
df.groupby(["crop", "year"])["ndvi"].mean()
```

---

## Pivot & Crosstab

```python
# Pivot: one column per entity
df.pivot_table(index="date", columns="entity_id", values="ndvi")

# Crosstab: count occurrences
pd.crosstab(df["crop"], df["year"])

# Pivot with aggregation
df.pivot_table(index="crop", columns="year", values="ndvi", aggfunc="mean")
```

---

## Missing Data

```python
df.isna().sum()                   # null count per column
df.isna().sum().sum()             # total nulls in entire DataFrame
df.dropna()                       # drop rows with any null
df.dropna(subset=["ndvi"])        # drop rows where ndvi is null
df.fillna(0)                      # replace all nulls with 0
df["ndvi"].fillna(df["ndvi"].mean())  # fill with column mean
```

---

## Dates

```python
# Convert string to datetime
df["date"] = pd.to_datetime(df["date"])

# Extract components
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_of_year"] = df["date"].dt.dayofyear

# Filter by date range
df[(df["date"] >= "2025-01-01") & (df["date"] < "2025-07-01")]

# Date range shortcut
mask = df["date"].between("2025-01-01", "2025-06-30")
df[mask]
```

---

## Merge & Join

```python
# Merge two DataFrames on a shared column
merged = df1.merge(df2, on="id")                        # inner join (default)
merged = df1.merge(df2, on="id", how="left")            # keep all rows from df1
merged = df1.merge(df2, on=["id", "date"], how="outer") # keep all rows from both

# Concatenate DataFrames (stack vertically)
combined = pd.concat([df1, df2], ignore_index=True)

# Concatenate side by side
combined = pd.concat([df1, df2], axis=1)
```

---

## Export

```python
# CSV
df.to_csv("results/output.csv", index=False)

# CSV with specific separator
df.to_csv("results/output.tsv", sep="\t", index=False)

# Parquet (fast, compact, preserves types)
df.to_parquet("results/output.parquet", index=False)

# Excel
df.to_excel("results/output.xlsx", index=False, sheet_name="Results")

# Multiple sheets to one Excel file
with pd.ExcelWriter("results/output.xlsx") as writer:
    df_ndvi.to_excel(writer, sheet_name="NDVI", index=False)
    df_weather.to_excel(writer, sheet_name="Weather", index=False)
```

---

## Import

```python
# CSV
df = pd.read_csv("inputs/data.csv")

# CSV with options
df = pd.read_csv("inputs/data.csv", sep=";", encoding="utf-8", usecols=["id", "crop"])

# Parquet
df = pd.read_parquet("inputs/data.parquet")

# Excel
df = pd.read_excel("inputs/data.xlsx", sheet_name="Sheet1")

# GeoDataFrame (shp, gpkg, geojson) — use earthdaily.agriculture helper
from earthdaily.agriculture.core.geometry import load_geodataframe
gdf = load_geodataframe("inputs/fields.shp", verbose=True)
```

---

## Display Options

```python
# Show more rows/columns in notebook output
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 80)

# Reset to defaults
pd.reset_option("all")
```

---

## Common Patterns in Extraction Workflows

```python
# Get results from bulk extraction
results = extractor.process_entity_coverage_bulk_parallel(entity_list=entities, ...)
df = results["results_df"]

# Quick summary after extraction
print(f"Rows: {len(df)}, Columns: {df.shape[1]}")
print(f"Entities: {df['id'].nunique()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Nulls:\n{df.isna().sum()}")

# Per-entity row count
df.groupby("id").size().describe()

# Export clean results
df.drop(columns=["geometry"], errors="ignore").to_csv("results/clean_output.csv", index=False)
```
