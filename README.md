# Receipts
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

To run the application itself, simply launch the `main.py` script.

```sh
poetry run python main.py
```

Also to run camera on you phone via LAN on testing, you should install additional SSL certificates to make this thing work. To do so just make this via openssl:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

If you do so, just ensure then, that you open an `https` version of a site (`http` now will give an disconnection error). Browser will tel you once that this SSL sertfiticate is not trusted, but you may still use the app and launch a camera for testing.

```sh
open https://localhost:8800/
open https://localhost:8800/docs/
```


-- 1. Сырые данные от API
CREATE TABLE crpt (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dump JSONB NOT NULL
);

-- 2. Компании (продавцы)
CREATE TABLE retailers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inn VARCHAR(12) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    is_individual BOOLEAN GENERATED ALWAYS AS (length(inn) = 12) STORED
);

-- 3. Магазины (точки продаж)
CREATE TABLE shops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    retailer_id UUID NOT NULL REFERENCES retailers(id) ON DELETE CASCADE,
    address TEXT NOT NULL,
    UNIQUE(retailer_id, address)
);

-- 4. Сотрудники (кассиры)
CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shop_id UUID NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    UNIQUE(shop_id, name)
);

-- 5. Чеки (только 5 ключей + связи)
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crpt_id UUID NOT NULL UNIQUE REFERENCES crpt(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    t TIMESTAMP NOT NULL,
    s NUMERIC(15,2) NOT NULL,
    fn BIGINT NOT NULL,
    i INTEGER NOT NULL,
    fp BIGINT NOT NULL,
    n SMALLINT NOT NULL
);

-- 6. Товарные позиции
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    receipt_id UUID NOT NULL REFERENCES receipts(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    price NUMERIC(15,2) NOT NULL,
    quantity NUMERIC(15,3) NOT NULL,
    total NUMERIC(15,2) NOT NULL,
    measure_code SMALLINT,
    nds_code SMALLINT,
    payment_type_code SMALLINT,
    product_type_code SMALLINT
);

-- 7. Справочник ставок НДС
CREATE TABLE nds_rates (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL,
    rate NUMERIC(5,2)
);

-- 8. Справочник единиц измерения
CREATE TABLE measure_units (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Индексы
CREATE INDEX idx_receipts_fn ON receipts(fn);
CREATE INDEX idx_receipts_t ON receipts(t);
CREATE INDEX idx_receipts_employee ON receipts(employee_id);
CREATE INDEX idx_receipts_all_keys ON receipts(fn, i, fp, n, t);
CREATE INDEX idx_items_receipt ON items(receipt_id);
CREATE INDEX idx_items_name ON items(name);
CREATE INDEX idx_shops_retailer ON shops(retailer_id);
CREATE INDEX idx_employees_shop ON employees(shop_id);
CREATE INDEX idx_retailers_inn ON retailers(inn);

-- Начальные данные для справочников (актуальные по ФНС)
INSERT INTO nds_rates (id, name, rate) VALUES
(1, 'НДС 20%', 20),
(2, 'НДС 10%', 10),
(3, 'НДС 20/120', 20),
(4, 'НДС 10/110', 10),
(5, 'НДС 0%', 0),
(6, 'НДС не облагается', NULL),
(7, 'НДС 5%', 5),
(8, 'НДС 7%', 7),
(9, 'НДС 5/105', 5),
(10, 'НДС 7/107', 7),
(11, 'НДС 22%', 22),
(12, 'НДС 22/122', 22);

INSERT INTO measure_units (id, name) VALUES
(0, 'piece'),
(10, 'gram'),
(11, 'kilogram'),
(12, 'tonne'),
(20, 'centimeter'),
(21, 'decimeter'),
(22, 'meter'),
(30, 'square_centimeter'),
(31, 'square_decimeter'),
(32, 'square_meter'),
(40, 'milliliter'),
(41, 'liter'),
(42, 'cubic_meter'),
(50, 'kilowatt_hour'),
(51, 'gigacalorie'),
(70, 'day'),
(71, 'hour'),
(72, 'minute'),
(73, 'second'),
(80, 'kilobyte'),
(81, 'megabyte'),
(82, 'gigabyte'),
(83, 'terabyte'),
(255, 'other');