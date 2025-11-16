"""
Simple Syntax Examples (NEW in v0.6.0!)

This example demonstrates the new simplified syntax for dimensions and metrics.
You can now use plain strings instead of Dimension() and Metric() objects!
"""

import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'YOUR_PROPERTY_ID'

print("=" * 70)
print("SIMPLE SYNTAX EXAMPLES - v0.6.0")
print("=" * 70)
print()

# ============================================================================
# Example 1: Before vs After - Basic Query
# ============================================================================
print("Example 1: Basic Query")
print("-" * 70)

# OLD SYNTAX (still works!)
print("OLD (v0.5.0 and earlier):")
print("""
request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        gp.Dimension(name="country"),
        gp.Dimension(name="city")
    ],
    metrics=[
        gp.Metric(name="activeUsers"),
        gp.Metric(name="sessions")
    ],
    date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")]
)
""")

# NEW SYNTAX - Much simpler!
print("\nNEW (v0.6.0+) - Using helper functions:")
print("""
# Helper functions now accept strings!
comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country', 'city'],  # Just strings!
    metrics=['activeUsers', 'sessions'],  # Just strings!
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)
""")
print()

# ============================================================================
# Example 2: Trending Content with Simple Syntax
# ============================================================================
print("Example 2: Get Trending Content")
print("-" * 70)
print("""
# Super simple - no more gp.Dimension() or gp.Metric()!
trending = gp.get_trending_content(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)
print(trending.head())
""")
print()

# ============================================================================
# Example 3: Traffic Sources with Simple Syntax
# ============================================================================
print("Example 3: Get Traffic Sources")
print("-" * 70)
print("""
sources = gp.get_traffic_sources(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)
print(sources.head())
""")
print()

# ============================================================================
# Example 4: Date Comparison with Simple Syntax
# ============================================================================
print("Example 4: Month-over-Month Comparison")
print("-" * 70)
print("""
# Notice how clean this looks - just pass strings!
comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],  # String list
    metrics=['activeUsers', 'sessions', 'conversions'],  # String list
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)

# Analyze results
print(comparison[['country',
                  'activeUsers_current',
                  'activeUsers_change_pct',
                  'sessions_current',
                  'sessions_change_pct']].head(10))
""")
print()

# ============================================================================
# Example 5: Advanced - Mixing Simple and Complex Syntax
# ============================================================================
print("Example 5: Mixing Simple Strings with Advanced Metrics")
print("-" * 70)
print("""
# You can STILL use advanced features when needed!
# Mix simple strings with Metric objects that have expressions

comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],  # Simple string
    metrics=[
        'activeUsers',  # Simple string
        'sessions',  # Simple string
        gp.Metric(  # Advanced metric with custom expression
            name='conversionRate',
            expression='conversions / sessions * 100'
        )
    ],
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)
""")
print()

# ============================================================================
# Example 6: Code Comparison - Lines Saved!
# ============================================================================
print("Example 6: How Much Code Do You Save?")
print("-" * 70)
print()
print("OLD (6 lines):")
print("""
dimensions=[
    gp.Dimension(name="country"),
    gp.Dimension(name="city"),
    gp.Dimension(name="region")
]
""")

print("NEW (1 line!):")
print("""
dimensions=['country', 'city', 'region']
""")
print()
print("✨ 83% LESS CODE! ✨")
print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Benefits of Simple Syntax (v0.6.0):
✅ 50-80% less code for common queries
✅ More readable and Pythonic
✅ Easier for beginners to learn
✅ Still supports advanced features (expressions, invisible metrics)
✅ 100% backward compatible - old syntax still works!

When to use which syntax:
📝 Use STRINGS for:      Most common cases
🔧 Use OBJECTS for:      Calculated metrics, invisible metrics, advanced features

All helper functions support both:
- compare_date_ranges()
- get_trending_content()
- get_traffic_sources()
""")
print("=" * 70)
