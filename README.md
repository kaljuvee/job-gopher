# JobServe UK Job Application Automation

An automated Python script for applying to jobs on JobServe UK. This tool can search for jobs based on your criteria and automatically submit applications using your CV and personal details.

## Features

- 🔍 **Smart Job Search**: Search for jobs using keywords, location, and job type filters
- 🤖 **Automated Applications**: Automatically fill out and submit job applications
- 📄 **CV Management**: Upload or select existing CVs from your JobServe profile
- 📊 **Results Tracking**: Save application results to CSV and JSON files
- 🛡️ **Error Handling**: Robust error handling with detailed logging
- ⚙️ **Configurable**: Easy configuration through config files
- 🧪 **Test Mode**: Test with limited applications before full automation

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- JobServe UK account
- CV file in PDF format

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kaljuvee/job-gopher.git
   cd job-gopher
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver** (if not already installed):
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # On macOS with Homebrew
   brew install chromedriver
   
   # Or use webdriver-manager (automatic)
   pip install webdriver-manager
   ```

## Configuration

1. **Update your credentials** in `config.py`:
   ```python
   JOBSERVE_EMAIL = "your_email@jobserve.com"
   JOBSERVE_PASSWORD = "your_password"
   CV_PATH = "/path/to/your/cv.pdf"
   ```

2. **Customize search criteria**:
   ```python
   SEARCH_KEYWORDS = "data scientist, AI engineer"
   SEARCH_LOCATION = "London"
   JOB_TYPE = "Contract/Full Time"
   MAX_APPLICATIONS = 50
   ```

3. **Optional: Use environment variables**:
   ```bash
   export JOBSERVE_EMAIL="your_email@jobserve.com"
   export JOBSERVE_PASSWORD="your_password"
   export CV_PATH="/path/to/your/cv.pdf"
   ```

## Usage

### Basic Usage

```bash
# Run the automation with default settings
python run_automation.py
```

### Test Mode (Recommended First)

```bash
# Test with only 2 applications
python run_automation.py --test
```

### Headless Mode

```bash
# Run without opening browser window
python run_automation.py --headless
```

### Custom Application Limit

```bash
# Apply to maximum 10 jobs
python run_automation.py --max-apps 10
```

## Output Files

The script generates several output files:

- `job_applications_YYYYMMDD_HHMMSS.csv` - Application results in CSV format
- `job_applications_YYYYMMDD_HHMMSS.json` - Application results in JSON format
- `jobserve_automation.log` - Detailed execution log

## Configuration Options

### Job Search Criteria

| Setting | Description | Options |
|---------|-------------|---------|
| `SEARCH_KEYWORDS` | Job search keywords | e.g., "data scientist, AI engineer" |
| `SEARCH_LOCATION` | Job location | e.g., "London", "Manchester" |
| `JOB_TYPE` | Type of employment | "Any", "Full Time", "Contract", "Contract/Full Time" |
| `MAX_APPLICATIONS` | Maximum applications to submit | Integer (e.g., 50) |

### Personal Information

| Setting | Description |
|---------|-------------|
| `FIRST_NAME` | Your first name |
| `LAST_NAME` | Your last name |
| `CV_PATH` | Path to your CV file |

### Automation Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `HEADLESS_MODE` | Run browser in background | `False` |
| `DELAY_BETWEEN_APPLICATIONS` | Delay between applications (seconds) | `5` |
| `TIMEOUT_SECONDS` | Page load timeout | `10` |

## How It Works

1. **Login**: Authenticates with JobServe UK using your credentials
2. **Search**: Searches for jobs matching your criteria
3. **Filter**: Filters jobs based on priority and exclude keywords
4. **Apply**: For each suitable job:
   - Opens the job application form
   - Fills in your personal details
   - Uploads or selects your CV
   - Submits the application
5. **Track**: Records application results and saves to files

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   ```bash
   pip install webdriver-manager
   ```

2. **Login fails**:
   - Check your JobServe credentials
   - Ensure your account is not locked
   - Try logging in manually first

3. **CV upload fails**:
   - Ensure CV file exists at the specified path
   - Check file permissions
   - Try uploading CV to JobServe manually first

4. **CAPTCHA appears**:
   - The script will log this and skip the application
   - Consider running in non-headless mode to solve CAPTCHAs manually

### Debug Mode

Run with debug logging:
```python
# In config.py
LOG_LEVEL = "DEBUG"
```

## Legal and Ethical Considerations

- ⚖️ **Terms of Service**: Ensure compliance with JobServe's Terms of Service
- 🤝 **Rate Limiting**: The script includes delays to be respectful to the website
- 📧 **Quality Applications**: Only apply to jobs you're genuinely interested in
- 🔒 **Data Privacy**: Your credentials are only used for authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with JobServe's Terms of Service
- Ensuring applications are relevant and appropriate
- Monitoring application results and following up professionally

The authors are not responsible for any misuse of this tool or any consequences arising from its use.

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the log files
3. Open an issue on GitHub with:
   - Error message
   - Log file excerpt
   - Steps to reproduce

## Changelog

### v1.0.0 (2025-08-19)
- Initial release
- Basic job search and application functionality
- CSV/JSON result export
- Configuration system
- Test mode support

