FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей и установите их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте всё остальное в виде приложения
COPY . .

# Убедитесь, что нужные директории (например, для базы данных) созданы
RUN mkdir -p /home/searhei/app/data

# Задайте переменные окружения
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Откройте порт, на котором будет работать приложение
EXPOSE 5000

# Команда для запуска приложения с использованием Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
