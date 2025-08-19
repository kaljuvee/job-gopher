#!/usr/bin/env python3
"""
Simple test script to demonstrate JobServe automation verification feature
"""

import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    """Setup Chrome driver with proper options for sandbox"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        logger.info("Chrome WebDriver initialized successfully")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
        return None

def test_jobserve_access():
    """Test basic JobServe access and structure"""
    driver = setup_driver()
    if not driver:
        return False
    
    try:
        # Navigate to JobServe
        logger.info("Navigating to JobServe...")
        driver.get("https://www.jobserve.com")
        time.sleep(3)
        
        # Check if we can access the site
        title = driver.title
        logger.info(f"Page title: {title}")
        
        # Check for login status
        if driver.find_elements(By.XPATH, "//a[contains(text(), 'Sign Out')]"):
            logger.info("✅ Already logged in to JobServe")
        else:
            logger.info("ℹ️  Not logged in")
        
        # Navigate to job search
        logger.info("Navigating to job search...")
        driver.get("https://www.jobserve.com/gb/en/JobSearch.aspx?shid=95B145B5415422FF864A&js=1")
        time.sleep(5)
        
        # Check for job listings
        apply_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Apply')]")
        logger.info(f"Found {len(apply_buttons)} apply buttons")
        
        # Check for job titles
        job_titles = driver.find_elements(By.XPATH, "//a[contains(@href, 'jobid')]")
        logger.info(f"Found {len(job_titles)} job title links")
        
        # Test verification URL access
        logger.info("Testing application history access...")
        driver.get("https://www.jobserve.com/ee/en/can/applications")
        time.sleep(3)
        
        page_source = driver.page_source.lower()
        if "limited number of features" in page_source:
            logger.info("⚠️  Application history has limited access")
        else:
            logger.info("✅ Application history accessible")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False
    finally:
        driver.quit()

def simulate_application_verification():
    """Simulate the application verification process"""
    logger.info("🧪 Simulating application verification process...")
    
    # Simulate job titles that would be applied to
    test_jobs = [
        "Data Scientist/Google Gemini/PowerBI/AI/NLP",
        "Senior Data Engineer (Python & SQL)",
        "AI Engineer - Machine Learning",
        "Data Analyst/Business Data Analyst"
    ]
    
    for job_title in test_jobs:
        logger.info(f"📝 Simulating application to: {job_title}")
        
        # Simulate verification logic
        job_title_lower = job_title.lower()
        job_title_variations = [
            job_title_lower,
            job_title_lower.replace(" ", ""),
            job_title_lower.split(" - ")[0] if " - " in job_title_lower else job_title_lower,
            job_title_lower.split(" (")[0] if " (" in job_title_lower else job_title_lower
        ]
        
        logger.info(f"🔍 Verification variations: {job_title_variations}")
        
        # Simulate verification result
        verification_success = True  # In real scenario, this would check the actual page
        
        if verification_success:
            logger.info(f"✅ Application verified in history: {job_title}")
        else:
            logger.info(f"⚠️  Application not found in history: {job_title}")
        
        time.sleep(1)

def main():
    """Main test function"""
    logger.info("🚀 Starting JobServe automation verification test...")
    
    # Test basic access
    access_success = test_jobserve_access()
    
    if access_success:
        logger.info("✅ Basic JobServe access test passed")
    else:
        logger.error("❌ Basic JobServe access test failed")
    
    # Simulate verification process
    simulate_application_verification()
    
    logger.info("🎯 Test completed!")

if __name__ == "__main__":
    main()

