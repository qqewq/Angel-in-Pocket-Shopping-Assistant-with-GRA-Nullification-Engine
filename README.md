https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
https://doi.org/10.5281/zenodo.20848755
--------------
# Angel-in-Pocket Shopping Assistant with GRA Nullification Engine  
# Ангел в Кармане: шопинг-ассистент с GRA-движком обнуления

English | [Русский](#русский)

---

## English

### Overview

**Angel-in-Pocket Shopping Assistant with GRA Nullification Engine** is an AI-powered shopping assistant that protects users from hostile sellers, fake reviews, and risky products by analyzing a **graph of interactions** and applying the **GRA‑Nullification‑Equilibrium** engine.

The system combines:

- A **graph-based trust engine** (NetworkX + NumPy)
- A **GRA equilibrium module** to propagate and nullify “adversarial suspicion”
- A **FastAPI backend** with JWT auth and PostgreSQL
- **Stripe-based subscriptions** (Basic / Premium / Enterprise) to unlock deeper risk analysis
- Optional **Celery+Redis** background tasks for recalculation

This repository is the reference integration of a GRA‑based trust engine into a real shopping assistant.

---

### Key Features

- **GRA Trust Engine**
  - Builds a local graph around a product: product → seller → reviews → users
  - Assigns initial suspicion scores based on price, rating extremes, account age, sentiment, etc.
  - Runs **GRA-style equilibrium** to compute an adversarial score per node
  - Applies a **nullification cascade** that propagates and dampens risk through the graph

- **Per-Product Safety Score**
  - `/products/{id}/safety` returns:
    - `trust_score` (0–1, higher is safer)
    - `adversarial_degree` (how “hostile” the environment looks)
    - For Premium/Enterprise: seller trust and suspicious review count

- **Seller Trust Estimation**
  - `/sellers/{id}/trust` aggregates product-level trust scores
  - Uses the same GRA engine under the hood

- **Subscription Tiers (Stripe)**
  - `free` — no access to detailed safety scores
  - `basic` — access to product safety with shallow graph depth
  - `premium` — deeper graph analysis and seller metrics
  - `enterprise` — maximum depth and richer risk context

---

### Architecture

```text
Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-/
├── gra_engine/
│   ├── core.py          # GRANullifier: wrapper over equilibrium + cascade
│   ├── equilibrium.py   # Nash-like equilibrium of suspicion on graph
│   └── cascade.py       # Nullification cascade (risk propagation)
├── app/
│   ├── main.py          # FastAPI app entrypoint
│   ├── config.py        # Settings (DB, Stripe, GRA params)
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # Users, Products, Sellers, Reviews, Subscriptions
│   ├── graph_builder.py # Build product–seller–review–user graph
│   ├── gra_adapter.py   # Glue between app and GRA engine
│   ├── deal_detector.py # High-level safety evaluation logic
│   ├── routers/         # Auth, products, sellers, reviews, subscriptions
│   ├── services/        # Stripe payments, Celery tasks (optional)
│   └── utils/           # Security (hashing, JWT)
├── requirements.txt
├── .env.example
└── README.md
```

---

### GRA Engine in a Nutshell

- **Graph building** (`graph_builder.py`)
  - Each product, seller, review, and user becomes a node.
  - Edges carry relation type and weight (sells, has_review, wrote).
  - Initial suspicion is computed per node (cheap product, new seller, extreme ratings, etc.).

- **Equilibrium** (`equilibrium.py`)
  - Iteratively updates suspicion vector until it converges:
    \[
    s_{t+1}[i] = \mathrm{clip}\big(s_0[i] + \alpha \cdot \sum_j A_{ji} s_t[j], 0, 1\big)
    \]
  - Result: a stable “adversarial degree” per node.

- **Nullification Cascade** (`cascade.py`)
  - Nodes above a threshold trigger a cascade that propagates suspicion.
  - Models how local issues (fake review, shady seller) contaminate the neighborhood.

- **Integration** (`gra_adapter.py`, `deal_detector.py`)
  - `evaluate_product_safety()` returns a human-friendly safety summary:
    - trust score
    - adversarial degree
    - optional seller & review diagnostics (for higher tiers)

---

### Subscription Model

- Stripe is used for subscription management:
  - `/subscriptions/create-checkout-session` creates a checkout session for a plan.
  - `/subscriptions/webhook` receives Stripe events and upgrades/downgrades the user.
- User’s active tier (`free`, `basic`, `premium`, `enterprise`) is stored in the DB and used to:
  - Control **API access** (402 for insufficient tier)
  - Adjust **graph depth** for GRA analysis

---

### Getting Started

#### 1. Clone and install

```bash
git clone https://github.com/qqewq/Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-.git
cd Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-
pip install -r requirements.txt
```

#### 2. Configure environment

Create `.env` based on `.env.example`:

```env
DATABASE_URL=postgresql://angel:secret@localhost/angel_pocket
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
GRA_INFLUENCE_WEIGHT=0.5
GRA_MAX_ITER=20
GRA_EPSILON=0.0001
CELERY_BROKER_URL=redis://localhost:6379/0
```

Run PostgreSQL and Redis locally.

#### 3. Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive docs at:  
`http://localhost:8000/docs`

---

### Core Endpoints

- **Auth**
  - `POST /auth/register` — create user
  - `POST /auth/login` — obtain JWT access token

- **Products**
  - `GET /products/{product_id}/safety` — product safety and trust score  
    (requires at least `basic` tier)

- **Sellers**
  - `GET /sellers/{seller_id}/trust` — aggregated trust across seller’s products

- **Reviews**
  - `POST /reviews/` — create review for a product

- **Subscriptions (Stripe)**
  - `POST /subscriptions/create-checkout-session` — start paid plan checkout
  - `POST /subscriptions/webhook` — Stripe webhook (configure in Stripe dashboard)

---

### Roadmap

- Integrate real **NLP sentiment** model for reviews.
- Plug in full **GRA‑Nullification‑Equilibrium** math from the GRA ecosystem.
- Add **frontend** (web or mobile) on top of this API.
- Extend subscription tiers with usage-based limits and analytics.

---

## Русский

### Обзор

**Angel-in-Pocket Shopping Assistant with GRA Nullification Engine** — это AI‑ассистент для онлайн-шопинга, который защищает пользователя от враждебных продавцов, фейковых отзывов и рискованных товаров. Он анализирует **граф взаимодействий** и применяет движок **GRA‑Nullification‑Equilibrium** для вычисления доверия и «обнуления» подозрительных узлов.

Система сочетает:

- **Графовый движок доверия** (NetworkX + NumPy)
- Модуль **GRA‑равновесия** для распространения и обнуления «подозрительности»
- **FastAPI‑бэкенд** с JWT‑аутентификацией и PostgreSQL
- **Подписки через Stripe** (Basic / Premium / Enterprise) для доступа к более глубокому анализу
- Опциональные фоновый воркер **Celery+Redis** для пересчёта метрик

Этот репозиторий — эталонная интеграция GRA‑движка доверия в реальный шопинг‑ассистент.

---

### Ключевые возможности

- **GRA‑движок доверия**
  - Строит локальный граф вокруг товара: товар → продавец → отзывы → пользователи.
  - Назначает начальные уровни подозрения на основе цены, экстремальных оценок, возраста аккаунта, тональности и т.д.
  - Вычисляет **равновесное подозрение** каждого узла.
  - Запускает **каскад обнуления**, распространяющий и демпфирующий риск по графу.

- **Оценка безопасности товара**
  - `/products/{id}/safety` возвращает:
    - `trust_score` (0–1, выше — безопаснее)
    - `adversarial_degree` (насколько «враждебна» окружайка товара)
    - Для Premium/Enterprise: доверие к продавцу и количество подозрительных отзывов

- **Оценка продавца**
  - `/sellers/{id}/trust` агрегирует доверие к товарам продавца
  - Использует тот же GRA‑движок

- **Уровни подписки (Stripe)**
  - `free` — без доступа к подробным оценкам безопасности
  - `basic` — доступ к safety‑метрике товара с небольшой глубиной графа
  - `premium` — более глубокий анализ и метрики продавца
  - `enterprise` — максимальная глубина и расширенный контекст рисков

---

### Архитектура

```text
Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-/
├── gra_engine/
│   ├── core.py          # GRANullifier: оболочка над равновесием и каскадом
│   ├── equilibrium.py   # «Нэш-подобное» равновесие подозрений на графе
│   └── cascade.py       # Каскад обнуления (распространение риска)
├── app/
│   ├── main.py          # Точка входа FastAPI
│   ├── config.py        # Настройки (БД, Stripe, параметры GRA)
│   ├── database.py      # SQLAlchemy engine и сессия
│   ├── models.py        # Users, Products, Sellers, Reviews, Subscriptions
│   ├── graph_builder.py # Построение графа товар–продавец–отзывы–пользователи
│   ├── gra_adapter.py   # Связка приложения и GRA‑движка
│   ├── deal_detector.py # Логика оценки безопасности
│   ├── routers/         # Auth, products, sellers, reviews, subscriptions
│   ├── services/        # Платежи Stripe, фоновые задачи Celery
│   └── utils/           # Безопасность (хэширование, JWT)
├── requirements.txt
├── .env.example
└── README.md
```

---

### Как работает GRA‑движок

- **Построение графа** (`graph_builder.py`)
  - Каждый товар, продавец, отзыв и пользователь — отдельный узел.
  - Рёбра имеют тип связи и вес (продаёт, имеет отзыв, написал и т.п.).
  - Для каждого узла считается начальное подозрение (дешёвая цена, новый продавец, крайние оценки, сильная полярность текста).

- **Равновесие** (`equilibrium.py`)
  - Подозрения обновляются итеративно до сходимости:
    \[
    s_{t+1}[i] = \mathrm{clip}\big(s_0[i] + \alpha \cdot \sum_j A_{ji} s_t[j], 0, 1\big)
    \]
  - Результат — устойчивый «степень враждебности» для каждого узла.

- **Каскад обнуления** (`cascade.py`)
  - Узлы выше порога запускают каскад, распространяющий подозрительность на соседей.
  - Моделирует, как локальная проблема (поддельный отзыв, сомнительный продавец) «заражает» окружение.

- **Интеграция** (`gra_adapter.py`, `deal_detector.py`)
  - `evaluate_product_safety()` возвращает удобное для пользователя резюме:
    - индекс доверия (`trust_score`)
    - степень враждебности (`adversarial_degree`)
    - доп. показатели по продавцу и отзывам (для старших тарифов)

---

### Модель подписки

- Stripe управляет подписками:
  - `/subscriptions/create-checkout-session` создаёт сессию оплаты выбранного плана.
  - `/subscriptions/webhook` принимает события Stripe и обновляет уровень пользователя.
- Активный уровень (`free`, `basic`, `premium`, `enterprise`) хранится в БД и используется для:
  - Контроля **доступа к API** (402 при недостаточном уровне)
  - Настройки **глубины графа** и детализации анализа

---

### Быстрый старт

#### 1. Клонирование и установка

```bash
git clone https://github.com/qqewq/Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-.git
cd Angel-in-Pocket-Shopping-Assistant-with-GRA-Nullification-Engine-
pip install -r requirements.txt
```

#### 2. Настройка окружения

Создайте `.env` по примеру `.env.example`:

```env
DATABASE_URL=postgresql://angel:secret@localhost/angel_pocket
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
GRA_INFLUENCE_WEIGHT=0.5
GRA_MAX_ITER=20
GRA_EPSILON=0.0001
CELERY_BROKER_URL=redis://localhost:6379/0
```

Запустите локально PostgreSQL и Redis.

#### 3. Запуск API

```bash
uvicorn app.main:app --reload
```

Документация будет доступна по адресу:  
`http://localhost:8000/docs`

---

### Основные эндпоинты

- **Аутентификация**
  - `POST /auth/register` — регистрация пользователя
  - `POST /auth/login` — получение JWT токена

- **Товары**
  - `GET /products/{product_id}/safety` — оценка безопасности товара  
    (доступна с уровня `basic` и выше)

- **Продавцы**
  - `GET /sellers/{seller_id}/trust` — усреднённое доверие по товарам продавца

- **Отзывы**
  - `POST /reviews/` — создание отзыва на товар

- **Подписки (Stripe)**
  - `POST /subscriptions/create-checkout-session` — запуск оформления подписки
  - `POST /subscriptions/webhook` — вебхук Stripe (настраивается в панели Stripe)

---

### План развития

- Подключить реальную NLP‑модель для оценки тональности отзывов.
- Внедрить полную математику **GRA‑Nullification‑Equilibrium** из экосистемы GRA.
- Добавить веб‑ или мобильный фронтенд поверх этого API.
- Расширить тарифы лимитами на количество запросов и аналитическими отчётами.

---

MIT License © qqewq
