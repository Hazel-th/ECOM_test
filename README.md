Запуск  
```bash
git clone https://github.com/yourusername/nsfw-moderator.git
cd nsfw-moderator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Установить свой DEEPAI_API_KEY в .env

```bash
uvicorn main:app --reload
```
Пример запроса 
```bash
curl -X POST -F "file=@example.jpg" http://localhost:8000/moderate
```
