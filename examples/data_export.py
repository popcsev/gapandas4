"""
Data Export Examples (v0.6.0 - Simplified Syntax!)

This example demonstrates exporting Google Analytics data to various formats
using the NEW simplified query_report() function.

NOTE: Batch requests still use BatchRunReportsRequest since we query multiple
date ranges at once. See simple_syntax.py for more simplified syntax examples.
"""

import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'

# Example 1: Query and export to CSV
print("Example 1: Export to CSV")
df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'city'],
    metrics=['activeUsers', 'sessions'],
    start_date='2024-01-01',
    end_date='2024-01-31'
)

# Export to CSV
gp.export_to_csv(df, 'analytics_january.csv')
print()

# Example 2: Export to Excel
print("Example 2: Export to Excel")
# Export same data to Excel
gp.export_to_excel(df, 'analytics_january.xlsx')
print()

# Example 3: Export to JSON
print("Example 3: Export to JSON")
# Export to JSON (records format - array of objects)
gp.export_to_json(df, 'analytics_january.json')

# Export to JSON (table format - includes schema)
gp.export_to_json(df, 'analytics_january_table.json', orient='table')
print()

# Example 4: Export multiple DataFrames to separate CSV files
print("Example 4: Batch export to CSV")
batch_request = gp.BatchRunReportsRequest(
    property=f"properties/{property_id}",
    requests=[
        gp.RunReportRequest(
            dimensions=[gp.Dimension(name="country")],
            metrics=[gp.Metric(name="activeUsers")],
            date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")]
        ),
        gp.RunReportRequest(
            dimensions=[gp.Dimension(name="country")],
            metrics=[gp.Metric(name="activeUsers")],
            date_ranges=[gp.DateRange(start_date="2024-02-01", end_date="2024-02-29")]
        ),
        gp.RunReportRequest(
            dimensions=[gp.Dimension(name="country")],
            metrics=[gp.Metric(name="activeUsers")],
            date_ranges=[gp.DateRange(start_date="2024-03-01", end_date="2024-03-31")]
        ),
    ]
)

dfs = gp.query(service_account, batch_request, report_type="batch_report")

# This will create analytics_batch_0.csv, analytics_batch_1.csv, analytics_batch_2.csv
gp.export_to_csv(dfs, 'analytics_batch.csv')
print()

# Example 5: Export multiple DataFrames to Excel with custom sheet names
print("Example 5: Multiple sheets in Excel")
gp.export_to_excel(
    dfs,
    'analytics_quarterly.xlsx',
    sheet_names=['January', 'February', 'March']
)
print()

# Example 6: Custom CSV export options
print("Example 6: Custom CSV export")
# Export with custom delimiter and including index
gp.export_to_csv(
    df,
    'analytics_custom.csv',
    sep=';',  # Use semicolon as delimiter
    index=True,  # Include row index
    header=['Country', 'City', 'Users', 'Sessions']  # Custom column names
)
print()

# Example 7: Filter and export
print("Example 7: Filter and export")
# Get only US data and export
us_filter = gp.dimension_filter("country", "==", "United States")

df_us = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['city'],
    metrics=['activeUsers', 'sessions'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=us_filter
)

gp.export_to_csv(df_us, 'analytics_us_cities.csv')
print()

print("All exports completed successfully!")
