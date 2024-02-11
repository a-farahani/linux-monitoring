### linux-monitoring
Do you want to know if your server is accessible from a certain country?
There is a Python code powered by [check-host.net API](https://check-host.net/about/api) that can monitor your accessibility and send results to your telegram bot. if you want to use spesific node check [this](https://check-host.net/nodes/hosts).

![Telegram Bot Message](images/documentation/telegram-bot-message.jpg)

### How to use?

### Docker (recommended)
1- get docker-compose.yml from repo \
2- create `.env` like `.env.example` \
3- `docker compose up -d` (for stop docker `docker compose down`)

### Without Docker
1- clone latest release \
2- create `.env` like `.env.example` \
3- run code with `bash ./start.sh` (for stop `bash ./stop.sh`)
