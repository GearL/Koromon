Koromon
=====
CMS based on Flask

## Quick Start

#### 1. Install pip
`sudo apt-get install python-pip`

#### 2. Create virtual environment
`virtualenv env`

#### 3. Activate virtual environment
`source ./env/bin/activate`

#### 4. Install dependencies of Koromon
`pip install -r requirements.txt`

#### 5. Copy example config and set local config
`cp .env.sample .env`

edit `.env` according to your environment

#### 6. Start server
`honcho run python manage.py runserver --port [your port]`
