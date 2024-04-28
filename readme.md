# Medication Renewal Automation Script

This script automates the process of renewing medication prescriptions through 1177, handling authentication via BankID and submitting requests for medication renewals. 

## Prerequisites

- Python 3.x
- Selenium WebDriver
- Google Chrome and ChromeDriver

## Setup on Arch Linux

1. **Install Python and Selenium**:
   Ensure Python 3 is installed. You can install Python and Selenium WebDriver using pip:
   ```bash
   sudo pacman -Syu python python-pip
   pip install selenium
   ```
2. **Install Chromedriver**
   ```bash
   sudo pacman -S chromedriver
   ```
   or yay for the latest veriosn
   ```bash
   yay -S chromedriver
   ```
3. Configuration:
Store the URL and any necessary configurations in a separate config.py file (you need to create this). Example configuration:



# Usage
1. **Setting the Link Address:** The script requires a specific URL to function:
- Navigate to the **Vårdval/mottagningar section on the website.**
- Click on **Förnya recept.**
- Right-click and select **Copy link address.**
- Set this address to the **LINK_ADDRESS** in your `config.py` file.
2. **Running the Script:**
Execute the script from your terminal:

# Automation with Cron
To run this script automatically, such as once a month, you can use cron on Linux:

Open your crontab:
```bash
crontab -e
```
Add a cron job that runs the script monthly. Modify the path to where your script is located:

```cron
0 0 1 * * /usr/bin/python /path/to/your/main.py
```
This cron job will execute the script at midnight on the first day of every month. But i guess you have to be awake, since you have to log in with bankid