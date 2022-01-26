# Устанавливаю базовый образ

FROM debian:bookworm

# Обновляю репозитории и устанавливаю Java Runtime Environment 11
RUN apt-get -y update && apt-get install -y openjdk-11-jre

# Устанавливаю python 3.9 и модуль pip
RUN apt-get install -y python3 && apt-get install -y python3-pip

# Копирую deb пакет allure
COPY allure_2.15.0-1_all.deb .

# Устанавливаю allure
RUN dpkg -i allure_2.15.0-1_all.deb

# Создаю рабочую директорию внутри контейнера
WORKDIR /app

# Копирую зависимости
COPY requirements.txt .	

# Выполняю необходимые команды

RUN pip3 install -U pip && pip3 install -r requirements.txt

# Копирую остальные файлы проекта
COPY . .
	
CMD ["pytest"]
