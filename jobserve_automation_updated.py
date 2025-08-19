#!/usr/bin/env python3
"""
JobServe UK Job Application Automation Script - Updated Version

This script automates the process of applying to jobs on JobServe UK.
Updated with current website structure and element selectors.

Author: Julian Kaljuvee
Date: August 2025
"""

import time
import logging
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


@dataclass
class JobSearchCriteria:
    """Job search criteria configuration"""
    keywords: str = "data scientist, AI engineer"
    location: str = "London"
    job_type: str = "Contract"
    distance: str = "Within 25 miles"
    max_applications: int = 50


@dataclass
class UserCredentials:
    """User credentials for JobServe login"""
    email: str
    password: str
    first_name: str = "Julian"
    last_name: str = "Kaljuvee"
    cv_path: str = ""


@dataclass
class ApplicationResult:
    """Result of a job application attempt"""
    job_title: str = ""
    company: str = ""
    reference: str = ""
    status: str = "pending"  # pending, success, verified, failed, error
    error_message: str = ""
    application_date: str = ""


class JobServeAutomation:
    """Main automation class for JobServe job applications"""
    
    def __init__(self, credentials: UserCredentials, search_criteria: JobSearchCriteria, headless: bool = True):
        self.credentials = credentials
        self.search_criteria = search_criteria
        self.headless = headless
        self.driver = None
        self.wait = None
        self.applications_submitted = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('jobserve_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Try to use system ChromeDriver first
        try:
            from selenium.webdriver.chrome.service import Service
            service = Service("/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback to webdriver-manager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except:
                # Last resort - try default
                self.driver = webdriver.Chrome(options=chrome_options)
        
        self.wait = WebDriverWait(self.driver, 10)
        self.logger.info("Chrome WebDriver initialized")
    
    def navigate_to_jobserve(self):
        """Navigate to JobServe UK website"""
        try:
            self.driver.get("https://www.jobserve.com")
            time.sleep(3)
            self.logger.info("Navigated to JobServe.com")
            
            # Check if we're already logged in by looking for Sign Out
            if self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Sign Out')]"):
                self.logger.info("Already logged in to JobServe")
                return True
            
            self.logger.info("Not logged in, proceeding with login")
            return True
                
        except Exception as e:
            self.logger.error(f"Error navigating to JobServe: {str(e)}")
            raise
    
    def login(self):
        """Login to JobServe with provided credentials"""
        try:
            # Check if already logged in
            if self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Sign Out')]"):
                self.logger.info("Already logged in, skipping login process")
                return True
            
            # Look for login/sign in links
            login_elements = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(@href, 'login')]")
            
            if login_elements:
                login_elements[0].click()
                time.sleep(2)
                
                # Fill in credentials if login form is present
                email_fields = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='email'], input[name*='email'], input[id*='email']")
                password_fields = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='password'], input[name*='password'], input[id*='password']")
                
                if email_fields and password_fields:
                    email_fields[0].send_keys(self.credentials.email)
                    password_fields[0].send_keys(self.credentials.password)
                    
                    # Find and click submit button
                    submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                        "input[type='submit'], button[type='submit'], button[contains(text(), 'Sign In')]")
                    if submit_buttons:
                        submit_buttons[0].click()
                        time.sleep(3)
            
            # Verify login success
            if self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Sign Out')]"):
                self.logger.info("Login successful")
                return True
            else:
                self.logger.warning("Login status unclear, continuing anyway")
                return True
                
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return True  # Continue anyway, might already be logged in
    
    def search_jobs(self):
        """Navigate to job search and set up search criteria"""
        try:
            # Navigate to job search page
            self.driver.get("https://www.jobserve.com/gb/en/JobSearch.aspx")
            time.sleep(3)
            
            # Check if we're on a search results page already
            if "JobSearch.aspx" in self.driver.current_url:
                self.logger.info("Already on job search page")
                return True
            
            # Look for job search link
            job_search_links = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Job Search') or contains(@href, 'JobSearch')]")
            
            if job_search_links:
                job_search_links[0].click()
                time.sleep(3)
                self.logger.info("Navigated to job search")
                return True
            
            self.logger.warning("Could not find job search, but continuing")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in job search navigation: {str(e)}")
            return False
    
    def get_job_listings(self) -> List[Dict]:
        """Get list of available job listings"""
        jobs = []
        try:
            # Look for apply buttons which indicate available jobs
            apply_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Apply')]")
            
            for i, apply_button in enumerate(apply_buttons[:self.search_criteria.max_applications]):
                try:
                    # Find the job title associated with this apply button
                    # Look for nearby job title elements
                    parent = apply_button.find_element(By.XPATH, "./..")
                    job_title_elements = parent.find_elements(By.XPATH, 
                        ".//a[contains(@href, 'jobid') or contains(@class, 'job')]")
                    
                    if job_title_elements:
                        job_title = job_title_elements[0].text.strip()
                        job_url = job_title_elements[0].get_attribute('href')
                    else:
                        # Fallback: look for any nearby text that might be a job title
                        job_title = f"Job {i+1}"
                        job_url = self.driver.current_url
                    
                    # Check if this is a relevant job
                    if any(keyword.lower() in job_title.lower() 
                           for keyword in ['data', 'ai', 'engineer', 'scientist', 'tech', 'lead', 'analyst']):
                        jobs.append({
                            'title': job_title,
                            'url': job_url,
                            'apply_button': apply_button
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting job info for button {i}: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(jobs)} suitable job listings")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error getting job listings: {str(e)}")
            return []
    
    def apply_to_job(self, job: Dict) -> ApplicationResult:
        """Apply to a specific job"""
        result = ApplicationResult(
            job_title=job['title'],
            application_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        try:
            # Click the apply button
            apply_button = job['apply_button']
            self.driver.execute_script("arguments[0].click();", apply_button)
            time.sleep(3)
            
            # Check if application modal/form opened
            if self.is_application_form_present():
                return self.fill_application_form(result)
            else:
                result.status = "failed"
                result.error_message = "Application form did not open"
                return result
                
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            self.logger.error(f"Error applying to job {job['title']}: {str(e)}")
            return result
    
    def is_application_form_present(self) -> bool:
        """Check if application form is present"""
        form_indicators = [
            "//div[contains(text(), 'Job Application')]",
            "//h1[contains(text(), 'Job Application')]",
            "//input[@type='email']",
            "//select[contains(@name, 'status')]",
            "//button[contains(text(), 'Apply')]"
        ]
        
        for indicator in form_indicators:
            if self.driver.find_elements(By.XPATH, indicator):
                return True
        return False
    
    def fill_application_form(self, result: ApplicationResult) -> ApplicationResult:
        """Fill out the job application form"""
        try:
            # Email field (usually pre-filled)
            email_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
            if email_fields and not email_fields[0].get_attribute('value'):
                email_fields[0].clear()
                email_fields[0].send_keys(self.credentials.email)
            
            # Working status dropdown (usually pre-filled with UK Citizen)
            status_selects = self.driver.find_elements(By.CSS_SELECTOR, "select")
            if status_selects:
                # Check if it's already set to UK Citizen or similar
                current_value = status_selects[0].get_attribute('value')
                if not current_value or current_value == "":
                    status_select = Select(status_selects[0])
                    for option in status_select.options:
                        if any(term in option.text.lower() for term in ['uk citizen', 'citizen', 'british']):
                            status_select.select_by_visible_text(option.text)
                            break
            
            # CV handling - check if CV is already selected
            cv_handled = self.handle_cv_selection()
            
            # Personal information (usually pre-filled)
            first_name_fields = self.driver.find_elements(By.XPATH, 
                "//input[contains(@name, 'first') or contains(@id, 'first')]")
            if first_name_fields and not first_name_fields[0].get_attribute('value'):
                first_name_fields[0].send_keys(self.credentials.first_name)
            
            last_name_fields = self.driver.find_elements(By.XPATH, 
                "//input[contains(@name, 'last') or contains(@id, 'last')]")
            if last_name_fields and not last_name_fields[0].get_attribute('value'):
                last_name_fields[0].send_keys(self.credentials.last_name)
            
            # Submit application
            submit_buttons = self.driver.find_elements(By.XPATH, 
                "//button[contains(text(), 'Apply') or @type='submit']")
            
            if submit_buttons:
                self.driver.execute_script("arguments[0].click();", submit_buttons[0])
                time.sleep(3)
                
                # Check for success indicators
                if self.check_application_success():
                    result.status = "success"
                    result.company = self.extract_company_name()
                    result.reference = self.extract_reference_number()
                    self.logger.info(f"Successfully applied to: {result.job_title}")
                    
                    # Verify application appears in history
                    verification_result = self.verify_application_in_history(result.job_title)
                    if verification_result:
                        result.status = "verified"
                        self.logger.info(f"Application verified in history: {result.job_title}")
                    else:
                        self.logger.warning(f"Application not found in history: {result.job_title}")
                else:
                    result.status = "failed"
                    result.error_message = "Application submission may have failed"
            else:
                result.status = "failed"
                result.error_message = "No submit button found"
            
            return result
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            self.logger.error(f"Error filling application form: {str(e)}")
            return result
    
    def handle_cv_selection(self) -> bool:
        """Handle CV selection from existing stored CVs"""
        try:
            # Look for CV dropdown or existing CV indication
            cv_selects = self.driver.find_elements(By.XPATH, 
                "//select[contains(@name, 'cv') or contains(@name, 'resume')]")
            
            if cv_selects:
                cv_select = Select(cv_selects[0])
                # Select the first available CV (not "No file chosen")
                for option in cv_select.options[1:]:  # Skip first option
                    if option.text and "no file" not in option.text.lower():
                        cv_select.select_by_index(option.index)
                        self.logger.info(f"Selected CV: {option.text}")
                        return True
            
            # Check if CV is already selected/shown
            cv_indicators = self.driver.find_elements(By.XPATH, 
                "//text()[contains(., '.pdf') or contains(., 'CV') or contains(., 'resume')]")
            
            if cv_indicators:
                self.logger.info("CV appears to be already selected")
                return True
            
            self.logger.warning("No CV selection found, but continuing")
            return True
            
        except Exception as e:
            self.logger.warning(f"CV handling error: {str(e)}")
            return True  # Continue anyway
    
    def check_application_success(self) -> bool:
        """Check if application was submitted successfully"""
        success_indicators = [
            "application submitted",
            "thank you",
            "successfully applied",
            "application received",
            "confirmation"
        ]
        
        try:
            page_text = self.driver.page_source.lower()
            for indicator in success_indicators:
                if indicator in page_text:
                    return True
            
            # Check for success elements
            success_elements = self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'success') or contains(@class, 'confirm')]")
            
            return len(success_elements) > 0
            
        except:
            return False
    
    def extract_company_name(self) -> str:
        """Extract company name from the page"""
        try:
            company_elements = self.driver.find_elements(By.XPATH, 
                "//span[contains(@class, 'company')] | //div[contains(@class, 'company')]")
            if company_elements:
                return company_elements[0].text.strip()
            return ""
        except:
            return ""
    
    def extract_reference_number(self) -> str:
        """Extract job reference number from the page"""
        try:
            ref_elements = self.driver.find_elements(By.XPATH, 
                "//span[contains(@class, 'reference')] | //div[contains(@class, 'ref')]")
            if ref_elements:
                return ref_elements[0].text.strip()
            return ""
        except:
            return ""
    
    def verify_application_in_history(self, job_title: str) -> bool:
        """Verify that the application appears in the application history"""
        try:
            self.logger.info(f"Verifying application in history for: {job_title}")
            
            # First try the direct applications URL
            original_url = self.driver.current_url
            self.driver.get("https://www.jobserve.com/ee/en/can/applications")
            time.sleep(3)
            
            # Check if we can access the applications page
            page_source = self.driver.page_source.lower()
            
            # If we get a limited features message, try alternative verification
            if "limited number of features" in page_source:
                self.logger.info("Applications page has limited access, trying alternative verification")
                return self.verify_via_job_search(job_title)
            
            # Look for the job title in the applications history
            job_title_lower = job_title.lower()
            job_title_variations = [
                job_title_lower,
                job_title_lower.replace(" ", ""),
                job_title_lower.split(" - ")[0] if " - " in job_title_lower else job_title_lower,
                job_title_lower.split(" (")[0] if " (" in job_title_lower else job_title_lower
            ]
            
            # Check if any variation appears in the page
            for variation in job_title_variations:
                if variation in page_source:
                    self.logger.info(f"Found job title variation '{variation}' in application history")
                    return True
            
            # Check for today's date as indication of recent application
            today = datetime.now().strftime("%d/%m/%Y")
            today_alt = datetime.now().strftime("%Y-%m-%d")
            
            if today in page_source or today_alt in page_source:
                self.logger.info("Found today's date in applications, likely indicating recent application")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying application in history: {str(e)}")
            return False
        finally:
            # Return to original page
            try:
                self.driver.get(original_url)
                time.sleep(2)
            except:
                pass
    
    def verify_via_job_search(self, job_title: str) -> bool:
        """Alternative verification via job search results"""
        try:
            # Go back to job search to look for "APPLIED" status
            self.driver.get("https://www.jobserve.com/gb/en/JobSearch.aspx")
            time.sleep(3)
            
            page_source = self.driver.page_source.lower()
            
            # Look for "applied" indicators
            if "applied:" in page_source or "applied " in page_source:
                self.logger.info("Found 'APPLIED' status in job search results")
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Alternative verification failed: {str(e)}")
            return False
    
    def run_automation(self):
        """Main automation workflow"""
        try:
            self.setup_driver()
            self.navigate_to_jobserve()
            self.login()
            self.search_jobs()
            
            jobs = self.get_job_listings()
            
            if not jobs:
                self.logger.warning("No suitable jobs found")
                return
            
            for i, job in enumerate(jobs):
                if len(self.applications_submitted) >= self.search_criteria.max_applications:
                    break
                
                self.logger.info(f"Applying to job {i+1}/{len(jobs)}: {job['title']}")
                result = self.apply_to_job(job)
                self.applications_submitted.append(result)
                
                # Add delay between applications
                time.sleep(5)
            
            self.save_results()
            successful_apps = len([r for r in self.applications_submitted if r.status in ['success', 'verified']])
            self.logger.info(f"Automation completed. Applied to {successful_apps} jobs successfully.")
            
        except Exception as e:
            self.logger.error(f"Automation failed: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_results(self):
        """Save application results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        csv_filename = f"job_applications_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['job_title', 'company', 'reference', 'status', 'error_message', 'application_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for app in self.applications_submitted:
                writer.writerow({
                    'job_title': app.job_title,
                    'company': app.company,
                    'reference': app.reference,
                    'status': app.status,
                    'error_message': app.error_message,
                    'application_date': app.application_date
                })
        
        # Save to JSON
        json_filename = f"job_applications_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump([app.__dict__ for app in self.applications_submitted], jsonfile, indent=2)
        
        self.logger.info(f"Results saved to {csv_filename} and {json_filename}")


def main():
    """Main function for testing"""
    from config import *
    
    credentials = UserCredentials(
        email=JOBSERVE_EMAIL,
        password=JOBSERVE_PASSWORD,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        cv_path=CV_PATH
    )
    
    search_criteria = JobSearchCriteria(
        keywords=SEARCH_KEYWORDS,
        location=SEARCH_LOCATION,
        max_applications=2  # Test mode
    )
    
    automation = JobServeAutomation(credentials, search_criteria, headless=True)
    automation.run_automation()


if __name__ == "__main__":
    main()

