"""
Configuration file for JobServe automation

Update these settings according to your preferences and credentials.
"""

import os
from pathlib import Path

# JobServe Login Credentials
JOBSERVE_EMAIL = os.getenv("JOBSERVE_EMAIL", "kaljuvee@gmail.com")
JOBSERVE_PASSWORD = os.getenv("JOBSERVE_PASSWORD", "Toomesilane2$2")

# Personal Information
FIRST_NAME = "Julian"
LAST_NAME = "Kaljuvee"

# CV Path - Leave empty since CV is already stored on JobServe
CV_PATH = os.getenv("CV_PATH", "")

# Job Search Criteria
SEARCH_KEYWORDS = "data scientist, AI engineer"
SEARCH_LOCATION = "London"
JOB_TYPE = "Contract/Full Time"  # Options: Any, Full Time, Contract, Contract/Full Time, Part Time/Temporary/Seasonal
DISTANCE = "Within 25 miles"
MAX_APPLICATIONS = 50

# Automation Settings
HEADLESS_MODE = False  # Set to True to run browser in background
DELAY_BETWEEN_APPLICATIONS = 5  # seconds
TIMEOUT_SECONDS = 10

# Output Settings
SAVE_SCREENSHOTS = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Browser Settings
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080

# Job Filtering Keywords (jobs containing these keywords will be prioritized)
PRIORITY_KEYWORDS = [
    "data scientist",
    "ai engineer", 
    "machine learning",
    "data engineer",
    "tech lead",
    "ai developer",
    "data analyst",
    "python",
    "sql",
    "tensorflow",
    "pytorch"
]

# Exclude keywords (jobs containing these will be skipped)
EXCLUDE_KEYWORDS = [
    "senior manager",
    "director",
    "head of",
    "chief",
    "intern",
    "graduate"
]

