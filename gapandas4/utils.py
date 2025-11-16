"""
Utility functions for GAPandas4.

This module provides helper functions for data export, comparison, and batch operations.
"""

from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from datetime import datetime, timedelta
import json

import pandas as pd

from .gapandas4 import query, ReportType
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)


def export_to_csv(
    df: Union[pd.DataFrame, List[pd.DataFrame]],
    filepath: str,
    **kwargs
) -> None:
    """Export DataFrame(s) to CSV file(s).

    Args:
        df: Single DataFrame or list of DataFrames to export
        filepath: Path to save CSV file. For multiple DataFrames, will append
                 index number before extension (e.g., 'data.csv' -> 'data_0.csv', 'data_1.csv')
        **kwargs: Additional arguments passed to pandas to_csv()

    Example:
        >>> df = gp.query(service_account, request)
        >>> gp.export_to_csv(df, 'analytics_data.csv')

        >>> # Multiple DataFrames
        >>> dfs = gp.query(service_account, batch_request, report_type="batch_report")
        >>> gp.export_to_csv(dfs, 'analytics_data.csv')  # Creates data_0.csv, data_1.csv, etc.
    """
    # Set default kwargs for better CSV output
    csv_kwargs = {
        'index': False,
        'encoding': 'utf-8',
    }
    csv_kwargs.update(kwargs)

    if isinstance(df, list):
        # Handle multiple DataFrames
        filepath_obj = Path(filepath)
        stem = filepath_obj.stem
        suffix = filepath_obj.suffix

        for i, dataframe in enumerate(df):
            output_path = filepath_obj.parent / f"{stem}_{i}{suffix}"
            dataframe.to_csv(output_path, **csv_kwargs)
            print(f"Exported DataFrame {i} to {output_path}")
    else:
        # Single DataFrame
        df.to_csv(filepath, **csv_kwargs)
        print(f"Exported to {filepath}")


def export_to_excel(
    df: Union[pd.DataFrame, List[pd.DataFrame]],
    filepath: str,
    sheet_names: Optional[List[str]] = None,
    **kwargs
) -> None:
    """Export DataFrame(s) to Excel file.

    Args:
        df: Single DataFrame or list of DataFrames to export
        filepath: Path to save Excel file
        sheet_names: Optional list of sheet names for multiple DataFrames.
                    If not provided, uses 'Sheet1', 'Sheet2', etc.
        **kwargs: Additional arguments passed to pandas to_excel()

    Raises:
        ImportError: If openpyxl is not installed
        ValueError: If sheet_names length doesn't match number of DataFrames

    Example:
        >>> df = gp.query(service_account, request)
        >>> gp.export_to_excel(df, 'analytics_data.xlsx')

        >>> # Multiple DataFrames with custom sheet names
        >>> dfs = gp.query(service_account, batch_request, report_type="batch_report")
        >>> gp.export_to_excel(dfs, 'analytics_data.xlsx',
        ...                     sheet_names=['Day1', 'Day2', 'Day3'])
    """
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        raise ImportError(
            "openpyxl is required for Excel export. Install it with: pip install openpyxl"
        )

    # Set default kwargs
    excel_kwargs = {
        'index': False,
        'engine': 'openpyxl',
    }
    excel_kwargs.update(kwargs)

    if isinstance(df, list):
        # Handle multiple DataFrames
        if sheet_names and len(sheet_names) != len(df):
            raise ValueError(
                f"sheet_names length ({len(sheet_names)}) must match "
                f"number of DataFrames ({len(df)})"
            )

        if not sheet_names:
            sheet_names = [f"Sheet{i+1}" for i in range(len(df))]

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for i, (dataframe, sheet_name) in enumerate(zip(df, sheet_names)):
                dataframe.to_excel(writer, sheet_name=sheet_name, **excel_kwargs)
            print(f"Exported {len(df)} DataFrames to {filepath}")
    else:
        # Single DataFrame
        sheet_name = sheet_names[0] if sheet_names else 'Sheet1'
        df.to_excel(filepath, sheet_name=sheet_name, **excel_kwargs)
        print(f"Exported to {filepath}")


def export_to_json(
    df: Union[pd.DataFrame, List[pd.DataFrame]],
    filepath: str,
    orient: str = 'records',
    **kwargs
) -> None:
    """Export DataFrame(s) to JSON file.

    Args:
        df: Single DataFrame or list of DataFrames to export
        filepath: Path to save JSON file
        orient: Format of JSON string (records, index, columns, values, table).
               Default is 'records' (list of dicts)
        **kwargs: Additional arguments passed to pandas to_json()

    Example:
        >>> df = gp.query(service_account, request)
        >>> gp.export_to_json(df, 'analytics_data.json')

        >>> # Custom orientation
        >>> gp.export_to_json(df, 'analytics_data.json', orient='table')
    """
    # Set default kwargs for better JSON output
    json_kwargs = {
        'orient': orient,
        'date_format': 'iso',
        'indent': 2,
    }
    json_kwargs.update(kwargs)

    if isinstance(df, list):
        # Handle multiple DataFrames - export as array of objects
        output = [dataframe.to_dict(orient=orient) for dataframe in df]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, default=str)
        print(f"Exported {len(df)} DataFrames to {filepath}")
    else:
        # Single DataFrame
        df.to_json(filepath, **json_kwargs)
        print(f"Exported to {filepath}")


def compare_date_ranges(
    service_account: str,
    property_id: str,
    dimensions: List[str],
    metrics: List[str],
    current_start: str,
    current_end: str,
    previous_start: str,
    previous_end: str,
    **kwargs
) -> pd.DataFrame:
    """Compare metrics across two date ranges.

    Creates a comparison report showing current period, previous period,
    and the change between them.

    Args:
        service_account: Path to Google Service Account JSON keyfile
        property_id: GA4 property ID
        dimensions: List of dimension names (e.g., ['country', 'city'])
        metrics: List of metric names (e.g., ['activeUsers', 'sessions'])
        current_start: Start date for current period (YYYY-MM-DD)
        current_end: End date for current period (YYYY-MM-DD)
        previous_start: Start date for previous period (YYYY-MM-DD)
        previous_end: End date for previous period (YYYY-MM-DD)
        **kwargs: Additional arguments for RunReportRequest (filters, etc.)

    Returns:
        DataFrame with columns for each metric showing:
        - Current period value
        - Previous period value
        - Absolute change
        - Percentage change

    Example:
        >>> # Compare January 2024 vs January 2023
        >>> comparison = gp.compare_date_ranges(
        ...     service_account='client_secrets.json',
        ...     property_id='123456789',
        ...     dimensions=['country'],
        ...     metrics=['activeUsers', 'sessions'],
        ...     current_start='2024-01-01',
        ...     current_end='2024-01-31',
        ...     previous_start='2023-01-01',
        ...     previous_end='2023-01-31'
        ... )
    """
    # Build dimension objects
    dim_objs = [Dimension(name=d) for d in dimensions]
    metric_objs = [Metric(name=m) for m in metrics]

    # Query current period
    current_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dim_objs,
        metrics=metric_objs,
        date_ranges=[DateRange(start_date=current_start, end_date=current_end)],
        **kwargs
    )
    df_current = query(service_account, current_request)

    # Query previous period
    previous_request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dim_objs,
        metrics=metric_objs,
        date_ranges=[DateRange(start_date=previous_start, end_date=previous_end)],
        **kwargs
    )
    df_previous = query(service_account, previous_request)

    # Merge dataframes
    df_comparison = df_current.merge(
        df_previous,
        on=dimensions,
        how='outer',
        suffixes=('_current', '_previous')
    )

    # Calculate changes for each metric
    for metric in metrics:
        current_col = f"{metric}_current"
        previous_col = f"{metric}_previous"

        # Fill NaN with 0 for calculation
        df_comparison[current_col] = df_comparison[current_col].fillna(0)
        df_comparison[previous_col] = df_comparison[previous_col].fillna(0)

        # Absolute change
        df_comparison[f"{metric}_change"] = (
            df_comparison[current_col] - df_comparison[previous_col]
        )

        # Percentage change (avoid division by zero)
        df_comparison[f"{metric}_change_pct"] = df_comparison.apply(
            lambda row: (
                ((row[current_col] - row[previous_col]) / row[previous_col] * 100)
                if row[previous_col] != 0
                else 0
            ),
            axis=1
        )

    return df_comparison


def get_trending_content(
    service_account: str,
    property_id: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    metric: str = "screenPageViews",
    **kwargs
) -> pd.DataFrame:
    """Get top trending content for a time period.

    Args:
        service_account: Path to Google Service Account JSON keyfile
        property_id: GA4 property ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Number of top pages to return (default: 10)
        metric: Metric to sort by (default: 'screenPageViews')
        **kwargs: Additional arguments for RunReportRequest

    Returns:
        DataFrame with top pages sorted by the specified metric

    Example:
        >>> # Get top 10 pages by views
        >>> trending = gp.get_trending_content(
        ...     service_account='client_secrets.json',
        ...     property_id='123456789',
        ...     start_date='2024-01-01',
        ...     end_date='2024-01-31'
        ... )
    """
    from google.analytics.data_v1beta.types import OrderBy

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="pagePath"),
            Dimension(name="pageTitle"),
        ],
        metrics=[
            Metric(name=metric),
            Metric(name="activeUsers"),
            Metric(name="averageSessionDuration"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        order_bys=[
            OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name=metric),
                desc=True
            )
        ],
        limit=limit,
        **kwargs
    )

    df = query(service_account, request)
    return df


def get_traffic_sources(
    service_account: str,
    property_id: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    **kwargs
) -> pd.DataFrame:
    """Get top traffic sources for a time period.

    Args:
        service_account: Path to Google Service Account JSON keyfile
        property_id: GA4 property ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Number of top sources to return (default: 10)
        **kwargs: Additional arguments for RunReportRequest

    Returns:
        DataFrame with top traffic sources sorted by sessions

    Example:
        >>> sources = gp.get_traffic_sources(
        ...     service_account='client_secrets.json',
        ...     property_id='123456789',
        ...     start_date='2024-01-01',
        ...     end_date='2024-01-31'
        ... )
    """
    from google.analytics.data_v1beta.types import OrderBy

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
            Dimension(name="sessionCampaign"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="activeUsers"),
            Metric(name="conversions"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        order_bys=[
            OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name="sessions"),
                desc=True
            )
        ],
        limit=limit,
        **kwargs
    )

    df = query(service_account, request)
    return df


def format_date_range(days_ago: int, end_date: str = "today") -> tuple:
    """Helper function to create date ranges relative to today.

    Args:
        days_ago: Number of days ago to start the range
        end_date: End date (default: 'today'). Can be 'today', 'yesterday', or 'YYYY-MM-DD'

    Returns:
        Tuple of (start_date, end_date) as strings

    Example:
        >>> # Last 7 days
        >>> start, end = gp.format_date_range(7)
        >>> # Last 30 days ending yesterday
        >>> start, end = gp.format_date_range(30, 'yesterday')
    """
    if end_date == "today":
        end = datetime.now().date()
    elif end_date == "yesterday":
        end = datetime.now().date() - timedelta(days=1)
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

    start = end - timedelta(days=days_ago - 1)

    return (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
