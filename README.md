# Receipt
A simple frontend app and API to get information about fiscal checks in Russian federation by its fiscal data or just by QR codes from them.

Requirements are:
- Poetry
- Python
- Postgresql

Tech stack are:
- FastAPI
- Alembic
- Sqalchemy
- Pydantic

### Images

| ![Root page](<img/Receipts - Root page.png>) | ![Parsed data](<img/Receipts - Parsed data.png>) | ![Docs](<img/Receipts - Docs.png>) |
|-|-|-|

### API
Docs available on `/docs`, main page on `/` route. FastAPI tries to serve all static files from `static` dir, but it's recommended to use Nginx on deploy.

### Installation and launch
To prepare system to work, just create the `.env` file with system settings and run the poetry dependency installation.

```sh
# Create enviroment
cp .env.example .env
vim .env

# Install dependencies
poetry python install 3.14
poetry install

# Init database and migrate it
sudo -u postgres psql -c "CREATE DATABASE receipts;"
poetry run alembic upgrade head
```

To run the application itself, simply launch the main.py script.

```sh
poetry run python main.py
```

Also to run camera on you phone via LAN on testing, you should install additional SSL certificates to make this thing work. To do so just make this via openssl:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

If you do so, just ensure then, that you open an `https` version of a site (`http` now will give an disconnection error). Browser will tel you once that this SSL sertfiticate is not trusted, but you may still use the app and launch a camera for testing.
