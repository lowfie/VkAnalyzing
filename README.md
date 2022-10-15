# Аналитический телеграмм-бот для ВК

Удобный аналитический бот, который поможет мониторить группы ВК, следить за реакцией пользователей и статистикой

## Вы сможете
- Собирать данные группы одной командой 
- Отслеживать статистику по периоду
- Смотреть топы групп по периоду
- Наладить автоматический мониторинг

# Установка
1. Клонируйте репозиторий с GitHub `git clone https://github.com/lowfie/VkAnalyzing.git`
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Добавьте файл `.env` в папку директорию `data`
5. Установите docker для вашей ОС

Запустите локальную БД для работы FSM в aiogram и PostgreSQL для сбора данных:
```
docker run -p 6379:6379 -d redis
docker run -p 5432:5432 -e POSTGRES_PASSWORD=123 -d postgres
```
