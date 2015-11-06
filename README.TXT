--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
RUNNING ALL TESTS 
git clone https://github.com/william-zt-ho/eLocal.git
cd eLocal
pip install -r requirements.txt
------Please make sure latest version of Firefox is installed in computer-------
rm -rf cover .coverage */*.pyc */__pycache__
python manage.py test
python eLocal_app/tests/ui_tests.py (To only run the UI tests, and can see print messages in terminal of tests run)
--------------------------------------------------------------------------------
*Note:The first time running the above command, sometimes it causes a Selenium webdriver exception saying that "selenium.common.exceptions.WebDriverException: Message: Can't load the profile. Profile Dir: %s If you specified a log_file in the FirefoxBinary constructor, check it for details." The second or third time running the above command should execute the tests. 
--------------------------------------------------------------------------------


Setting up Postgres on Mac:
psql -d postgres
    CREATE ROLE elocal LOGIN;
    ALTER ROLE elocal PASSWORD 'elocal123';
    ALTER ROLE elocal CREATEDB;
    CREATE DATABASE elocal OWNER elocal;
    \q

Setting up Postgres on Windows:
    (haven't tried yet, sorry)

Setting up Postgres on Linux:
sudo -u postgres psql
    CREATE ROLE elocal LOGIN;
    ALTER ROLE elocal PASSWORD 'elocal123';
    ALTER ROLE elocal CREATEDB;
    CREATE DATABASE elocal OWNER elocal;
    \q