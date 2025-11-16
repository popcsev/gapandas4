# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
