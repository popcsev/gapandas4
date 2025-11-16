"""GAPandas4 - Python package for accessing Google Analytics Data API for GA4 using Pandas."""

from .gapandas4 import query, get_metadata
from .gapandas4 import (
    ReportType,
    GAPandasException,
    ServiceAccountError,
    InvalidReportTypeError,
    InvalidPropertyIDError,
)
from .filters import (
    FilterBuilder,
    dimension_filter,
    metric_filter,
    and_filter,
    or_filter,
    not_filter,
)

# Re-export Google Analytics types for convenience
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

__version__ = "0.5.0"

__all__ = [
    # Core functions
    "query",
    "get_metadata",
    # Enums
    "ReportType",
    # Exceptions
    "GAPandasException",
    "ServiceAccountError",
    "InvalidReportTypeError",
    "InvalidPropertyIDError",
    # Filter helpers
    "FilterBuilder",
    "dimension_filter",
    "metric_filter",
    "and_filter",
    "or_filter",
    "not_filter",
    # Google Analytics types
    "DateRange",
    "Dimension",
    "Metric",
    "OrderBy",
    "Filter",
    "Pivot",
    "FilterExpression",
    "FilterExpressionList",
    "RunReportRequest",
    "BatchRunReportsRequest",
    "RunPivotReportRequest",
    "BatchRunPivotReportsRequest",
    "RunRealtimeReportRequest",
]
