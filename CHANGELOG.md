# CHANGELOG


## [0.3.4] - 2024-10-16
### Added
- pad_string() to pad strings.


## [0.3.3] - 2024-09-24
### Changed
- pretty_print(): Modified this function to handle Class objects with
  non-seralized data.  This should be backwards compatible with the old
  function.  If not, I guess there will be another commit coming your way...


## [0.3.2] - 2024-09-16
### Changed
- pyproject.toml: Setting python=3.11 so I can run this on an ancient Raspberry Pi.
- Bumping Python packages versions.


## [0.3.1] - 2024-07-24
### Fixed
- pyproject.toml: git merged message jacked up the Poetry files.


## [0.3.0] - 2024-07-24
### Added
- test_azure_logger.py, test_custom_logger.py: Adding unit testing to existing
  logger modules.
### Changed
- Bumping Python packages versions.
- Converted docstrings to Google docstring format.


## [0.2.0] - 2024-03-26
### Changed
- common_funcs.py: Removed send_slack_msg(); Will move this to its own module.
- logger/custom_logger.py: Removing logging to Azure.  I rarely use this so I
  will move this to its own module and call it when needed.
- Removing anyio (4.2.0)
- Removing gitdb (4.0.11)
- Removing gitpython (3.1.40)
- Removing smmap (5.0.1)
- Removing sniffio (1.3.0)
- Updating certifi (2023.11.17 -> 2024.2.2)
- Updating urllib3 (2.1.0 -> 2.2.1)
- Updating packaging (23.2 -> 24.0)
- Updating pluggy (1.3.0 -> 1.4.0)
- Updating typing-extensions (4.9.0 -> 4.10.0)
- Updating azure-core (1.29.6 -> 1.30.1)
- Updating cryptography (41.0.7 -> 42.0.5)
- Updating dill (0.3.7 -> 0.3.8)
- Updating platformdirs (4.1.0 -> 4.2.0)
- Updating pytest (7.4.3 -> 7.4.4)
- Updating rich (13.7.0 -> 13.7.1)
- Updating stevedore (5.1.0 -> 5.2.0)
- Updating tomlkit (0.12.3 -> 0.12.4)
- Updating azure-storage-blob (12.19.0 -> 12.19.1)
- Updating bandit (1.7.6 -> 1.7.8)
- Updating coverage (7.3.4 -> 7.4.4)
- Updating slack-sdk (3.26.1 -> 3.27.1)
- Updating tablib (3.5.0 -> 3.6.0)



## [0.1.2] - 2023-12-26
### Changed
- pyproject.toml: Bumping minimum versions.


## [0.1.1] - 2023-11-26
### Changed
- pyproject.toml: Rolling back Python version to 3.11.  v3.12 not in widespread
  use yet...


## [0.1.0] - 2023-11-17
### Added
- Creating a new project to contain classes that I commonly use across all my 
  scripts.
