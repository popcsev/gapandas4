"""
GAPandas4
"""

import os
from enum import Enum
from pathlib import Path
from typing import List, Union, Optional

import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import MetricType
from google.analytics.data_v1beta.types import GetMetadataRequest
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import OrderBy
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import Pivot
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import BatchRunReportsRequest
from google.analytics.data_v1beta.types import RunPivotReportRequest
from google.analytics.data_v1beta.types import BatchRunPivotReportsRequest
from google.analytics.data_v1beta.types import RunRealtimeReportRequest


class ReportType(str, Enum):
    """Enumeration of supported report types."""

    REPORT = "report"
    BATCH_REPORT = "batch_report"
    PIVOT = "pivot"
    BATCH_PIVOT = "batch_pivot"
    REALTIME = "realtime"


class GAPandasException(Exception):
    """Base exception class for GAPandas4 errors."""

    pass


class ServiceAccountError(GAPandasException):
    """Raised when there are issues with the service account credentials."""

    pass


class InvalidReportTypeError(GAPandasException):
    """Raised when an invalid report type is specified."""

    pass


class InvalidPropertyIDError(GAPandasException):
    """Raised when an invalid property ID is specified."""

    pass


def _get_client(service_account: str) -> BetaAnalyticsDataClient:
    """Create a connection using a service account.

    Args:
        service_account: Filepath to Google Service Account client secrets JSON keyfile

    Returns:
        Google Analytics Data API client

    Raises:
        ServiceAccountError: If the service account file doesn't exist or is invalid
    """
    service_account_path = Path(service_account)

    if not service_account_path.exists():
        raise ServiceAccountError(
            f"Service account file not found: {service_account}"
        )

    if not service_account_path.is_file():
        raise ServiceAccountError(
            f"Service account path is not a file: {service_account}"
        )

    try:
        # Set environment variable for Google API authentication
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(service_account_path)
        client = BetaAnalyticsDataClient()
        return client
    except Exception as e:
        raise ServiceAccountError(
            f"Failed to create Google Analytics client: {str(e)}"
        ) from e


def _get_request(
    service_account: str,
    request: Union[
        RunReportRequest,
        BatchRunReportsRequest,
        RunPivotReportRequest,
        BatchRunPivotReportsRequest,
        RunRealtimeReportRequest,
    ],
    report_type: str = ReportType.REPORT,
):
    """Pass a request to the API and return a response.

    Args:
        service_account: Filepath to Google Service Account client secrets JSON keyfile
        request: API request in Protocol Buffer format
        report_type: Report type (report, batch_report, pivot, batch_pivot, or realtime)

    Returns:
        API response

    Raises:
        InvalidReportTypeError: If an invalid report type is specified
    """
    if report_type not in [rt.value for rt in ReportType]:
        raise InvalidReportTypeError(
            f"Invalid report type: {report_type}. Must be one of: {', '.join([rt.value for rt in ReportType])}"
        )

    client = _get_client(service_account)

    if report_type == ReportType.REALTIME:
        response = client.run_realtime_report(request)
    elif report_type == ReportType.PIVOT:
        response = client.run_pivot_report(request)
    elif report_type == ReportType.BATCH_PIVOT:
        response = client.batch_run_pivot_reports(request)
    elif report_type == ReportType.BATCH_REPORT:
        response = client.batch_run_reports(request)
    else:
        response = client.run_report(request)

    return response


def _get_headers(response) -> List[str]:
    """Return a Python list of dimension and metric header names from the Protobuf response.

    Args:
        response: Google Analytics Data API response

    Returns:
        List of column header names
    """
    headers = []

    for header in response.dimension_headers:
        headers.append(header.name)

    for header in response.metric_headers:
        headers.append(header.name)

    return headers


def _get_rows(response) -> List[List[str]]:
    """Return a Python list of row value lists from the Protobuf response.

    Args:
        response: Google Analytics Data API response

    Returns:
        List of rows
    """
    rows = []
    for _row in response.rows:
        row = []
        for dimension in _row.dimension_values:
            row.append(dimension.value)
        for metric in _row.metric_values:
            row.append(metric.value)
        rows.append(row)
    return rows


def _convert_column_types(df: pd.DataFrame, response) -> pd.DataFrame:
    """Convert metric columns to appropriate numeric types.

    Args:
        df: Pandas DataFrame with string columns
        response: Google Analytics Data API response containing metric type information

    Returns:
        DataFrame with properly typed columns
    """
    # Get metric names and their types
    for header in response.metric_headers:
        metric_name = header.name
        if metric_name in df.columns:
            metric_type = MetricType(header.type_).name

            # Convert based on metric type
            if metric_type in ["TYPE_INTEGER", "TYPE_SECONDS", "TYPE_MILLISECONDS"]:
                df[metric_name] = pd.to_numeric(df[metric_name], errors="coerce").astype(
                    "Int64"
                )
            elif metric_type in [
                "TYPE_FLOAT",
                "TYPE_CURRENCY",
                "TYPE_DISTANCE",
                "TYPE_STANDARD",
            ]:
                df[metric_name] = pd.to_numeric(df[metric_name], errors="coerce")

    return df


def _to_dataframe(response) -> pd.DataFrame:
    """Returns a Pandas dataframe of results.

    Args:
        response: Google Analytics Data API response

    Returns:
        Pandas dataframe created from response
    """
    headers = _get_headers(response)
    rows = _get_rows(response)
    df = pd.DataFrame(rows, columns=headers)

    # Convert metric columns to appropriate types
    df = _convert_column_types(df, response)

    return df


def _batch_to_dataframe_list(response) -> List[pd.DataFrame]:
    """Return a list of dataframes of results from a batchRunReports query.

    Args:
        response: Response object from a batchRunReports query

    Returns:
        List of Pandas dataframes of results
    """
    output = []
    for report in response.reports:
        output.append(_to_dataframe(report))
    return output


def _batch_pivot_to_dataframe_list(response) -> List[pd.DataFrame]:
    """Return a list of dataframes of results from a batchRunPivotReports query.

    Args:
        response: Response object from a batchRunPivotReports query

    Returns:
        List of Pandas dataframes of results
    """
    output = []
    for report in response.pivot_reports:
        output.append(_to_dataframe(report))
    return output


def _handle_response(response) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """Use the kind to determine the type of report requested and reformat the output to a Pandas dataframe.

    Args:
        response: Protobuf response object from the Google Analytics Data API

    Returns:
        A single dataframe for runReport, runPivotReport, or runRealtimeReport
        or a list of dataframes for batchRunReports and batchRunPivotReports

    Raises:
        GAPandasException: If the response kind is unsupported
    """
    if response.kind == "analyticsData#runReport":
        return _to_dataframe(response)
    elif response.kind == "analyticsData#batchRunReports":
        return _batch_to_dataframe_list(response)
    elif response.kind == "analyticsData#runPivotReport":
        return _to_dataframe(response)
    elif response.kind == "analyticsData#batchRunPivotReports":
        return _batch_pivot_to_dataframe_list(response)
    elif response.kind == "analyticsData#runRealtimeReport":
        return _to_dataframe(response)
    else:
        raise GAPandasException(f"Unsupported response kind: {response.kind}")


def query(
    service_account: str,
    request: Union[
        RunReportRequest,
        BatchRunReportsRequest,
        RunPivotReportRequest,
        BatchRunPivotReportsRequest,
        RunRealtimeReportRequest,
    ],
    report_type: str = ReportType.REPORT,
) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """Return Pandas formatted data for a Google Analytics Data API query.

    Args:
        service_account: Path to Google Service Account client secrets JSON key file
        request: Google Analytics Data API protocol buffer request
        report_type: Report type (report, batch_report, pivot, batch_pivot, or realtime)

    Returns:
        A single dataframe for runReport, runPivotReport, or runRealtimeReport
        or a list of dataframes for batchRunReports and batchRunPivotReports

    Raises:
        ServiceAccountError: If there are issues with the service account
        InvalidReportTypeError: If an invalid report type is specified
        GAPandasException: For other errors during query execution

    Example:
        >>> import gapandas4 as gp
        >>> service_account = 'client_secrets.json'
        >>> property_id = 'xxxxxxxxx'
        >>> report_request = gp.RunReportRequest(
        ...     property=f"properties/{property_id}",
        ...     dimensions=[gp.Dimension(name="country")],
        ...     metrics=[gp.Metric(name="activeUsers")],
        ...     date_ranges=[gp.DateRange(start_date="2022-06-01", end_date="2022-06-01")]
        ... )
        >>> df = gp.query(service_account, report_request)
    """
    response = _get_request(service_account, request, report_type)
    output = _handle_response(response)
    return output


def get_metadata(service_account: str, property_id: str) -> pd.DataFrame:
    """Return metadata for the Google Analytics property.

    Args:
        service_account: Filepath to Google Service Account client secrets JSON keyfile
        property_id: Google Analytics 4 property ID

    Returns:
        Pandas dataframe of metadata for the property

    Raises:
        ServiceAccountError: If there are issues with the service account
        InvalidPropertyIDError: If the property ID is invalid

    Example:
        >>> import gapandas4 as gp
        >>> metadata = gp.get_metadata('client_secrets.json', '123456789')
    """
    if not property_id:
        raise InvalidPropertyIDError("Property ID cannot be empty")

    # Validate property ID format (should be numeric)
    property_id_clean = property_id.replace("properties/", "")
    if not property_id_clean.isdigit():
        raise InvalidPropertyIDError(
            f"Invalid property ID format: {property_id}. Must be numeric."
        )

    client = _get_client(service_account)
    request = GetMetadataRequest(name=f"properties/{property_id_clean}/metadata")

    try:
        response = client.get_metadata(request)
    except Exception as e:
        raise GAPandasException(
            f"Failed to fetch metadata for property {property_id}: {str(e)}"
        ) from e

    metadata = []
    for dimension in response.dimensions:
        metadata.append(
            {
                "Type": "Dimension",
                "Data type": "STRING",
                "API Name": dimension.api_name,
                "UI Name": dimension.ui_name,
                "Description": dimension.description,
                "Custom definition": dimension.custom_definition,
            }
        )

    for metric in response.metrics:
        metadata.append(
            {
                "Type": "Metric",
                "Data type": MetricType(metric.type_).name,
                "API Name": metric.api_name,
                "UI Name": metric.ui_name,
                "Description": metric.description,
                "Custom definition": metric.custom_definition,
            }
        )

    return pd.DataFrame(metadata).sort_values(by=["Type", "API Name"]).drop_duplicates()
