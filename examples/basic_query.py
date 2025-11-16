"""
Basic GAPandas4 Query Example

This example demonstrates the NEW simplified syntax (v0.6.0+) using strings
instead of Dimension/Metric objects.
"""

import gapandas4 as gp

# Set up credentials and property
service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'  # Replace with your GA4 property ID

# Execute a query with simplified syntax - just use strings!
df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'city'],  # Simple strings!
    metrics=['activeUsers', 'sessions'],  # Simple strings!
    start_date='2024-01-01',
    end_date='2024-01-31'
)

# Display results
print("Top 10 cities by active users:")
print(df.head(10))

# Basic data analysis
print(f"\nTotal active users: {df['activeUsers'].sum()}")
print(f"Total sessions: {df['sessions'].sum()}")
print(f"Average sessions per user: {df['sessions'].sum() / df['activeUsers'].sum():.2f}")

# ============================================================================
# OLD SYNTAX (still works if you need advanced features)
# ============================================================================
"""
# This is the old way - still works but more verbose:
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
df = gp.query(service_account, report_request)
"""
