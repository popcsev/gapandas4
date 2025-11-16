"""
Advanced Filtering Examples (v0.6.0 - Simplified Syntax!)

This example demonstrates filtering with the NEW simplified query_report() function.
Uses plain strings for dimensions and metrics - much cleaner than the old syntax!
"""

import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'

# Example 1: Simple dimension filter
# Get data only for United States
print("Example 1: Filter by country (US only)")
us_filter = gp.dimension_filter("country", "==", "United States")

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'city'],  # Simple strings!
    metrics=['activeUsers'],  # Simple strings!
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=us_filter
)

print(df.head())
print()

# Example 2: Simple metric filter
# Get only high-traffic cities (>1000 active users)
print("Example 2: Filter by metric (activeUsers > 1000)")
high_traffic_filter = gp.metric_filter("activeUsers", ">", 1000)

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['city'],  # Simple strings!
    metrics=['activeUsers', 'sessions'],  # Simple strings!
    start_date='2024-01-01',
    end_date='2024-01-31',
    metric_filter=high_traffic_filter
)


# Example 3: Multiple countries using OR
# Get data for US, UK, and Canada
print("Example 3: Multiple countries using OR filter")
multi_country_filter = gp.or_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.dimension_filter("country", "==", "United Kingdom"),
    gp.dimension_filter("country", "==", "Canada"),
])

# Alternative: Using IN operator (simpler!)
# multi_country_filter = gp.dimension_filter("country", "in", ["United States", "United Kingdom", "Canada"])

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=multi_country_filter
)
print(df)
print()

# Example 4: Combining dimension and metric filters with AND
# Get US cities with >500 sessions
print("Example 4: Combine dimension and metric filters (US cities with >500 sessions)")
combined_filter = gp.and_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.metric_filter("sessions", ">", 500),
])

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['city'],
    metrics=['sessions', 'activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=combined_filter
)
print(df.head(10))
print()

# Example 5: Text pattern matching
# Get pages that start with "/blog/"
print("Example 5: Pattern matching (pages starting with /blog/)")
blog_filter = gp.dimension_filter("pagePath", "starts_with", "/blog/")

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['pagePath'],
    metrics=['screenPageViews'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=blog_filter
)
print(df.head(10))
print()

# Example 6: Regex filtering
# Get pages matching a pattern (e.g., /product/[0-9]+)
print("Example 6: Regex filtering (product pages)")
product_filter = gp.dimension_filter("pagePath", "regex", "^/product/[0-9]+$")

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['pagePath'],
    metrics=['screenPageViews'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=product_filter
)
print(df.head())
print()

# Example 7: Range filtering (between)
# Get data for cities with sessions between 100 and 500
print("Example 7: Range filtering (sessions between 100 and 500)")
range_filter = gp.metric_filter("sessions", "between", [100, 500])

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['city'],
    metrics=['sessions', 'activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    metric_filter=range_filter
)
print(df.head())
print()

# Example 8: Complex nested filters
# (US cities with >1000 sessions) OR (UK cities with >500 sessions)
print("Example 8: Complex nested filters")
us_high_traffic = gp.and_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.metric_filter("sessions", ">", 1000),
])

uk_medium_traffic = gp.and_filter([
    gp.dimension_filter("country", "==", "United Kingdom"),
    gp.metric_filter("sessions", ">", 500),
])

complex_filter = gp.or_filter([us_high_traffic, uk_medium_traffic])

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'city'],
    metrics=['sessions', 'activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=complex_filter
)
print(df.head(20))
print()

# Example 9: Excluding data with NOT
# Get all countries except United States
print("Example 9: Excluding data (all countries except US)")
not_us_filter = gp.not_filter(
    gp.dimension_filter("country", "==", "United States")
)

# Alternative: Using != operator (simpler!)
# not_us_filter = gp.dimension_filter("country", "!=", "United States")

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=not_us_filter
)
print(df.head(10))
print()

# Example 10: Using FilterBuilder class directly
# For more explicit code or when building filters programmatically
print("Example 10: Using FilterBuilder class")
filter_obj = gp.FilterBuilder.dimension_filter("browser", "in", ["Chrome", "Firefox", "Safari"])

df = gp.query_report(
    service_account=service_account,
    property_id=property_id,
    dimensions=['browser'],
    metrics=['activeUsers'],
    start_date='2024-01-01',
    end_date='2024-01-31',
    dimension_filter=filter_obj
)
print(df)
