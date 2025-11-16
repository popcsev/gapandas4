"""
Filter helper functions for GAPandas4.

This module provides easy-to-use functions for creating dimension and metric filters
for Google Analytics 4 Data API queries.
"""

from typing import List, Union, Any

from google.analytics.data_v1beta.types import (
    Filter,
    FilterExpression,
    FilterExpressionList,
)


class FilterBuilder:
    """Helper class for building complex filter expressions."""

    @staticmethod
    def dimension_filter(
        dimension_name: str,
        operator: str,
        value: Union[str, List[str], int, float],
        case_sensitive: bool = False,
    ) -> FilterExpression:
        """Create a dimension filter.

        Args:
            dimension_name: Name of the dimension to filter (e.g., "country", "city")
            operator: Comparison operator. Supported operators:
                - "==" or "equals": Exact match
                - "!=" or "not_equals": Not equal
                - "contains": Contains substring
                - "not_contains": Does not contain substring
                - "starts_with" or "begins_with": Starts with string
                - "ends_with": Ends with string
                - "in": Value in list
                - "not_in": Value not in list
                - "regex" or "matches_regex": Matches regular expression
                - "is_null" or "is_empty": Is null/empty
                - "is_not_null" or "is_not_empty": Is not null/empty
            value: Value to compare against (string, number, or list for 'in'/'not_in')
            case_sensitive: Whether the comparison should be case-sensitive (default: False)

        Returns:
            FilterExpression for dimension filtering

        Raises:
            ValueError: If operator is not supported or value type is invalid

        Example:
            >>> filter1 = FilterBuilder.dimension_filter("country", "==", "United States")
            >>> filter2 = FilterBuilder.dimension_filter("city", "contains", "New")
            >>> filter3 = FilterBuilder.dimension_filter("browser", "in", ["Chrome", "Firefox"])
        """
        operator = operator.lower().strip()

        # Handle null checks
        if operator in ["is_null", "is_empty"]:
            return FilterExpression(
                filter=Filter(
                    field_name=dimension_name,
                    null_filter=True,
                )
            )
        elif operator in ["is_not_null", "is_not_empty"]:
            return FilterExpression(
                not_expression=FilterExpression(
                    filter=Filter(
                        field_name=dimension_name,
                        null_filter=True,
                    )
                )
            )

        # Handle list operators
        if operator in ["in", "not_in"]:
            if not isinstance(value, list):
                raise ValueError(f"Operator '{operator}' requires a list of values")

            filter_expr = FilterExpression(
                filter=Filter(
                    field_name=dimension_name,
                    in_list_filter=Filter.InListFilter(
                        values=[str(v) for v in value],
                        case_sensitive=case_sensitive,
                    ),
                )
            )

            if operator == "not_in":
                return FilterExpression(not_expression=filter_expr)
            return filter_expr

        # Handle string operators
        if not isinstance(value, (str, int, float)):
            raise ValueError(
                f"Operator '{operator}' requires a string or numeric value, got {type(value)}"
            )

        value_str = str(value)

        if operator in ["==", "equals"]:
            match_type = Filter.StringFilter.MatchType.EXACT
        elif operator == "contains":
            match_type = Filter.StringFilter.MatchType.CONTAINS
        elif operator in ["starts_with", "begins_with"]:
            match_type = Filter.StringFilter.MatchType.BEGINS_WITH
        elif operator == "ends_with":
            match_type = Filter.StringFilter.MatchType.ENDS_WITH
        elif operator in ["regex", "matches_regex"]:
            match_type = Filter.StringFilter.MatchType.FULL_REGEXP
        else:
            raise ValueError(
                f"Unsupported dimension filter operator: '{operator}'. "
                f"Supported operators: ==, !=, contains, not_contains, starts_with, "
                f"ends_with, in, not_in, regex, is_null, is_not_null"
            )

        filter_expr = FilterExpression(
            filter=Filter(
                field_name=dimension_name,
                string_filter=Filter.StringFilter(
                    match_type=match_type,
                    value=value_str,
                    case_sensitive=case_sensitive,
                ),
            )
        )

        # Handle negation operators
        if operator in ["!=", "not_equals", "not_contains"]:
            if operator == "not_contains":
                # First create contains filter, then negate it
                filter_expr = FilterExpression(
                    filter=Filter(
                        field_name=dimension_name,
                        string_filter=Filter.StringFilter(
                            match_type=Filter.StringFilter.MatchType.CONTAINS,
                            value=value_str,
                            case_sensitive=case_sensitive,
                        ),
                    )
                )
            return FilterExpression(not_expression=filter_expr)

        return filter_expr

    @staticmethod
    def metric_filter(
        metric_name: str,
        operator: str,
        value: Union[int, float, List[Union[int, float]]],
    ) -> FilterExpression:
        """Create a metric filter.

        Args:
            metric_name: Name of the metric to filter (e.g., "activeUsers", "sessions")
            operator: Comparison operator. Supported operators:
                - "==" or "equals": Equal to
                - "!=" or "not_equals": Not equal to
                - ">" or "greater_than": Greater than
                - ">=" or "greater_than_or_equal": Greater than or equal
                - "<" or "less_than": Less than
                - "<=" or "less_than_or_equal": Less than or equal
                - "between": Between two values (inclusive)
            value: Numeric value to compare against, or list of [min, max] for 'between'

        Returns:
            FilterExpression for metric filtering

        Raises:
            ValueError: If operator is not supported or value type is invalid

        Example:
            >>> filter1 = FilterBuilder.metric_filter("activeUsers", ">", 1000)
            >>> filter2 = FilterBuilder.metric_filter("sessions", "between", [100, 500])
            >>> filter3 = FilterBuilder.metric_filter("bounceRate", "<=", 0.5)
        """
        operator = operator.lower().strip()

        # Handle between operator
        if operator == "between":
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError(
                    "Operator 'between' requires a list of two values: [min, max]"
                )

            return FilterExpression(
                filter=Filter(
                    field_name=metric_name,
                    between_filter=Filter.BetweenFilter(
                        from_value=Filter.NumericValue(
                            int64_value=int(value[0])
                            if isinstance(value[0], int)
                            else None,
                            double_value=float(value[0])
                            if isinstance(value[0], float)
                            else None,
                        ),
                        to_value=Filter.NumericValue(
                            int64_value=int(value[1])
                            if isinstance(value[1], int)
                            else None,
                            double_value=float(value[1])
                            if isinstance(value[1], float)
                            else None,
                        ),
                    ),
                )
            )

        # Handle numeric comparison operators
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Operator '{operator}' requires a numeric value, got {type(value)}"
            )

        if operator in ["==", "equals"]:
            operation = Filter.NumericFilter.Operation.EQUAL
        elif operator in ["<", "less_than"]:
            operation = Filter.NumericFilter.Operation.LESS_THAN
        elif operator in ["<=", "less_than_or_equal"]:
            operation = Filter.NumericFilter.Operation.LESS_THAN_OR_EQUAL
        elif operator in [">", "greater_than"]:
            operation = Filter.NumericFilter.Operation.GREATER_THAN
        elif operator in [">=", "greater_than_or_equal"]:
            operation = Filter.NumericFilter.Operation.GREATER_THAN_OR_EQUAL
        else:
            raise ValueError(
                f"Unsupported metric filter operator: '{operator}'. "
                f"Supported operators: ==, !=, >, >=, <, <=, between"
            )

        filter_expr = FilterExpression(
            filter=Filter(
                field_name=metric_name,
                numeric_filter=Filter.NumericFilter(
                    operation=operation,
                    value=Filter.NumericValue(
                        int64_value=int(value) if isinstance(value, int) else None,
                        double_value=float(value) if isinstance(value, float) else None,
                    ),
                ),
            )
        )

        # Handle not equals
        if operator in ["!=", "not_equals"]:
            return FilterExpression(not_expression=filter_expr)

        return filter_expr

    @staticmethod
    def and_filter(filters: List[FilterExpression]) -> FilterExpression:
        """Combine multiple filters with AND logic.

        All filters must be true for the row to be included.

        Args:
            filters: List of FilterExpression objects to combine

        Returns:
            FilterExpression combining all filters with AND

        Raises:
            ValueError: If filters list is empty or contains invalid items

        Example:
            >>> filter1 = FilterBuilder.dimension_filter("country", "==", "US")
            >>> filter2 = FilterBuilder.metric_filter("sessions", ">", 100)
            >>> combined = FilterBuilder.and_filter([filter1, filter2])
        """
        if not filters:
            raise ValueError("and_filter requires at least one filter")

        if len(filters) == 1:
            return filters[0]

        return FilterExpression(
            and_group=FilterExpressionList(expressions=filters)
        )

    @staticmethod
    def or_filter(filters: List[FilterExpression]) -> FilterExpression:
        """Combine multiple filters with OR logic.

        At least one filter must be true for the row to be included.

        Args:
            filters: List of FilterExpression objects to combine

        Returns:
            FilterExpression combining all filters with OR

        Raises:
            ValueError: If filters list is empty or contains invalid items

        Example:
            >>> filter1 = FilterBuilder.dimension_filter("country", "==", "US")
            >>> filter2 = FilterBuilder.dimension_filter("country", "==", "UK")
            >>> combined = FilterBuilder.or_filter([filter1, filter2])
        """
        if not filters:
            raise ValueError("or_filter requires at least one filter")

        if len(filters) == 1:
            return filters[0]

        return FilterExpression(or_group=FilterExpressionList(expressions=filters))

    @staticmethod
    def not_filter(filter_expr: FilterExpression) -> FilterExpression:
        """Negate a filter expression.

        Args:
            filter_expr: FilterExpression to negate

        Returns:
            FilterExpression that negates the input

        Example:
            >>> filter1 = FilterBuilder.dimension_filter("country", "==", "US")
            >>> not_us = FilterBuilder.not_filter(filter1)  # All countries except US
        """
        return FilterExpression(not_expression=filter_expr)


# Convenience functions for backward compatibility and ease of use
def dimension_filter(
    dimension_name: str,
    operator: str,
    value: Union[str, List[str], int, float],
    case_sensitive: bool = False,
) -> FilterExpression:
    """Create a dimension filter. See FilterBuilder.dimension_filter for details."""
    return FilterBuilder.dimension_filter(dimension_name, operator, value, case_sensitive)


def metric_filter(
    metric_name: str,
    operator: str,
    value: Union[int, float, List[Union[int, float]]],
) -> FilterExpression:
    """Create a metric filter. See FilterBuilder.metric_filter for details."""
    return FilterBuilder.metric_filter(metric_name, operator, value)


def and_filter(filters: List[FilterExpression]) -> FilterExpression:
    """Combine filters with AND logic. See FilterBuilder.and_filter for details."""
    return FilterBuilder.and_filter(filters)


def or_filter(filters: List[FilterExpression]) -> FilterExpression:
    """Combine filters with OR logic. See FilterBuilder.or_filter for details."""
    return FilterBuilder.or_filter(filters)


def not_filter(filter_expr: FilterExpression) -> FilterExpression:
    """Negate a filter. See FilterBuilder.not_filter for details."""
    return FilterBuilder.not_filter(filter_expr)
