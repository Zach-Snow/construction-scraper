# construction-scraper
This is a Flask application that would scrap project data for 3 customers for ALASCO.
Namely, GARBE Immobilien-Projekte, BRAND BERGER real estate consulting and Rosa-Alscher Gruppe.
The Flask app has to be run in Windows environment as the selenium webdriver might create conflict with WSL or native Linux environment.
Chrome driver needs to be configured before running.

## Relevant Commands

`python -m venv venv` To create a virtual Environment named venv.

`venv\Scripts\activate` To activate the venv.

`python -m pip install --upgrade pip` To upgrade pip version.

`pip install -r requirements.txt` To install packages from requirements text file.

`python app.py` To initiate the flask app.
