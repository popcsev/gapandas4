"""
Data Comparison Examples

This example demonstrates how to compare metrics across different time periods.
"""

import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'

# Example 1: Compare current month vs previous month
print("Example 1: Month-over-month comparison")
comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers', 'sessions', 'conversions'],
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)

print(comparison.head(10))
print()

# Example 2: Year-over-year comparison
print("Example 2: Year-over-year comparison")
yoy_comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers', 'sessions'],
    current_start='2024-01-01',
    current_end='2024-01-31',
    previous_start='2023-01-01',
    previous_end='2023-01-31'
)

print(yoy_comparison.head(10))

# Find countries with the biggest growth
yoy_comparison_sorted = yoy_comparison.sort_values(
    by='activeUsers_change_pct',
    ascending=False
)
print("\nTop 5 countries by user growth:")
print(yoy_comparison_sorted[['country', 'activeUsers_current',
                              'activeUsers_previous',
                              'activeUsers_change_pct']].head())
print()

# Example 3: Week-over-week comparison with filters
print("Example 3: Week-over-week comparison with filters")
# Compare only mobile traffic
mobile_filter = gp.dimension_filter("deviceCategory", "==", "mobile")

wow_comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers', 'sessions'],
    current_start='2024-02-05',
    current_end='2024-02-11',
    previous_start='2024-01-29',
    previous_end='2024-02-04',
    dimension_filter=mobile_filter
)

print(wow_comparison.head())
print()

# Example 4: Export comparison to Excel
print("Example 4: Export comparison report")
gp.export_to_excel(comparison, 'month_over_month_comparison.xlsx')
print("Exported comparison to Excel")
print()

# Example 5: Compare specific metrics with advanced analysis
print("Example 5: Advanced comparison analysis")
# Compare multiple dimensions
detailed_comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'deviceCategory'],
    metrics=['activeUsers', 'sessions', 'engagementRate'],
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)

# Analyze the results
print("Countries with declining engagement:")
declining = detailed_comparison[
    detailed_comparison['engagementRate_change_pct'] < -10
].sort_values(by='engagementRate_change_pct')
print(declining[['country', 'deviceCategory', 'engagementRate_current',
                 'engagementRate_previous', 'engagementRate_change_pct']])
print()

# Example 6: Using format_date_range helper
print("Example 6: Using date range helpers")
# Compare last 7 days vs previous 7 days
start_current, end_current = gp.format_date_range(7, 'today')
start_previous, end_previous = gp.format_date_range(7, end_date=start_current)

print(f"Current period: {start_current} to {end_current}")
print(f"Previous period: {start_previous} to {end_previous}")

recent_comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers'],
    current_start=start_current,
    current_end=end_current,
    previous_start=start_previous,
    previous_end=end_previous
)

print(recent_comparison.head())
print()

print("Comparison examples completed!")
