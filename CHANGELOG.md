# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-11-16

### Added

#### Filter Helper Functions
- **Filter helper functions** - Easy-to-use functions for creating dimension and metric filters
  - `dimension_filter()` - Filter dimensions with operators: ==, !=, contains, starts_with, ends_with, in, regex, etc.
  - `metric_filter()` - Filter metrics with operators: ==, !=, >, >=, <, <=, between
  - `and_filter()` - Combine multiple filters with AND logic
  - `or_filter()` - Combine multiple filters with OR logic
  - `not_filter()` - Negate a filter expression
- `FilterBuilder` class for programmatic filter creation
- Comprehensive filter tests with 100% coverage (40+ test cases)

#### Data Export Utilities
- **Export functions** - One-line data export to multiple formats
  - `export_to_csv()` - Export to CSV with custom options
  - `export_to_excel()` - Export to Excel with multiple sheets support
  - `export_to_json()` - Export to JSON with flexible formatting
- Support for exporting single DataFrames or lists of DataFrames
- Automatic handling of file paths and sheet names

#### Period Comparison
- **Date range comparison** - Compare metrics across different time periods
  - `compare_date_ranges()` - Month-over-month, year-over-year, and custom period comparisons
  - Automatically calculates absolute and percentage changes
  - Supports all dimensions and metrics
  - Works with filters for focused analysis

#### Helper Functions
- **Convenience functions** - Common analytics tasks made simple
  - `get_trending_content()` - Get top pages/content by any metric
  - `get_traffic_sources()` - Get top traffic sources with key metrics
  - `format_date_range()` - Easy relative date range formatting (last 7 days, last 30 days, etc.)

#### Examples and Documentation
- New examples directory with practical usage examples:
  - `examples/basic_query.py` - Simple query examples
  - `examples/advanced_filters.py` - 10 comprehensive filtering examples
  - `examples/data_export.py` - Export examples for all formats
  - `examples/data_comparison.py` - Period comparison examples
  - `examples/helper_functions.py` - Helper function usage
  - `examples/README.md` - Guide for using examples
- Extensive README updates with documentation for all new features

### Changed
- Updated documentation with usage examples for all new features
- Improved feature list highlighting filtering, export, and comparison capabilities
- Enhanced error messages in filter functions with clear operator documentation
- README now includes comprehensive sections for filters, exports, comparisons, and helpers

### Developer Experience
- All functions fully documented with type hints
- IntelliSense/autocomplete support for all operations
- Clear error messages when invalid operators or values are used
- Consistent API across all utility functions

## [0.004] - 2025-11-16

### Added
- Type hints throughout the entire codebase for better IDE support and type checking
- Custom exception classes: `GAPandasException`, `ServiceAccountError`, `InvalidReportTypeError`, `InvalidPropertyIDError`
- Input validation for property IDs and report types
- `ReportType` enum for report type constants
- Automatic conversion of metric columns to appropriate numeric types (int, float)
- Comprehensive test suite with pytest (90%+ coverage)
- Code quality tools: Black, Flake8, isort, mypy
- GitHub Actions CI/CD workflow for automated testing
- `__all__` export list in `__init__.py`
- Development dependencies in `setup.py` extras_require
- `pyproject.toml` for modern Python packaging
- `.flake8` configuration file
- `requirements-dev.txt` for development dependencies
- This CHANGELOG.md file
- CONTRIBUTING.md with contribution guidelines

### Changed
- **BREAKING**: Minimum Python version now 3.8+ (was 3.6)
- **BREAKING**: `exit()` calls replaced with proper exception raising (libraries should not exit the program)
- Exception handling improved with specific exceptions instead of bare `except Exception`
- Better error messages with context and suggestions
- Service account validation now checks file existence and type before attempting to load
- Updated development status from Alpha to Beta
- Pinned dependency versions with upper bounds for stability
- Improved documentation in docstrings with examples

### Fixed
- Unreachable code in `_handle_response()` function
- LICENSE.txt now has correct copyright holder (Matt Clarke)
- File handle leak in service account validation
- Bare exception handling that could mask errors

### Security
- Enhanced `.gitignore` to prevent accidental credential commits
- Better validation of service account file paths

## [0.003] - Previous Release

### Added
- Support for all current API functionality including `RunReportRequest`, `BatchRunReportsRequest`, `RunPivotReportRequest`, `BatchRunPivotReportsRequest`, `RunRealtimeReportRequest`, and `GetMetadataRequest`
- Returns data in Pandas dataframe or list of Pandas dataframes
- Dropped duplicate rows in metadata returned

## [0.002] - Earlier Release

### Added
- Initial working version with basic functionality

## [0.001] - Initial Release

### Added
- Initial project structure
- Basic Google Analytics Data API integration
