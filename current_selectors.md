# Current JobServe Element Selectors - August 2025

## Navigation Elements
- Job Search Link: `a[href*="JobSearch.aspx"]` or text "Job Search"
- My Account: `a` with text "My Account"
- Applications: `a` with text "Applications"

## Job Search Page
- URL: `https://www.jobserve.com/gb/en/JobSearch.aspx`
- Apply Button: `a` with text "Apply" (appears for each job listing)
- Job Titles: `a` with class containing job title links
- Contract Filter: Input checkboxes for job types

## Application Form (Modal Dialog)
- Modal Title: "Job Application"
- Email Field: `input` with value pre-filled (kaljuvee@gmail.com)
- Working Status: `select` dropdown (UK Citizen selected)
- CV Attachment: Shows existing CV "kaljuvee-julian-ds-long-2025 [18 Aug 2025]"
- CV File Input: "Choose File" button for CV upload
- Covering Letter: Optional text area
- First Name: `input` field (pre-filled: Julian)
- Last Name: `input` field (pre-filled: Kaljuvee)
- Address: `textarea` field
- Country: `input` field (United Kingdom)
- Phone Fields: Home Telephone, Mobile/Cell
- Apply Button: Blue "Apply" button to submit

## Key Observations
1. User is already logged in as "Julian Kaljuvee"
2. CV is already stored and available for selection
3. Personal information is pre-filled
4. Application form opens in modal dialog
5. Working status defaults to "UK Citizen"
6. Email confirmation checkbox available

## Application History
- URL: `https://www.jobserve.com/ee/en/can/applications` (has access limitations)
- Alternative: Check job search results for "APPLIED" status indicators

## Current Job Search Results
- 401 jobs found for "data scientist, AI engineer"
- 385 contract positions available
- Jobs show apply buttons and status indicators
- Applied jobs show timestamps (e.g., "APPLIED: 18/08/2025 21:10:19")

