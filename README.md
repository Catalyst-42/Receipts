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


### API
Docs available on `/docs`, main page on `/` route.

### Launch
To prepare system to work, just create the `.env` file with system settings and run the poetry dependency installation.

```sh
cp .env.example .env
poetry install
```

To run the application itself, simply launch the main.py script.

```sh
poetry run python main.py
```
