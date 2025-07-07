import requests

isbn = "686ab7b5710f4a556e34e864"
response = requests.get(f"http://localhost:8000/search_by_isbn?isbn={isbn}")
print("Ответ сервера:", response.status_code)
if response.status_code == 200:
    book = response.json()
    print(book)
    print("Книга найдена:", book)
else:
    print("Ошибка:", response.json().get('detail', 'Неизвестная ошибка'))