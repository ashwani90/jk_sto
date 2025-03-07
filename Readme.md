## Install the project

```
python -m venv .env
pip install -r requirements.txt

```

### To Run The project

```
source .env/bin/activate
python manage.pyn runserver
```

### Commands

#### Financial Data command

```
# Download and save financial
python manage.py download_and_save_financials

# Download financial Data
python manage.py download_financial_data

# download financial info
python manage.py download_financial_info

# get company Events
python manage.py get_company_events
```