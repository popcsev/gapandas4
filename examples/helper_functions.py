"""
Helper Functions Examples

This example demonstrates convenient helper functions for common analytics tasks.
"""

import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'

# Example 1: Get trending content
print("Example 1: Get top 10 trending pages")
trending = gp.get_trending_content(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)

print("Top 10 pages by views:")
print(trending)
print()

# Example 2: Get trending content with filters
print("Example 2: Get trending blog posts only")
blog_filter = gp.dimension_filter("pagePath", "starts_with", "/blog/")

trending_blogs = gp.get_trending_content(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10,
    dimension_filter=blog_filter
)

print("Top blog posts:")
print(trending_blogs)
print()

# Example 3: Get traffic sources
print("Example 3: Get top traffic sources")
sources = gp.get_traffic_sources(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)

print("Top 10 traffic sources:")
print(sources)
print()

# Example 4: Analyze traffic sources
print("Example 4: Analyze conversion rates by source")
# Add conversion rate calculation
sources['conversion_rate'] = (
    sources['conversions'] / sources['sessions'] * 100
).round(2)

print("Sources by conversion rate:")
print(sources.sort_values(by='conversion_rate', ascending=False)[
    ['sessionSource', 'sessionMedium', 'sessions', 'conversions', 'conversion_rate']
].head())
print()

# Example 5: Get paid traffic sources only
print("Example 5: Get paid traffic sources")
paid_filter = gp.dimension_filter("sessionMedium", "in", ["cpc", "ppc", "paid"])

paid_sources = gp.get_traffic_sources(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10,
    dimension_filter=paid_filter
)

print("Top paid sources:")
print(paid_sources)
print()

# Example 6: Date range helpers
print("Example 6: Using date range helpers")

# Last 7 days
last_7_days = gp.format_date_range(7)
print(f"Last 7 days: {last_7_days[0]} to {last_7_days[1]}")

# Last 30 days
last_30_days = gp.format_date_range(30)
print(f"Last 30 days: {last_30_days[0]} to {last_30_days[1]}")

# Last 7 days ending yesterday
last_7_ending_yesterday = gp.format_date_range(7, 'yesterday')
print(f"Last 7 days (ending yesterday): {last_7_ending_yesterday[0]} to {last_7_ending_yesterday[1]}")

# Last 90 days ending on specific date
last_90_custom = gp.format_date_range(90, '2024-01-31')
print(f"Last 90 days ending Jan 31: {last_90_custom[0]} to {last_90_custom[1]}")
print()

# Example 7: Combining helpers with export
print("Example 7: Get trending content and export")
trending = gp.get_trending_content(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=50,
    metric='screenPageViews'
)

# Export to Excel for analysis
gp.export_to_excel(trending, 'trending_content_january.xlsx')
print("Exported trending content to Excel")
print()

# Example 8: Traffic source analysis with export
print("Example 8: Comprehensive traffic analysis")
# Get last 30 days of traffic
start, end = gp.format_date_range(30)

sources = gp.get_traffic_sources(
    service_account=service_account,
    property_id=property_id,
    start_date=start,
    end_date=end,
    limit=100
)

# Calculate additional metrics
sources['users_per_session'] = (
    sources['activeUsers'] / sources['sessions']
).round(2)

sources['conversions_per_user'] = (
    sources['conversions'] / sources['activeUsers']
).round(4)

# Export comprehensive analysis
gp.export_to_excel(sources, 'traffic_analysis_last_30_days.xlsx')
print("Exported traffic analysis to Excel")
print()

print("Helper function examples completed!")
