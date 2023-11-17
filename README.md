# Aaron's Common Library for Python Applications

A Python "library" containing all the classes commonly used across my scripts.

## Getting Started

### About This Code

### Prerequisites / Requirements

* [python-poetry](https://python-poetry.org/) (for package management)
* Network Access to Azure Storage (if logging to Azure is enabled).
* Environment Variables (see below)

#### Environment Variables

* CSV_FILE: Filename for CSV export; .csv extension will be replaced by .json for the summary export.
* Logging: LOG_LEVEL, LOG_PATH
* Slack: SLACK_URL for Webhook URL

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

## Instructions For Use

If using poetry: `poetry add git+ssh://git@github.com:aaronmelton/aaron-common-libs.git#egg=aaron-common-libs`

If using pip: `pip install git+ssh://git@github.com:aaronmelton/aaron-common-libs.git#egg=aaron-common-libs`

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>