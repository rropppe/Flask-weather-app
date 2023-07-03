# Используем базовый образ Python
FROM python:3.9

# Установка рабочей директории в контейнере
WORKDIR /weather

# Копирование всех файлов из корневой папки в контейнер
COPY . /weather

# Обновление интерпретатора и установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск команды для запуска приложения
CMD python app.py
