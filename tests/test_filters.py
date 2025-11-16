"""Tests for filter helper functions."""

import pytest
from google.analytics.data_v1beta.types import FilterExpression, Filter

from gapandas4.filters import (
    FilterBuilder,
    dimension_filter,
    metric_filter,
    and_filter,
    or_filter,
    not_filter,
)


class TestDimensionFilter:
    """Test dimension filter creation."""

    def test_dimension_equals(self):
        """Test dimension equals filter."""
        result = FilterBuilder.dimension_filter("country", "==", "United States")

        assert isinstance(result, FilterExpression)
        assert result.filter.field_name == "country"
        assert result.filter.string_filter.value == "United States"
        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.EXACT
        )

    def test_dimension_equals_alternative_operator(self):
        """Test dimension equals with 'equals' operator."""
        result = FilterBuilder.dimension_filter("city", "equals", "New York")

        assert result.filter.field_name == "city"
        assert result.filter.string_filter.value == "New York"

    def test_dimension_not_equals(self):
        """Test dimension not equals filter."""
        result = FilterBuilder.dimension_filter("country", "!=", "United States")

        assert isinstance(result, FilterExpression)
        assert result.not_expression is not None
        assert result.not_expression.filter.field_name == "country"

    def test_dimension_contains(self):
        """Test dimension contains filter."""
        result = FilterBuilder.dimension_filter("city", "contains", "New")

        assert result.filter.field_name == "city"
        assert result.filter.string_filter.value == "New"
        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.CONTAINS
        )

    def test_dimension_not_contains(self):
        """Test dimension not contains filter."""
        result = FilterBuilder.dimension_filter("city", "not_contains", "Test")

        assert result.not_expression is not None
        assert result.not_expression.filter.field_name == "city"
        assert result.not_expression.filter.string_filter.value == "Test"

    def test_dimension_starts_with(self):
        """Test dimension starts with filter."""
        result = FilterBuilder.dimension_filter("browser", "starts_with", "Chrome")

        assert result.filter.field_name == "browser"
        assert result.filter.string_filter.value == "Chrome"
        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.BEGINS_WITH
        )

    def test_dimension_begins_with_alternative(self):
        """Test dimension begins with alternative operator."""
        result = FilterBuilder.dimension_filter("browser", "begins_with", "Fire")

        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.BEGINS_WITH
        )

    def test_dimension_ends_with(self):
        """Test dimension ends with filter."""
        result = FilterBuilder.dimension_filter("pagePath", "ends_with", ".html")

        assert result.filter.field_name == "pagePath"
        assert result.filter.string_filter.value == ".html"
        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.ENDS_WITH
        )

    def test_dimension_regex(self):
        """Test dimension regex filter."""
        result = FilterBuilder.dimension_filter("pagePath", "regex", "^/blog/.*")

        assert result.filter.field_name == "pagePath"
        assert result.filter.string_filter.value == "^/blog/.*"
        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.FULL_REGEXP
        )

    def test_dimension_matches_regex_alternative(self):
        """Test dimension matches regex alternative operator."""
        result = FilterBuilder.dimension_filter("url", "matches_regex", ".*test.*")

        assert (
            result.filter.string_filter.match_type
            == Filter.StringFilter.MatchType.FULL_REGEXP
        )

    def test_dimension_in_list(self):
        """Test dimension in list filter."""
        countries = ["United States", "Canada", "Mexico"]
        result = FilterBuilder.dimension_filter("country", "in", countries)

        assert result.filter.field_name == "country"
        assert result.filter.in_list_filter is not None
        assert list(result.filter.in_list_filter.values) == countries

    def test_dimension_not_in_list(self):
        """Test dimension not in list filter."""
        browsers = ["Chrome", "Firefox"]
        result = FilterBuilder.dimension_filter("browser", "not_in", browsers)

        assert result.not_expression is not None
        assert result.not_expression.filter.field_name == "browser"
        assert result.not_expression.filter.in_list_filter is not None

    def test_dimension_is_null(self):
        """Test dimension is null filter."""
        result = FilterBuilder.dimension_filter("country", "is_null", None)

        assert result.filter.field_name == "country"
        assert result.filter.null_filter is True

    def test_dimension_is_empty_alternative(self):
        """Test dimension is empty alternative operator."""
        result = FilterBuilder.dimension_filter("city", "is_empty", None)

        assert result.filter.null_filter is True

    def test_dimension_is_not_null(self):
        """Test dimension is not null filter."""
        result = FilterBuilder.dimension_filter("country", "is_not_null", None)

        assert result.not_expression is not None
        assert result.not_expression.filter.field_name == "country"
        assert result.not_expression.filter.null_filter is True

    def test_dimension_is_not_empty_alternative(self):
        """Test dimension is not empty alternative operator."""
        result = FilterBuilder.dimension_filter("city", "is_not_empty", None)

        assert result.not_expression is not None
        assert result.not_expression.filter.null_filter is True

    def test_dimension_case_sensitive(self):
        """Test dimension filter with case sensitivity."""
        result = FilterBuilder.dimension_filter(
            "country", "==", "usa", case_sensitive=True
        )

        assert result.filter.string_filter.case_sensitive is True

    def test_dimension_case_insensitive_default(self):
        """Test dimension filter is case insensitive by default."""
        result = FilterBuilder.dimension_filter("country", "==", "usa")

        assert result.filter.string_filter.case_sensitive is False

    def test_dimension_numeric_value_as_string(self):
        """Test dimension filter with numeric value converted to string."""
        result = FilterBuilder.dimension_filter("eventCount", "==", 5)

        assert result.filter.string_filter.value == "5"

    def test_dimension_invalid_operator(self):
        """Test that invalid operator raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported dimension filter operator"):
            FilterBuilder.dimension_filter("country", "invalid_op", "US")

    def test_dimension_in_operator_requires_list(self):
        """Test that 'in' operator requires a list."""
        with pytest.raises(ValueError, match="requires a list"):
            FilterBuilder.dimension_filter("country", "in", "US")

    def test_dimension_string_operator_invalid_value_type(self):
        """Test that string operators reject list values."""
        with pytest.raises(ValueError, match="requires a string or numeric value"):
            FilterBuilder.dimension_filter("country", "==", ["US", "UK"])


class TestMetricFilter:
    """Test metric filter creation."""

    def test_metric_equals_int(self):
        """Test metric equals filter with integer."""
        result = FilterBuilder.metric_filter("activeUsers", "==", 1000)

        assert isinstance(result, FilterExpression)
        assert result.filter.field_name == "activeUsers"
        assert result.filter.numeric_filter.value.int64_value == 1000
        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.EQUAL
        )

    def test_metric_equals_float(self):
        """Test metric equals filter with float."""
        result = FilterBuilder.metric_filter("bounceRate", "==", 0.45)

        assert result.filter.field_name == "bounceRate"
        assert result.filter.numeric_filter.value.double_value == 0.45

    def test_metric_not_equals(self):
        """Test metric not equals filter."""
        result = FilterBuilder.metric_filter("sessions", "!=", 0)

        assert result.not_expression is not None
        assert result.not_expression.filter.field_name == "sessions"

    def test_metric_greater_than(self):
        """Test metric greater than filter."""
        result = FilterBuilder.metric_filter("activeUsers", ">", 500)

        assert result.filter.field_name == "activeUsers"
        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.GREATER_THAN
        )
        assert result.filter.numeric_filter.value.int64_value == 500

    def test_metric_greater_than_alternative(self):
        """Test metric greater than with alternative operator."""
        result = FilterBuilder.metric_filter("sessions", "greater_than", 100)

        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.GREATER_THAN
        )

    def test_metric_greater_than_or_equal(self):
        """Test metric greater than or equal filter."""
        result = FilterBuilder.metric_filter("sessions", ">=", 100)

        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.GREATER_THAN_OR_EQUAL
        )

    def test_metric_less_than(self):
        """Test metric less than filter."""
        result = FilterBuilder.metric_filter("bounceRate", "<", 0.5)

        assert result.filter.field_name == "bounceRate"
        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.LESS_THAN
        )
        assert result.filter.numeric_filter.value.double_value == 0.5

    def test_metric_less_than_or_equal(self):
        """Test metric less than or equal filter."""
        result = FilterBuilder.metric_filter("activeUsers", "<=", 1000)

        assert (
            result.filter.numeric_filter.operation
            == Filter.NumericFilter.Operation.LESS_THAN_OR_EQUAL
        )

    def test_metric_between_int(self):
        """Test metric between filter with integers."""
        result = FilterBuilder.metric_filter("sessions", "between", [100, 500])

        assert result.filter.field_name == "sessions"
        assert result.filter.between_filter is not None
        assert result.filter.between_filter.from_value.int64_value == 100
        assert result.filter.between_filter.to_value.int64_value == 500

    def test_metric_between_float(self):
        """Test metric between filter with floats."""
        result = FilterBuilder.metric_filter("bounceRate", "between", [0.2, 0.8])

        assert result.filter.between_filter.from_value.double_value == 0.2
        assert result.filter.between_filter.to_value.double_value == 0.8

    def test_metric_invalid_operator(self):
        """Test that invalid operator raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported metric filter operator"):
            FilterBuilder.metric_filter("sessions", "invalid", 100)

    def test_metric_between_requires_two_values(self):
        """Test that 'between' operator requires exactly two values."""
        with pytest.raises(ValueError, match="requires a list of two values"):
            FilterBuilder.metric_filter("sessions", "between", [100])

    def test_metric_between_requires_list(self):
        """Test that 'between' operator requires a list."""
        with pytest.raises(ValueError, match="requires a list of two values"):
            FilterBuilder.metric_filter("sessions", "between", 100)

    def test_metric_comparison_requires_numeric(self):
        """Test that comparison operators require numeric values."""
        with pytest.raises(ValueError, match="requires a numeric value"):
            FilterBuilder.metric_filter("sessions", ">", "not a number")


class TestCombinedFilters:
    """Test combined filter expressions."""

    def test_and_filter(self):
        """Test AND filter combination."""
        filter1 = dimension_filter("country", "==", "US")
        filter2 = metric_filter("sessions", ">", 100)

        result = and_filter([filter1, filter2])

        assert isinstance(result, FilterExpression)
        assert result.and_group is not None
        assert len(result.and_group.expressions) == 2

    def test_and_filter_single(self):
        """Test AND filter with single filter returns the filter unchanged."""
        filter1 = dimension_filter("country", "==", "US")

        result = and_filter([filter1])

        assert result == filter1

    def test_and_filter_empty_raises_error(self):
        """Test that AND filter with empty list raises ValueError."""
        with pytest.raises(ValueError, match="requires at least one filter"):
            and_filter([])

    def test_or_filter(self):
        """Test OR filter combination."""
        filter1 = dimension_filter("country", "==", "US")
        filter2 = dimension_filter("country", "==", "UK")
        filter3 = dimension_filter("country", "==", "CA")

        result = or_filter([filter1, filter2, filter3])

        assert isinstance(result, FilterExpression)
        assert result.or_group is not None
        assert len(result.or_group.expressions) == 3

    def test_or_filter_single(self):
        """Test OR filter with single filter returns the filter unchanged."""
        filter1 = dimension_filter("country", "==", "US")

        result = or_filter([filter1])

        assert result == filter1

    def test_or_filter_empty_raises_error(self):
        """Test that OR filter with empty list raises ValueError."""
        with pytest.raises(ValueError, match="requires at least one filter"):
            or_filter([])

    def test_not_filter(self):
        """Test NOT filter."""
        filter1 = dimension_filter("country", "==", "US")

        result = not_filter(filter1)

        assert isinstance(result, FilterExpression)
        assert result.not_expression is not None
        assert result.not_expression == filter1

    def test_complex_nested_filters(self):
        """Test complex nested filter combinations."""
        # (country == "US" AND sessions > 100) OR (country == "UK" AND sessions > 200)
        us_filter = and_filter([
            dimension_filter("country", "==", "US"),
            metric_filter("sessions", ">", 100)
        ])

        uk_filter = and_filter([
            dimension_filter("country", "==", "UK"),
            metric_filter("sessions", ">", 200)
        ])

        result = or_filter([us_filter, uk_filter])

        assert result.or_group is not None
        assert len(result.or_group.expressions) == 2


class TestConvenienceFunctions:
    """Test convenience function exports."""

    def test_dimension_filter_function(self):
        """Test that convenience dimension_filter function works."""
        result = dimension_filter("country", "==", "US")
        assert isinstance(result, FilterExpression)

    def test_metric_filter_function(self):
        """Test that convenience metric_filter function works."""
        result = metric_filter("sessions", ">", 100)
        assert isinstance(result, FilterExpression)

    def test_and_filter_function(self):
        """Test that convenience and_filter function works."""
        f1 = dimension_filter("country", "==", "US")
        f2 = metric_filter("sessions", ">", 100)
        result = and_filter([f1, f2])
        assert isinstance(result, FilterExpression)

    def test_or_filter_function(self):
        """Test that convenience or_filter function works."""
        f1 = dimension_filter("country", "==", "US")
        f2 = dimension_filter("country", "==", "UK")
        result = or_filter([f1, f2])
        assert isinstance(result, FilterExpression)

    def test_not_filter_function(self):
        """Test that convenience not_filter function works."""
        f1 = dimension_filter("country", "==", "US")
        result = not_filter(f1)
        assert isinstance(result, FilterExpression)
