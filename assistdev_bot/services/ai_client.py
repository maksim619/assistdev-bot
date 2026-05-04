import httpx
import asyncio
from config import DEEPSEEK_API_KEY


class AIClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-v4-flash"

    async def chat(self, messages, max_tokens=300):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": max_tokens,
        }
        timeout = httpx.Timeout(15.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"AI error: {response.status_code} - {response.text}")
                    return "❌ Ошибка API. Попробуйте позже или напишите Максиму напрямую."
            except asyncio.TimeoutError:
                return "⏱️ Сервер AI не отвечает. Пожалуйста, повторите позже или нажмите «Заказать услугу»."
            except Exception as e:
                print(f"AI exception: {e}")
                return "⚠️ Техническая ошибка. Используйте кнопку заказа."
