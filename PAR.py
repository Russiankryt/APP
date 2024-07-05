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
            for i, vacancy in enumerate(vacancies):

                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                work_experience = vacancy.get("experience", {}).get("name")
                employment_type = vacancy.get("employment", {}).get("name")
                schedule = vacancy.get("schedule", {}).get("name")

                output.put_text(f"ID: {vacancy_id}")
                output.put_text(f"Заголовок: {vacancy_title}")
                output.put_text(f"Компания: {company_name}")
                output.put_text(f"URL: {vacancy_url}")
                output.put_text(f"Опыт работы: {work_experience}")
                output.put_text(f"Тип занятости: {employment_type}")
                output.put_text(f"График работы: {schedule}")
                output.put_text("")

                if i < num_vacancies - 1:
                    output.put_text("---------")
        else:
            output.put_text("Вакансии не найдены.")
    else:
        output.put_text(f"Запрос завершился ошибкой с кодом: {response.status_code}")

def search_vacancies():
    keyword = input.input("Введите название вакансии:", type=input.TEXT)
    selected_region = input.select("Выберите регион:", options=list(regions.keys()))
    region_id = regions[selected_region]

    output.clear()
    output.put_text("Поиск вакансий...")
    get_vacancies(keyword, region_id)

if __name__ == '__main__':
    start_server(search_vacancies, port=8080)
