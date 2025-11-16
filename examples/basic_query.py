"""
Basic GAPandas4 Query Example

This example demonstrates how to use the raw GA4 API with RunReportRequest.

NOTE: This shows the raw Google Analytics Data API syntax. For simpler queries,
check out simple_syntax.py and our helper functions (compare_date_ranges,
get_trending_content, etc.) which use simplified string syntax!
"""

import gapandas4 as gp

# Set up credentials and property
service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'  # Replace with your GA4 property ID

# Create a basic report request
report_request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        gp.Dimension(name="country"),
        gp.Dimension(name="city")
    ],
    metrics=[
        gp.Metric(name="activeUsers"),
        gp.Metric(name="sessions")
    ],
    date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")],
)

# Execute the query
df = gp.query(service_account, report_request)

# Display results
print("Top 10 cities by active users:")
print(df.head(10))

# Basic data analysis
print(f"\nTotal active users: {df['activeUsers'].sum()}")
print(f"Total sessions: {df['sessions'].sum()}")
print(f"Average sessions per user: {df['sessions'].sum() / df['activeUsers'].sum():.2f}")
