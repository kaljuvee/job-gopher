#!/usr/bin/env python3
"""
JobServe Automation Runner

Simple script to run the JobServe job application automation.
Make sure to update config.py with your credentials and preferences.

Usage:
    python run_automation.py
    python run_automation.py --test  # Run with only 2 applications for testing
    python run_automation.py --headless  # Run in headless mode
"""

import argparse
import sys
from pathlib import Path

# Add current directory to path to import local modules
sys.path.append(str(Path(__file__).parent))

from jobserve_automation import JobServeAutomation, UserCredentials, JobSearchCriteria
import config


def main():
    parser = argparse.ArgumentParser(description="JobServe Job Application Automation")
    parser.add_argument("--test", action="store_true", help="Test mode - apply to only 2 jobs")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--max-apps", type=int, help="Maximum number of applications")
    
    args = parser.parse_args()
    
    # Validate CV path (optional since CV may be stored on JobServe)
    if config.CV_PATH and not Path(config.CV_PATH).exists():
        print(f"⚠️  CV file not found at: {config.CV_PATH}")
        print("Continuing anyway - assuming CV is already stored on JobServe")
    elif config.CV_PATH:
        print(f"✅ CV file found: {config.CV_PATH}")
    else:
        print("ℹ️  No CV path specified - assuming CV is already stored on JobServe")
    
    # Validate credentials
    if config.JOBSERVE_EMAIL == "your_email@example.com":
        print("❌ Please update your JobServe credentials in config.py")
        return 1
    
    # Setup credentials
    credentials = UserCredentials(
        email=config.JOBSERVE_EMAIL,
        password=config.JOBSERVE_PASSWORD,
        first_name=config.FIRST_NAME,
        last_name=config.LAST_NAME,
        cv_path=config.CV_PATH
    )
    
    # Setup search criteria
    max_apps = 2 if args.test else (args.max_apps or config.MAX_APPLICATIONS)
    search_criteria = JobSearchCriteria(
        keywords=config.SEARCH_KEYWORDS,
        location=config.SEARCH_LOCATION,
        job_type=config.JOB_TYPE,
        max_applications=max_apps
    )
    
    # Setup automation
    headless = args.headless or config.HEADLESS_MODE
    automation = JobServeAutomation(credentials, search_criteria, headless=headless)
    
    print(f"🚀 Starting JobServe automation...")
    print(f"📧 Email: {credentials.email}")
    print(f"🔍 Search: {search_criteria.keywords} in {search_criteria.location}")
    print(f"📄 CV: {credentials.cv_path}")
    print(f"🎯 Max applications: {max_apps}")
    print(f"🖥️  Headless mode: {headless}")
    
    if args.test:
        print("🧪 Running in TEST MODE - will apply to maximum 2 jobs")
    
    try:
        automation.run_automation()
        print("✅ Automation completed successfully!")
        return 0
    except Exception as e:
        print(f"❌ Automation failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())

