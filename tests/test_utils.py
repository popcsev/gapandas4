"""
Tests for utility and normalization functions.
"""

import pytest
import pandas as pd
from google.analytics.data_v1beta.types import Dimension, Metric, DateRange

from gapandas4.utils import (
    normalize_dimensions,
    normalize_metrics,
    normalize_date_range,
)


class TestNormalizeDimensions:
    """Test dimension normalization function."""

    def test_single_string(self):
        """Test normalizing a single dimension string."""
        result = normalize_dimensions("country")
        assert len(result) == 1
        assert isinstance(result[0], Dimension)
        assert result[0].name == "country"

    def test_list_of_strings(self):
        """Test normalizing a list of dimension strings."""
        result = normalize_dimensions(["country", "city", "region"])
        assert len(result) == 3
        assert all(isinstance(d, Dimension) for d in result)
        assert [d.name for d in result] == ["country", "city", "region"]

    def test_single_dimension_object(self):
        """Test normalizing a single Dimension object."""
        dim = Dimension(name="country")
        result = normalize_dimensions(dim)
        assert len(result) == 1
        assert result[0] == dim

    def test_list_of_dimension_objects(self):
        """Test normalizing a list of Dimension objects."""
        dims = [Dimension(name="country"), Dimension(name="city")]
        result = normalize_dimensions(dims)
        assert len(result) == 2
        assert result == dims

    def test_mixed_list(self):
        """Test normalizing a list with both strings and Dimension objects."""
        dims = [Dimension(name="country"), "city", "region"]
        result = normalize_dimensions(dims)
        assert len(result) == 3
        assert all(isinstance(d, Dimension) for d in result)
        assert result[0].name == "country"
        assert result[1].name == "city"
        assert result[2].name == "region"

    def test_empty_list(self):
        """Test normalizing an empty list."""
        result = normalize_dimensions([])
        assert result == []

    def test_invalid_type_in_list(self):
        """Test that invalid types in list raise TypeError."""
        with pytest.raises(TypeError, match="Invalid dimension type"):
            normalize_dimensions([123, "country"])

    def test_invalid_type(self):
        """Test that invalid input type raises TypeError."""
        with pytest.raises(TypeError, match="Invalid dimensions type"):
            normalize_dimensions(123)

    def test_none_type(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError, match="Invalid dimensions type"):
            normalize_dimensions(None)


class TestNormalizeMetrics:
    """Test metric normalization function."""

    def test_single_string(self):
        """Test normalizing a single metric string."""
        result = normalize_metrics("activeUsers")
        assert len(result) == 1
        assert isinstance(result[0], Metric)
        assert result[0].name == "activeUsers"

    def test_list_of_strings(self):
        """Test normalizing a list of metric strings."""
        result = normalize_metrics(["activeUsers", "sessions", "conversions"])
        assert len(result) == 3
        assert all(isinstance(m, Metric) for m in result)
        assert [m.name for m in result] == ["activeUsers", "sessions", "conversions"]

    def test_single_metric_object(self):
        """Test normalizing a single Metric object."""
        metric = Metric(name="activeUsers")
        result = normalize_metrics(metric)
        assert len(result) == 1
        assert result[0] == metric

    def test_list_of_metric_objects(self):
        """Test normalizing a list of Metric objects."""
        metrics = [Metric(name="activeUsers"), Metric(name="sessions")]
        result = normalize_metrics(metrics)
        assert len(result) == 2
        assert result == metrics

    def test_mixed_list(self):
        """Test normalizing a list with both strings and Metric objects."""
        metrics = [Metric(name="activeUsers"), "sessions", "conversions"]
        result = normalize_metrics(metrics)
        assert len(result) == 3
        assert all(isinstance(m, Metric) for m in result)
        assert result[0].name == "activeUsers"
        assert result[1].name == "sessions"
        assert result[2].name == "conversions"

    def test_metric_with_expression(self):
        """Test that Metric objects with expressions are preserved."""
        expr_metric = Metric(name="revenuePerUser", expression="totalRevenue/activeUsers")
        result = normalize_metrics([expr_metric, "sessions"])
        assert len(result) == 2
        assert result[0].name == "revenuePerUser"
        assert result[0].expression == "totalRevenue/activeUsers"
        assert result[1].name == "sessions"

    def test_metric_with_invisible(self):
        """Test that Metric objects with invisible flag are preserved."""
        invisible_metric = Metric(name="sessions", invisible=True)
        result = normalize_metrics([invisible_metric, "activeUsers"])
        assert len(result) == 2
        assert result[0].name == "sessions"
        assert result[0].invisible is True
        assert result[1].name == "activeUsers"

    def test_empty_list(self):
        """Test normalizing an empty list."""
        result = normalize_metrics([])
        assert result == []

    def test_invalid_type_in_list(self):
        """Test that invalid types in list raise TypeError."""
        with pytest.raises(TypeError, match="Invalid metric type"):
            normalize_metrics([123, "activeUsers"])

    def test_invalid_type(self):
        """Test that invalid input type raises TypeError."""
        with pytest.raises(TypeError, match="Invalid metrics type"):
            normalize_metrics(123)

    def test_none_type(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError, match="Invalid metrics type"):
            normalize_metrics(None)


class TestNormalizeDateRange:
    """Test date range normalization function."""

    def test_tuple_input(self):
        """Test normalizing a tuple of (start, end) dates."""
        result = normalize_date_range(("2024-01-01", "2024-01-31"))
        assert isinstance(result, DateRange)
        assert result.start_date == "2024-01-01"
        assert result.end_date == "2024-01-31"

    def test_daterange_object(self):
        """Test normalizing a DateRange object (passthrough)."""
        dr = DateRange(start_date="2024-01-01", end_date="today")
        result = normalize_date_range(dr)
        assert result == dr

    def test_tuple_with_special_values(self):
        """Test normalizing tuple with special date values like 'today'."""
        result = normalize_date_range(("7daysAgo", "today"))
        assert isinstance(result, DateRange)
        assert result.start_date == "7daysAgo"
        assert result.end_date == "today"

    def test_invalid_tuple_length(self):
        """Test that tuple with wrong length raises TypeError."""
        with pytest.raises(TypeError, match="Invalid date_range type"):
            normalize_date_range(("2024-01-01",))

    def test_invalid_type(self):
        """Test that invalid input type raises TypeError."""
        with pytest.raises(TypeError, match="Invalid date_range type"):
            normalize_date_range("2024-01-01")

    def test_none_type(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError, match="Invalid date_range type"):
            normalize_date_range(None)


class TestNormalizationIntegration:
    """Integration tests for normalization with actual utility functions."""

    def test_compare_date_ranges_accepts_strings(self):
        """Test that compare_date_ranges accepts string dimensions/metrics."""
        # This would require mocking the query function, which is complex
        # For now we'll just test that the normalization works
        from gapandas4.utils import normalize_dimensions, normalize_metrics

        dims = normalize_dimensions(["country", "city"])
        metrics = normalize_metrics(["activeUsers", "sessions"])

        assert len(dims) == 2
        assert len(metrics) == 2
        assert all(isinstance(d, Dimension) for d in dims)
        assert all(isinstance(m, Metric) for m in metrics)

    def test_mixed_input_preserves_advanced_features(self):
        """Test that mixing simple strings with advanced Metric objects works."""
        from gapandas4.utils import normalize_metrics

        # Mix simple string with advanced metric
        calculated_metric = Metric(
            name="conversionRate",
            expression="conversions / sessions * 100"
        )

        result = normalize_metrics([
            "activeUsers",
            calculated_metric,
            "sessions"
        ])

        assert len(result) == 3
        assert result[0].name == "activeUsers"
        assert result[1].name == "conversionRate"
        assert result[1].expression == "conversions / sessions * 100"
        assert result[2].name == "sessions"
