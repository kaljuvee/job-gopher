#!/usr/bin/env python3
"""
Basic test script to verify JobServe automation setup
"""

import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_chrome_setup():
    """Test if Chrome and ChromeDriver are working"""
    print("🧪 Testing Chrome setup...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        print(f"✅ Chrome setup working! Page title: {title}")
        return True
    except Exception as e:
        print(f"❌ Chrome setup failed: {str(e)}")
        return False

def test_cv_file():
    """Test if CV file exists"""
    print("🧪 Testing CV file...")
    cv_path = "/home/ubuntu/upload/kaljuvee-julian-ds-long-2025.pdf"
    
    if Path(cv_path).exists():
        print(f"✅ CV file found: {cv_path}")
        return True
    else:
        print(f"❌ CV file not found: {cv_path}")
        return False

def test_jobserve_access():
    """Test basic access to JobServe website"""
    print("🧪 Testing JobServe website access...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.jobserve.com")
        title = driver.title
        print(f"✅ JobServe accessible! Page title: {title}")
        
        # Check if we can find key elements
        page_source = driver.page_source.lower()
        if "jobserve" in page_source:
            print("✅ JobServe page loaded correctly")
        else:
            print("⚠️  JobServe page may not have loaded correctly")
        
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ JobServe access failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running JobServe automation tests...\n")
    
    tests = [
        test_chrome_setup,
        test_cv_file,
        test_jobserve_access
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The automation setup is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    exit(main())

