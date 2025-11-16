"""Unit tests for GAPandas4."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

import pandas as pd
import pytest

from gapandas4 import (
    query,
    get_metadata,
    ReportType,
    GAPandasException,
    ServiceAccountError,
    InvalidReportTypeError,
    InvalidPropertyIDError,
)
from gapandas4.gapandas4 import (
    _get_client,
    _get_headers,
    _get_rows,
    _convert_column_types,
    _to_dataframe,
    _handle_response,
)


class TestExceptions:
    """Test custom exception classes."""

    def test_base_exception(self):
        """Test GAPandasException."""
        exc = GAPandasException("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_service_account_error(self):
        """Test ServiceAccountError."""
        exc = ServiceAccountError("Service account error")
        assert str(exc) == "Service account error"
        assert isinstance(exc, GAPandasException)

    def test_invalid_report_type_error(self):
        """Test InvalidReportTypeError."""
        exc = InvalidReportTypeError("Invalid report type")
        assert str(exc) == "Invalid report type"
        assert isinstance(exc, GAPandasException)

    def test_invalid_property_id_error(self):
        """Test InvalidPropertyIDError."""
        exc = InvalidPropertyIDError("Invalid property ID")
        assert str(exc) == "Invalid property ID"
        assert isinstance(exc, GAPandasException)


class TestReportType:
    """Test ReportType enum."""

    def test_report_types(self):
        """Test all report type values."""
        assert ReportType.REPORT == "report"
        assert ReportType.BATCH_REPORT == "batch_report"
        assert ReportType.PIVOT == "pivot"
        assert ReportType.BATCH_PIVOT == "batch_pivot"
        assert ReportType.REALTIME == "realtime"


class TestGetClient:
    """Test _get_client function."""

    def test_service_account_not_found(self):
        """Test that ServiceAccountError is raised when file doesn't exist."""
        with pytest.raises(ServiceAccountError, match="Service account file not found"):
            _get_client("/nonexistent/path/to/file.json")

    def test_service_account_is_directory(self):
        """Test that ServiceAccountError is raised when path is a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ServiceAccountError, match="not a file"):
                _get_client(tmpdir)

    @patch("gapandas4.gapandas4.BetaAnalyticsDataClient")
    def test_successful_client_creation(self, mock_client_class):
        """Test successful client creation."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp.write(b'{"test": "data"}')
            tmp_path = tmp.name

        try:
            mock_client = Mock()
            mock_client_class.return_value = mock_client

            client = _get_client(tmp_path)

            assert client == mock_client
            assert os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") == tmp_path
            mock_client_class.assert_called_once()
        finally:
            os.unlink(tmp_path)


class TestGetHeaders:
    """Test _get_headers function."""

    def test_get_headers_with_dimensions_and_metrics(self):
        """Test extracting headers from response."""
        mock_response = Mock()
        mock_response.dimension_headers = [
            Mock(name="country"),
            Mock(name="city"),
        ]
        mock_response.metric_headers = [
            Mock(name="activeUsers"),
            Mock(name="sessions"),
        ]

        headers = _get_headers(mock_response)

        assert headers == ["country", "city", "activeUsers", "sessions"]

    def test_get_headers_empty(self):
        """Test with no headers."""
        mock_response = Mock()
        mock_response.dimension_headers = []
        mock_response.metric_headers = []

        headers = _get_headers(mock_response)

        assert headers == []


class TestGetRows:
    """Test _get_rows function."""

    def test_get_rows_with_data(self):
        """Test extracting rows from response."""
        mock_dim1 = Mock(value="US")
        mock_dim2 = Mock(value="New York")
        mock_metric1 = Mock(value="1000")
        mock_metric2 = Mock(value="500")

        mock_row = Mock()
        mock_row.dimension_values = [mock_dim1, mock_dim2]
        mock_row.metric_values = [mock_metric1, mock_metric2]

        mock_response = Mock()
        mock_response.rows = [mock_row]

        rows = _get_rows(mock_response)

        assert rows == [["US", "New York", "1000", "500"]]

    def test_get_rows_empty(self):
        """Test with no rows."""
        mock_response = Mock()
        mock_response.rows = []

        rows = _get_rows(mock_response)

        assert rows == []


class TestConvertColumnTypes:
    """Test _convert_column_types function."""

    def test_convert_integer_metrics(self):
        """Test converting integer metric types."""
        df = pd.DataFrame({"activeUsers": ["100", "200", "300"]})

        mock_header = Mock()
        mock_header.name = "activeUsers"
        mock_header.type_ = 1  # TYPE_INTEGER

        mock_response = Mock()
        mock_response.metric_headers = [mock_header]

        result_df = _convert_column_types(df, mock_response)

        assert result_df["activeUsers"].dtype == "Int64"
        assert result_df["activeUsers"].tolist() == [100, 200, 300]

    def test_convert_float_metrics(self):
        """Test converting float metric types."""
        df = pd.DataFrame({"bounceRate": ["0.45", "0.52", "0.38"]})

        mock_header = Mock()
        mock_header.name = "bounceRate"
        mock_header.type_ = 2  # TYPE_FLOAT

        mock_response = Mock()
        mock_response.metric_headers = [mock_header]

        result_df = _convert_column_types(df, mock_response)

        assert result_df["bounceRate"].dtype == "float64"
        assert result_df["bounceRate"].tolist() == pytest.approx([0.45, 0.52, 0.38])


class TestToDataFrame:
    """Test _to_dataframe function."""

    def test_to_dataframe(self):
        """Test converting response to DataFrame."""
        mock_response = Mock()
        mock_response.dimension_headers = [Mock(name="country")]
        mock_response.metric_headers = [Mock(name="activeUsers", type_=1)]

        mock_row = Mock()
        mock_row.dimension_values = [Mock(value="US")]
        mock_row.metric_values = [Mock(value="1000")]
        mock_response.rows = [mock_row]

        df = _to_dataframe(mock_response)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["country", "activeUsers"]
        assert len(df) == 1
        assert df["country"].iloc[0] == "US"
        assert df["activeUsers"].iloc[0] == 1000


class TestHandleResponse:
    """Test _handle_response function."""

    def test_handle_run_report(self):
        """Test handling runReport response."""
        mock_response = Mock()
        mock_response.kind = "analyticsData#runReport"
        mock_response.dimension_headers = [Mock(name="country")]
        mock_response.metric_headers = [Mock(name="activeUsers", type_=1)]
        mock_response.rows = []

        result = _handle_response(mock_response)

        assert isinstance(result, pd.DataFrame)

    def test_handle_batch_reports(self):
        """Test handling batchRunReports response."""
        mock_report1 = Mock()
        mock_report1.dimension_headers = [Mock(name="country")]
        mock_report1.metric_headers = [Mock(name="activeUsers", type_=1)]
        mock_report1.rows = []

        mock_report2 = Mock()
        mock_report2.dimension_headers = [Mock(name="city")]
        mock_report2.metric_headers = [Mock(name="sessions", type_=1)]
        mock_report2.rows = []

        mock_response = Mock()
        mock_response.kind = "analyticsData#batchRunReports"
        mock_response.reports = [mock_report1, mock_report2]

        result = _handle_response(mock_response)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(df, pd.DataFrame) for df in result)

    def test_handle_unsupported_response(self):
        """Test handling unsupported response kind."""
        mock_response = Mock()
        mock_response.kind = "unsupported#kind"

        with pytest.raises(GAPandasException, match="Unsupported response kind"):
            _handle_response(mock_response)


class TestGetMetadata:
    """Test get_metadata function."""

    def test_empty_property_id(self):
        """Test that empty property ID raises error."""
        with pytest.raises(InvalidPropertyIDError, match="cannot be empty"):
            get_metadata("service_account.json", "")

    def test_invalid_property_id_format(self):
        """Test that non-numeric property ID raises error."""
        with pytest.raises(InvalidPropertyIDError, match="Must be numeric"):
            get_metadata("service_account.json", "invalid-id")

    @patch("gapandas4.gapandas4._get_client")
    def test_get_metadata_success(self, mock_get_client):
        """Test successful metadata retrieval."""
        # Create mock client
        mock_client = Mock()

        # Create mock dimension
        mock_dimension = Mock()
        mock_dimension.api_name = "country"
        mock_dimension.ui_name = "Country"
        mock_dimension.description = "User country"
        mock_dimension.custom_definition = False

        # Create mock metric
        mock_metric = Mock()
        mock_metric.api_name = "activeUsers"
        mock_metric.ui_name = "Active Users"
        mock_metric.description = "Number of active users"
        mock_metric.custom_definition = False
        mock_metric.type_ = 1  # TYPE_INTEGER

        # Create mock response
        mock_response = Mock()
        mock_response.dimensions = [mock_dimension]
        mock_response.metrics = [mock_metric]

        mock_client.get_metadata.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_metadata("service_account.json", "123456789")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "Type" in result.columns
        assert "API Name" in result.columns


class TestQuery:
    """Test query function."""

    def test_invalid_report_type(self):
        """Test that invalid report type raises error."""
        mock_request = Mock()

        with pytest.raises(InvalidReportTypeError, match="Invalid report type"):
            query("service_account.json", mock_request, report_type="invalid_type")

    @patch("gapandas4.gapandas4._get_request")
    def test_query_with_valid_report_type(self, mock_get_request):
        """Test query with valid report type."""
        mock_response = Mock()
        mock_response.kind = "analyticsData#runReport"
        mock_response.dimension_headers = [Mock(name="country")]
        mock_response.metric_headers = [Mock(name="activeUsers", type_=1)]
        mock_response.rows = []

        mock_get_request.return_value = mock_response
        mock_request = Mock()

        result = query("service_account.json", mock_request, report_type="report")

        assert isinstance(result, pd.DataFrame)
        mock_get_request.assert_called_once()
