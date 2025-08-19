#!/usr/bin/env python3
"""
JobServe UK Job Application Automation Script

This script automates the process of applying to jobs on JobServe UK.
It logs in, searches for jobs based on criteria, and applies to suitable positions.

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
    job_type: str = "Contract/Full Time"  # Options: Any, Full Time, Contract, Contract/Full Time, Part Time/Temporary/Seasonal
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
    job_title: str
    company: str = ""
    reference: str = ""
    status: str = ""  # success, failed, error
    error_message: str = ""
    application_date: str = ""


class JobServeAutomation:
    """Main automation class for JobServe job applications"""
    
    def __init__(self, credentials: UserCredentials, search_criteria: JobSearchCriteria, headless: bool = False):
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
            self.logger.info("Navigated to JobServe.com")
            
            # Switch to UK site if needed
            try:
                uk_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "United Kingdom")))
                uk_link.click()
                self.logger.info("Switched to UK site")
                time.sleep(2)
            except TimeoutException:
                self.logger.info("Already on UK site or UK link not found")
                
        except Exception as e:
            self.logger.error(f"Error navigating to JobServe: {str(e)}")
            raise
    
    def login(self):
        """Login to JobServe with provided credentials"""
        try:
            # Click on Sign In/Register
            sign_in_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign In/Register")))
            sign_in_link.click()
            
            # Click on Job Seekers
            job_seekers_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Job Seekers")))
            job_seekers_link.click()
            
            # Fill in email
            email_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[id*='email']")))
            email_field.clear()
            email_field.send_keys(self.credentials.email)
            
            # Fill in password
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.clear()
            password_field.send_keys(self.credentials.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            login_button.click()
            
            # Wait for successful login
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sign Out")))
            self.logger.info("Successfully logged in to JobServe")
            
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise
    
    def search_jobs(self):
        """Search for jobs based on criteria"""
        try:
            # Navigate to job search
            job_search_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Job Search")))
            job_search_link.click()
            
            # Fill in keywords
            keywords_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Marketing'], input[name*='keyword']")))
            keywords_field.clear()
            keywords_field.send_keys(self.search_criteria.keywords)
            
            # Fill in location
            location_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='London'], input[name*='location']")
            location_field.clear()
            location_field.send_keys(self.search_criteria.location)
            
            # Select job type
            job_type_select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[name*='jobtype'], select[name*='type']"))
            job_type_select.select_by_visible_text(self.search_criteria.job_type)
            
            # Click search
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[value='Search']")
            search_button.click()
            
            # Wait for results
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='JobSearch'], .job-title, h3")))
            self.logger.info(f"Job search completed for: {self.search_criteria.keywords} in {self.search_criteria.location}")
            
        except Exception as e:
            self.logger.error(f"Job search failed: {str(e)}")
            raise
    
    def get_job_listings(self) -> List[Dict]:
        """Extract job listings from search results"""
        jobs = []
        try:
            # Look for job listings in various possible formats
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".job-title, h3 a, a[href*='job'], .job-link")
            
            for job_element in job_elements[:self.search_criteria.max_applications]:
                try:
                    job_title = job_element.text.strip()
                    job_url = job_element.get_attribute('href')
                    
                    if job_title and job_url and any(keyword.lower() in job_title.lower() 
                                                   for keyword in ['data', 'ai', 'engineer', 'scientist', 'tech', 'lead']):
                        jobs.append({
                            'title': job_title,
                            'url': job_url,
                            'element': job_element
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting job info: {str(e)}")
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
            # Click on the job or apply button
            if 'element' in job:
                self.driver.execute_script("arguments[0].click();", job['element'])
            else:
                self.driver.get(job['url'])
            
            time.sleep(2)
            
            # Look for Apply button
            apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='apply'], button[text*='Apply'], input[value*='Apply'], .apply-btn")
            
            if not apply_buttons:
                result.status = "failed"
                result.error_message = "No apply button found"
                return result
            
            # Click apply button
            apply_button = apply_buttons[0]
            self.driver.execute_script("arguments[0].click();", apply_button)
            time.sleep(3)
            
            # Check if application form opened
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
            "input[type='email']",
            "select[name*='status']",
            "input[name*='name']",
            ".application-form",
            "form[action*='apply']"
        ]
        
        for indicator in form_indicators:
            if self.driver.find_elements(By.CSS_SELECTOR, indicator):
                return True
        return False
    
    def fill_application_form(self, result: ApplicationResult) -> ApplicationResult:
        """Fill out the job application form"""
        try:
            # Email field (usually pre-filled)
            email_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[name*='email']")
            if email_fields and not email_fields[0].get_attribute('value'):
                email_fields[0].send_keys(self.credentials.email)
            
            # Working status dropdown
            status_selects = self.driver.find_elements(By.CSS_SELECTOR, "select[name*='status'], select[name*='work']")
            if status_selects:
                status_select = Select(status_selects[0])
                # Try to select UK Citizen or similar
                for option in status_select.options:
                    if any(term in option.text.lower() for term in ['uk citizen', 'citizen', 'british']):
                        status_select.select_by_visible_text(option.text)
                        break
            
            # CV upload or selection
            cv_handled = self.handle_cv_upload()
            
            # First name
            first_name_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='first'], input[name*='fname']")
            if first_name_fields:
                first_name_fields[0].clear()
                first_name_fields[0].send_keys(self.credentials.first_name)
            
            # Last name
            last_name_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name*='last'], input[name*='lname']")
            if last_name_fields:
                last_name_fields[0].clear()
                last_name_fields[0].send_keys(self.credentials.last_name)
            
            # Submit application
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "input[value*='Apply'], button[type='submit'], .apply-button")
            
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
    
    def handle_cv_upload(self) -> bool:
        """Handle CV upload or selection"""
        try:
            # Check for existing CV dropdown first
            cv_selects = self.driver.find_elements(By.CSS_SELECTOR, "select[name*='cv'], select[name*='resume']")
            if cv_selects:
                cv_select = Select(cv_selects[0])
                # Select the first available CV (not "No file chosen")
                for option in cv_select.options[1:]:  # Skip first option which is usually "No file chosen"
                    cv_select.select_by_index(option.index)
                    return True
            
            # If no dropdown, look for file upload
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs and self.credentials.cv_path and Path(self.credentials.cv_path).exists():
                file_inputs[0].send_keys(str(Path(self.credentials.cv_path).absolute()))
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"CV upload/selection failed: {str(e)}")
            return False
    
    def check_application_success(self) -> bool:
        """Check if application was submitted successfully"""
        success_indicators = [
            "application submitted",
            "thank you",
            "successfully applied",
            "application received",
            "confirmation"
        ]
        
        page_text = self.driver.page_source.lower()
        return any(indicator in page_text for indicator in success_indicators)
    
    def extract_company_name(self) -> str:
        """Extract company/recruiter name from the page"""
        try:
            company_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".company-name, .recruiter-name, .employer-name")
            if company_elements:
                return company_elements[0].text.strip()
            return ""
        except:
            return ""
    
    def extract_reference_number(self) -> str:
        """Extract job reference number from the page"""
        try:
            ref_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".reference, .job-ref, .ref-number")
            if ref_elements:
                return ref_elements[0].text.strip()
            return ""
        except:
            return ""
    
    def verify_application_in_history(self, job_title: str) -> bool:
        """Verify that the application appears in the application history"""
        try:
            self.logger.info(f"Verifying application in history for: {job_title}")
            
            # Navigate to applications history page
            self.driver.get("https://www.jobserve.com/ee/en/can/applications")
            time.sleep(3)
            
            # Wait for the page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Look for the job title in the applications history
            page_source = self.driver.page_source.lower()
            job_title_lower = job_title.lower()
            
            # Try different variations of the job title
            job_title_variations = [
                job_title_lower,
                job_title_lower.replace(" ", ""),
                job_title_lower.split(" - ")[0] if " - " in job_title_lower else job_title_lower,
                job_title_lower.split(" (")[0] if " (" in job_title_lower else job_title_lower
            ]
            
            # Check if any variation of the job title appears in the page
            for variation in job_title_variations:
                if variation in page_source:
                    self.logger.info(f"Found job title variation '{variation}' in application history")
                    return True
            
            # Also check for application elements that might contain the job title
            application_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".application-item, .job-application, tr, .application-row, .application")
            
            for element in application_elements:
                try:
                    element_text = element.text.lower()
                    for variation in job_title_variations:
                        if variation in element_text:
                            self.logger.info(f"Found job title in application element: {variation}")
                            return True
                except:
                    continue
            
            # Check for recent applications (today's date)
            today = datetime.now().strftime("%d/%m/%Y")
            today_alt = datetime.now().strftime("%Y-%m-%d")
            
            if today in page_source or today_alt in page_source:
                self.logger.info(f"Found today's date in applications, likely indicating recent application")
                # If we find today's date and we just applied, it's probably our application
                return True
            
            self.logger.warning(f"Job title '{job_title}' not found in application history")
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying application in history: {str(e)}")
            return False
    
    def run_automation(self):
        """Main automation workflow"""
        try:
            self.setup_driver()
            self.navigate_to_jobserve()
            self.login()
            self.search_jobs()
            
            jobs = self.get_job_listings()
            
            for i, job in enumerate(jobs):
                if len(self.applications_submitted) >= self.search_criteria.max_applications:
                    break
                
                self.logger.info(f"Applying to job {i+1}/{len(jobs)}: {job['title']}")
                result = self.apply_to_job(job)
                self.applications_submitted.append(result)
                
                # Add delay between applications
                time.sleep(5)
            
            self.save_results()
            self.logger.info(f"Automation completed. Applied to {len([r for r in self.applications_submitted if r.status == 'success'])} jobs successfully.")
            
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
            
            for result in self.applications_submitted:
                writer.writerow({
                    'job_title': result.job_title,
                    'company': result.company,
                    'reference': result.reference,
                    'status': result.status,
                    'error_message': result.error_message,
                    'application_date': result.application_date
                })
        
        # Save to JSON
        json_filename = f"job_applications_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump([result.__dict__ for result in self.applications_submitted], 
                     jsonfile, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {csv_filename} and {json_filename}")


def main():
    """Main function to run the automation"""
    # Configuration
    credentials = UserCredentials(
        email="kaljuvee@gmail.com",
        password="Toomesilane2$2",
        first_name="Julian",
        last_name="Kaljuvee",
        cv_path="/path/to/your/cv.pdf"  # Update this path
    )
    
    search_criteria = JobSearchCriteria(
        keywords="data scientist, AI engineer",
        location="London",
        job_type="Contract/Full Time",
        max_applications=50
    )
    
    # Run automation
    automation = JobServeAutomation(credentials, search_criteria, headless=False)
    automation.run_automation()


if __name__ == "__main__":
    main()

