A light python scraper for jobs on Indeed.

Requirements:
* Download and install firefox (https://www.mozilla.org/en-CA/firefox/new/).
* Download and install geckodriver from their github releases page (https://github.com/mozilla/geckodriver/releases).
* Put geckodriver.exe's folder in the path environment variable.
* Add scrapy settings to environment variable (in this setup -  SCRAPY_SETTINGS_MODULE: scraper.scraper.settings)

Tips:
* For vsCoders, activate pylance basic type checking from settings

Usage:
* To use, navigate to the spider file and launch the vscode debugger for scrapy spider