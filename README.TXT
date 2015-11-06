--------------------------------------------------------------------------------
RUNNING USER INTERFACE TESTS 
git clone https://github.com/william-zt-ho/eLocal.git
cd eLocal
pip install -r requirements.txt
--Please make sure latest version of Firefox is installed in computer
python manage.py eLocal_app/tests/ui_tests.py

RUNNING CODE COVERAGE 
python manage.py test

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