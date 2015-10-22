
Setting up Postgres on Mac:
psql -d postgres
    CREATE ROLE elocal LOGIN;
    ALTER ROLE elocal PASSWORD 'elocal123';
    CREATE DATABASE elocal OWNER elocal;
    \q

Setting up Postgres on Windows:
    (haven't tried yet, sorry)

Setting up Postgres on Linux:
sudo -u postgres psql
    CREATE ROLE elocal LOGIN;
    ALTER ROLE elocal PASSWORD 'elocal123';
    CREATE DATABASE elocal OWNER elocal;
    \q