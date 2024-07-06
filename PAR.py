import requests
from pywebio import input, output, start_server

# РЕГИОНЫ
regions = {
    "Москва": 1,
    "Санкт-Петербург": 2,
    "Новосибирск": 4,
    "Екатеринбург": 3,
    "Нижний Новгород": 66,
    "Казань": 88,
    "Челябинск": 56,
    "Ростов-на-Дону": 76,
    "Уфа": 99,
    "Волгоград": 38
}

def get_vacancies(keyword, region_id):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "area": region_id,
        "per_page": 100,
    }
    headers = {
        "User-Agent": "Your User Agent",
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])
        num_vacancies = len(vacancies)

        if num_vacancies > 0:
            for vacancy in vacancies:
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                work_experience = vacancy.get("experience", {}).get("name")
                employment_type = vacancy.get("employment", {}).get("name")
                schedule = vacancy.get("schedule", {}).get("name")

                output.put_html(f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px;">
                    <h3>{vacancy_title}</h3>
                    <p><strong>Компания:</strong> {company_name}</p>
                    <p><strong>URL:</strong> <a href="{vacancy_url}" target="_blank">{vacancy_url}</a></p>
                    <p><strong>Опыт работы:</strong> {work_experience}</p>
                    <p><strong>Тип занятости:</strong> {employment_type}</p>
                    <p><strong>График работы:</strong> {schedule}</p>
                </div>
                """)

        else:
            output.put_text("Вакансии не найдены.")
    else:
        output.put_text(f"Запрос завершился ошибкой с кодом: {response.status_code}")

def search_vacancies():
    keyword = input.input("Введите название вакансии:", type=input.TEXT)
    selected_region = input.select("Выберите регион:", options=list(regions.keys()))
    region_id = regions[selected_region]

    output.clear()
    output.put_html('<p><strong>Поиск вакансий...</strong></p>')
    get_vacancies(keyword, region_id)

if __name__ == '__main__':
    start_server(search_vacancies, port=8080)

# парсер с sql

from time import sleep
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# РЕГИОНЫ
regions = {...}  # те же регионы, что и ранее

DB_URL = "postgresql://user:password@db:5432/vacancies_db"

def create_db():
    engine = create_engine(DB_URL)
    metadata = MetaData()

    vacancies = Table('vacancies', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('title', String),
                      Column('company', String),
                      Column('url', String),
                      Column('experience', String),
                      Column('employment_type', String),
                      Column('schedule', String),
                      )

    metadata.create_all(engine)

    return engine, vacancies


def get_vacancies(engine, vacancies, keyword, region_id):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "area": region_id,
        "per_page": 100,
    }
    headers = {"User-Agent": "Your User Agent"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vacancy_items = data.get("items", [])
        with engine.connect() as conn:
            for vacancy in vacancy_items:
                vacancy_data = {
                    'id': vacancy.get("id"),
                    'title': vacancy.get("name"),
                    'company': vacancy.get("employer", {}).get("name"),
                    'url': vacancy.get("alternate_url"),
                    'experience': vacancy.get("experience", {}).get("name"),
                    'employment_type': vacancy.get("employment", {}).get("name"),
                    'schedule': vacancy.get("schedule", {}).get("name"),
                }
                conn.execute(vacancies.insert().values(vacancy_data))


def main():
    engine, vacancies = create_db()
    for region_name, region_id in regions.items():
        get_vacancies(engine, vacancies, "Python разработчик", region_id)
        sleep(1)


if __name__ == '__main__':
    main()


# аналитика!!!!!!!!!!!!

from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_URL = "postgresql://user:password@db:5432/vacancies_db"

def get_vacancy_count():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM vacancies"))
        num_vacancies = result.scalar()
    return num_vacancies


def main():
    num_vacancies = get_vacancy_count()
    print(f"Total number of vacancies: {num_vacancies}")


if __name__ == '__main__':
    main()
