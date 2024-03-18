# Проєкт "PhotoRecognitionApp"
<p align="center">
   <img src="https://img.shields.io/badge/Language-Python-9cf">
   <img src="https://img.shields.io/badge/FastAPI-0.95.1-brightgreen">
   <img src="https://img.shields.io/badge/SQLAlchemy-2.0-orange">
   <img src="https://img.shields.io/badge/Pytest-7.3.0-informational">
   <img src="https://img.shields.io/badge/Language-HTML-purple">
   <img src="https://img.shields.io/badge/Language-CSS-blue">
   <img src="https://img.shields.io/badge/Platform-Jupyter-orange">
   <img src="https://img.shields.io/badge/Library-TensorFlow-pink">
   <img src="https://img.shields.io/badge/License-MIT-yellow">
</p>

## Опис моделі


## Розміщення на DockerHub 
<a href="https://hub.docker.com/r/ustymenko/data_science/tags">PhotoRecognitionApp</a>

## Установка 💻

1. Для розгортання додатку локально на комп'ютері потрібно завантажити проєкт з репозиторію GitHub.
2. Встановити ```Docker(desktop)```
3. Встановити пакет віртуального оточення ```poetry```
4. Запустити середовище розробки 
5. Створити ```".env"``` файл на основі ```"example.env"```
6. В терміналі виконати команду ```poetry lock```
7. В терміналі виконати команду ```poetry install```
8. В терміналі виконати команду ```poetry sell```
9. В терміналі виконати команду ```docker-compose up -d```
10. Передати у контейнер ```".env"``` файл командою ```docker cp .env photorecognitionapp-my_service-1:.env```
11. Створити таблиці БД командою в терміналі ```docker exec photorecognitionapp-my_service-1 python create_db.py```
11. Виконати міграції БД командою в терміналі ```docker exec photorecognitionapp-my_service-1 alembic upgrade heads```
12. Також в терміналі запустити серевер командою ```docker exec -d photorecognitionapp-my_service-1 uvicorn main:app --host 0.0.0.0 --port 8080 --reload```
13. Відкрити сторінку в браузері за посиланням ```http://localhost:8080/```.
 
## Розробники
<div align="">
  Developer: <a href="https://github.com/OlegDovhyi">Oleg Dovhyi</a><br>
  Developer: <a href="https://github.com/Nevskiy911">Oleksandr Malieiev</a><br>
  Developer: <a href="https://github.com/CadejoBlanko">Oleksandr Martyniuk</a><br>
  Scrum Master/Developer: <a href="https://github.com/GhosteLLoS">Oleksii Medvetskyi</a><br>
  Team Lead/Developer: <a href="https://github.com/UstymenkoOB">Oksana Ustymenko</a><br>
</div>
