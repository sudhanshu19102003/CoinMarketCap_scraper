
# Coinmarketcap Scraping API ASSIGNMENT

> [!CAUTION]
> This project is intended for educational purposes only. It serves as a learning resource for understanding how to develop a Django REST Framework API for scraping cryptocurrency data. The project utilizes Celery for asynchronous task management and Selenium for dynamic web scraping.

## Overview

This repository contains a Django REST Framework API for scraping cryptocurrency data from various sources. It utilizes Celery for asynchronous task management, allowing parallel scraping of multiple cryptocurrencies. The API enables users to initiate scraping tasks, monitor their progress, and retrieve the scraped data.

## Features

- **Scraping Initiation**: Initiate scraping tasks for multiple cryptocurrencies simultaneously.
- **Asynchronous Processing**: Utilize Celery for asynchronous execution of scraping jobs, ensuring scalability and responsiveness.
- **Real-time Monitoring**: Track the progress of scraping tasks and retrieve the current status.
- **Flexible Scraping**: Utilize Selenium for dynamic web scraping, enabling extraction of data from JavaScript-rendered pages.

## Usage

### Initiating Scraping

Endpoint: `POST /api/taskmanager/start_scraping`

![Screenshot 2024-06-06 184744](https://github.com/sudhanshu19102003/CoinMarketCap_scraper/assets/78022236/d315835e-812b-4648-9148-33084d7745ef)


### Checking Scraping Status

Endpoint: `GET /api/taskmanager/scraping_status/<job_id>`

![Screenshot 2024-06-06 184823](https://github.com/sudhanshu19102003/CoinMarketCap_scraper/assets/78022236/7a5ea769-ece2-4d2c-be87-828f2471c6d1)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cryptocurrency-scraping-api.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations:

    ```bash
    python manage.py migrate
    ```

4. Start the Celery worker:

    ```bash
    celery -A yourprojectname worker --loglevel=info
    ```

5. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to propose changes or enhancements to the project.

---

Feel free to customize the content and styling further according to your preferences and project specifics.
