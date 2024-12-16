from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Создаем приложение
app = FastAPI()

# Список пользователей
users: List[dict] = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# 1. GET запрос для получения всех пользователей
@app.get("/users")
async def get_users() -> List[User]:
    return users

# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def add_user(username: str, age: int) -> User:
    new_id = users[-1]['id'] + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user.dict())
    return new_user

# 3. PUT запрос для обновления данных пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user['id'] == user_id:
            user['username'] = username
            user['age'] = age
            return User(**user)
    raise HTTPException(status_code=404, detail="User was not found")

# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> User:
    for index, user in enumerate(users):
        if user['id'] == user_id:
            removed_user = users.pop(index)
            return User(**removed_user)
    raise HTTPException(status_code=404, detail="User was not found")

# Тестовые запросы (сценарий выполнения)
# 1. GET '/users'
# []
#
# 2. POST '/user/UrbanUser/24'
# User(id=1, username="UrbanUser", age=24)
#
# 3. POST '/user/UrbanTest/36'
# User(id=2, username="UrbanTest", age=36)
#
# 4. POST '/user/Admin/42'
# User(id=3, username="Admin", age=42)
#
# 5. PUT '/user/1/UrbanProfi/28'
# User(id=1, username="UrbanProfi", age=28)
#
# 6. DELETE '/user/2'
# User(id=2, username="UrbanTest", age=36)
#
# 7. GET '/users'
# [
#     {
#         "id": 1,
#         "username": "UrbanProfi",
#         "age": 28
#     },
#     {
#         "id": 3,
#         "username": "Admin",
#         "age": 42
#     }
# ]
#
# 8. DELETE '/user/2'
# HTTPException(status_code=404, detail="User was not found")