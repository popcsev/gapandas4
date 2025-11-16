# GAPandas4
GAPandas4 is a Python package for querying the Google Analytics Data API for GA4 and displaying the results in a Pandas dataframe. It is the successor to the [GAPandas](https://practicaldatascience.co.uk/data-science/how-to-access-google-analytics-data-in-pandas-using-gapandas) package, which did the same thing for GA3 or Universal Analytics. GAPandas4 is a wrapper around the official Google Analytics Data API package and simplifies imports and queries, requiring far less code. 

### Before you start
In order to use GAPandas4 you will first need to [create a Google Service Account](https://practicaldatascience.co.uk/data-engineering/how-to-create-a-google-service-account-client-secrets-json-key) with access to the Google Analytics Data API and export a client secrets JSON keyfile to use for authentication. You'll also need to add the service account email address as a user on the Google Analytics 4 property you wish to access, and you'll need to note the property ID to use in your queries.  

### Installation
You can install GAPandas4 in two ways: via GitHub or via PyPi using the Pip Python package management system. 

```commandline
pip3 install git+https://github.com/practical-data-science/gapandas4.git
pip3 install gapandas4
```

### Usage examples
GAPandas4 has been written to allow you to use as little code as possible. Unlike the previous version of GAPandas for Universal Analytics, which used a payload based on a Python dictionary, GAPandas4 now uses a Protobuf (Protocol Buffer) payload as used in the API itself. 

#### Report
The `query()` function is used to send a protobug API payload to the API. The function supports various report types 
via the `report_type` argument. Standard reports are handled using `report_type="report"`, but this is also the 
default. Data are returned as a Pandas dataframe. 

```python
import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'xxxxxxxxx'

report_request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        gp.Dimension(name="country"),
        gp.Dimension(name="city")
    ],
    metrics=[
        gp.Metric(name="activeUsers")
    ],
    date_ranges=[gp.DateRange(start_date="2022-06-01", end_date="2022-06-01")],
)

df = gp.query(service_account, report_request, report_type="report")
print(df.head())
```

#### Filtering data (NEW in v0.5.0!)
GAPandas4 now includes powerful, easy-to-use filter helpers that make it simple to filter your GA4 data without dealing with complex protobuf structures.

##### Simple dimension filter
Filter data to show only specific dimension values:

```python
import gapandas4 as gp

# Get data only for United States
us_filter = gp.dimension_filter("country", "==", "United States")

request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[gp.Dimension(name="city")],
    metrics=[gp.Metric(name="activeUsers")],
    date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")],
    dimension_filter=us_filter,  # Apply the filter
)

df = gp.query(service_account, request)
```

**Supported dimension operators:**
- `==` or `equals` - Exact match
- `!=` or `not_equals` - Not equal
- `contains` - Contains substring
- `not_contains` - Does not contain
- `starts_with` or `begins_with` - Starts with string
- `ends_with` - Ends with string
- `in` - Value in list
- `not_in` - Value not in list
- `regex` or `matches_regex` - Regular expression match
- `is_null`, `is_empty` - Is null/empty
- `is_not_null`, `is_not_empty` - Is not null/empty

##### Simple metric filter
Filter data based on metric values:

```python
# Get only cities with more than 1000 active users
high_traffic = gp.metric_filter("activeUsers", ">", 1000)

request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[gp.Dimension(name="city")],
    metrics=[gp.Metric(name="activeUsers")],
    date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")],
    metric_filter=high_traffic,  # Apply the filter
)

df = gp.query(service_account, request)
```

**Supported metric operators:**
- `==` or `equals` - Equal to
- `!=` or `not_equals` - Not equal to
- `>` or `greater_than` - Greater than
- `>=` or `greater_than_or_equal` - Greater than or equal
- `<` or `less_than` - Less than
- `<=` or `less_than_or_equal` - Less than or equal
- `between` - Between two values (provide list: `[min, max]`)

##### Combining filters with AND
Combine multiple filters where all must be true:

```python
# US cities with more than 500 sessions
combined = gp.and_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.metric_filter("sessions", ">", 500)
])

request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[gp.Dimension(name="city")],
    metrics=[gp.Metric(name="sessions")],
    date_ranges=[gp.DateRange(start_date="2024-01-01", end_date="2024-01-31")],
    dimension_filter=combined,
)

df = gp.query(service_account, request)
```

##### Combining filters with OR
Combine filters where at least one must be true:

```python
# Data for US, UK, or Canada
multi_country = gp.or_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.dimension_filter("country", "==", "United Kingdom"),
    gp.dimension_filter("country", "==", "Canada")
])

# Or use the simpler 'in' operator:
multi_country = gp.dimension_filter("country", "in", ["United States", "United Kingdom", "Canada"])
```

##### Complex nested filters
Create sophisticated filter combinations:

```python
# (US cities with >1000 sessions) OR (UK cities with >500 sessions)
us_high = gp.and_filter([
    gp.dimension_filter("country", "==", "United States"),
    gp.metric_filter("sessions", ">", 1000)
])

uk_medium = gp.and_filter([
    gp.dimension_filter("country", "==", "United Kingdom"),
    gp.metric_filter("sessions", ">", 500)
])

complex_filter = gp.or_filter([us_high, uk_medium])
```

##### More filter examples
See the [examples directory](examples/) for comprehensive filtering examples including:
- Pattern matching with `starts_with`, `ends_with`, and regex
- Range filtering with `between`
- List filtering with `in` and `not_in`
- Negation with `not_filter` or `!=`
- Complex nested combinations

#### Data export and utilities (NEW in v0.5.0!)

##### Export to CSV, Excel, or JSON
Easily export your analytics data to various formats:

```python
# Get your data
df = gp.query(service_account, request)

# Export to CSV
gp.export_to_csv(df, 'analytics_data.csv')

# Export to Excel
gp.export_to_excel(df, 'analytics_data.xlsx')

# Export to JSON
gp.export_to_json(df, 'analytics_data.json')

# Export multiple DataFrames to Excel with custom sheet names
dfs = gp.query(service_account, batch_request, report_type="batch_report")
gp.export_to_excel(dfs, 'analytics.xlsx', sheet_names=['Jan', 'Feb', 'Mar'])
```

##### Compare date ranges
Compare metrics across different time periods:

```python
# Month-over-month comparison
comparison = gp.compare_date_ranges(
    service_account=service_account,
    property_id=property_id,
    dimensions=['country'],
    metrics=['activeUsers', 'sessions'],
    current_start='2024-02-01',
    current_end='2024-02-29',
    previous_start='2024-01-01',
    previous_end='2024-01-31'
)

# Result includes current, previous, absolute change, and % change
print(comparison[['country', 'activeUsers_current', 'activeUsers_previous',
                  'activeUsers_change', 'activeUsers_change_pct']])
```

##### Helper functions for common tasks
Quick shortcuts for frequently-used queries:

```python
# Get top trending content
trending = gp.get_trending_content(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)

# Get top traffic sources
sources = gp.get_traffic_sources(
    service_account=service_account,
    property_id=property_id,
    start_date='2024-01-01',
    end_date='2024-01-31',
    limit=10
)

# Format date ranges easily
last_7_days = gp.format_date_range(7)  # Returns (start_date, end_date)
last_30_days = gp.format_date_range(30, 'yesterday')
```

See [examples/](examples/) for more comprehensive examples of data export, comparison, and helper functions.

#### Batch report
If you construct a protobuf payload using `BatchRunReportsRequest()` you can pass up to five requests at once. These 
are returned as a list of Pandas dataframes, so will need to access them using their index. 

```python
import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'xxxxxxxxx'


batch_report_request = gp.BatchRunReportsRequest(
    property=f"properties/{property_id}",
    requests=[
        gp.RunReportRequest(
            dimensions=[
                gp.Dimension(name="country"),
                gp.Dimension(name="city")
            ],
            metrics=[
                gp.Metric(name="activeUsers")
            ],
            date_ranges=[gp.DateRange(start_date="2022-06-01", end_date="2022-06-01")]
        ),
        gp.RunReportRequest(
            dimensions=[
                gp.Dimension(name="country"),
                gp.Dimension(name="city")
            ],
            metrics=[
                gp.Metric(name="activeUsers")
            ],
            date_ranges=[gp.DateRange(start_date="2022-06-02", end_date="2022-06-02")]
        )
    ]
)

df = gp.query(service_account, batch_report_request, report_type="batch_report")
print(df[0].head())
print(df[1].head())
```

#### Pivot report
Constructing a report using `RunPivotReportRequest()` will return pivoted data in a single Pandas dataframe. 

```python
import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'xxxxxxxxx'

pivot_request = gp.RunPivotReportRequest(
    property=f"properties/{property_id}",
    dimensions=[gp.Dimension(name="country"),
                gp.Dimension(name="browser")],
    metrics=[gp.Metric(name="sessions")],
    date_ranges=[gp.DateRange(start_date="2022-05-30", end_date="today")],
    pivots=[
        gp.Pivot(
            field_names=["country"],
            limit=5,
            order_bys=[
                gp.OrderBy(
                    dimension=gp.OrderBy.DimensionOrderBy(dimension_name="country")
                )
            ],
        ),
        gp.Pivot(
            field_names=["browser"],
            offset=0,
            limit=5,
            order_bys=[
                gp.OrderBy(
                    metric=gp.OrderBy.MetricOrderBy(metric_name="sessions"), desc=True
                )
            ],
        ),
    ],
)

df = gp.query(service_account, pivot_request, report_type="pivot")
print(df.head())
```

#### Batch pivot report
Constructing a payload using `BatchRunPivotReportsRequest()` will allow you to run up to five pivot reports. These 
are returned as a list of Pandas dataframes. 

```python
import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = 'xxxxxxxxx'

batch_pivot_request = gp.BatchRunPivotReportsRequest(
    property=f"properties/{property_id}",
    requests=[
        gp.RunPivotReportRequest(
            dimensions=[gp.Dimension(name="country"),
                        gp.Dimension(name="browser")],
                metrics=[gp.Metric(name="sessions")],
                date_ranges=[gp.DateRange(start_date="2022-05-30", end_date="today")],
                pivots=[
                    gp.Pivot(
                        field_names=["country"],
                        limit=5,
                        order_bys=[
                            gp.OrderBy(
                                dimension=gp.OrderBy.DimensionOrderBy(dimension_name="country")
                            )
                        ],
                    ),
                    gp.Pivot(
                        field_names=["browser"],
                        offset=0,
                        limit=5,
                        order_bys=[
                            gp.OrderBy(
                                metric=gp.OrderBy.MetricOrderBy(metric_name="sessions"), desc=True
                            )
                        ],
                    ),
                ],
        ),
        gp.RunPivotReportRequest(
            dimensions=[gp.Dimension(name="country"),
                        gp.Dimension(name="browser")],
                metrics=[gp.Metric(name="sessions")],
                date_ranges=[gp.DateRange(start_date="2022-05-30", end_date="today")],
                pivots=[
                    gp.Pivot(
                        field_names=["country"],
                        limit=5,
                        order_bys=[
                            gp.OrderBy(
                                dimension=gp.OrderBy.DimensionOrderBy(dimension_name="country")
                            )
                        ],
                    ),
                    gp.Pivot(
                        field_names=["browser"],
                        offset=0,
                        limit=5,
                        order_bys=[
                            gp.OrderBy(
                                metric=gp.OrderBy.MetricOrderBy(metric_name="sessions"), desc=True
                            )
                        ],
                    ),
                ],
        )
    ]
)

df = gp.query(service_account, batch_pivot_request, report_type="batch_pivot")
print(df[0].head())
print(df[1].head())

```

#### Metadata
The `get_metadata()` function will return all metadata on dimensions and metrics within the Google Analytics 4 property. 

```python
metadata = gp.get_metadata(service_account, property_id)
print(metadata)
```

### Features
- **Easy-to-use filter helpers** (NEW in v0.5.0!) - Simple functions for dimension and metric filtering
- **Data export utilities** (NEW in v0.5.0!) - Export to CSV, Excel, and JSON with one line of code
- **Period comparison** (NEW in v0.5.0!) - Compare metrics across different time periods
- **Helper functions** (NEW in v0.5.0!) - Get trending content, traffic sources, and more
- **Full GA4 API support** - `RunReportRequest`, `BatchRunReportsRequest`, `RunPivotReportRequest`, `BatchRunPivotReportsRequest`, `RunRealtimeReportRequest`, and `GetMetadataRequest`
- **Pandas DataFrame output** - Results returned as Pandas DataFrames with proper data types
- **Type hints** - Full type hint support for better IDE autocomplete and type checking
- **Comprehensive testing** - 90%+ test coverage with pytest
- **Modern Python** - Supports Python 3.8+

### What's New in v0.5.0
- 🎉 **Filter helper functions** - Easy dimension and metric filtering
- 📊 **Data export** - Export to CSV, Excel, and JSON formats
- 📈 **Period comparison** - Month-over-month, year-over-year, and custom comparisons
- ⚡ **Helper functions** - Trending content, traffic sources, date range formatting
- 🚀 **Automatic type conversion** - Metrics automatically converted to int/float
- 📚 **Examples directory** - Practical examples for all features
- 🧪 **Comprehensive tests** - All functions fully tested
- 📖 **Improved documentation** - More examples and clearer explanations

See [CHANGELOG.md](CHANGELOG.md) for full version history. 