# GAPandas4 Examples

This directory contains practical examples demonstrating how to use GAPandas4 for various Google Analytics 4 reporting tasks.

## Setup

Before running these examples, you need to:

1. **Create a Google Service Account** and download the JSON keyfile
   - Follow this guide: https://practicaldatascience.co.uk/data-engineering/how-to-create-a-google-service-account-client-secrets-json-key

2. **Add the service account to your GA4 property** with Viewer permissions

3. **Update the examples** with your credentials:
   ```python
   service_account = 'path/to/your/client_secrets.json'
   property_id = 'YOUR_PROPERTY_ID'  # Your GA4 property ID (numeric)
   ```

## Examples

### basic_query.py
The simplest way to query GA4 data. Perfect for getting started.
- Basic report structure
- Dimensions and metrics
- Simple data analysis

### advanced_filters.py
Comprehensive filtering examples covering:
- Dimension filters (equals, contains, starts_with, regex, etc.)
- Metric filters (comparisons, ranges)
- Combining filters (AND, OR, NOT)
- Complex nested filters
- Pattern matching

## Running the Examples

```bash
# Install GAPandas4
pip install gapandas4

# Run an example
python examples/basic_query.py
```

## Common Dimensions and Metrics

### Popular Dimensions
- `country`, `city`, `region`
- `browser`, `deviceCategory`, `operatingSystem`
- `pagePath`, `pageTitle`
- `sessionSource`, `sessionMedium`, `sessionCampaign`
- `date`, `year`, `month`, `day`

### Popular Metrics
- `activeUsers`, `totalUsers`, `newUsers`
- `sessions`, `sessionsPerUser`
- `screenPageViews`, `screenPageViewsPerSession`
- `averageSessionDuration`
- `bounceRate`, `engagementRate`
- `conversions`, `totalRevenue`

For a complete list, use:
```python
metadata = gp.get_metadata(service_account, property_id)
print(metadata)
```

## Need Help?

- Check the [main README](../README.md)
- Review the [API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- Open an issue on GitHub
