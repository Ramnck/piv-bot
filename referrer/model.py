from utils import Info
import requests


class Referrer:
    def __init__(self):
        self.model_name = "mistral:7b"
        self.url = "http://localhost:11434/api/generate"
        pass

    def make_referrence(self, user_prompt: str, bottle_infos: list[Info]) -> str:
        beer_list = "\n".join(
            f"{i + 1}. {info.name} — {info.beer_type}, {info.conclusion}, {info.strength}%, {info.country}, {info.cost} руб., рейтинг: {info.score}"
            for i, info in enumerate(bottle_infos)
        )
        prompt = (
            "Твоя задача — помочь мне выбрать пиво на полке на основе моих вкусовых предпочтений. "
            "Следуй следующей структуре ответа:\n"
            "Вступление: Объясни, что ты будешь делать. Старайся сразу переходить к делу и не представляться.\n"
            "Рекомендации: Если я хочу что-то конкретное, проверь, есть ли это пиво в списке доступных. "
            "Если конкретного пива нет, явно скажи, что его нет в наличии. "
            "Если я не указал конкретное пиво, проанализируй мои предпочтения и предложи 1–3 подходящих варианта из доступных. "
            "Для каждого рекомендуемого пива укажи краткую информацию о нем. "
            "Если нет ни одного подходящего варианта, честно скажи об этом. "
            "Не выдумывай пиво, которого нет в списке, и не добавляй информацию, которая не основана на данных из списка пива. "
            "Дай краткое объяснение, почему именно эти сорта подходят. Если подходящих вариантов нет, просто скажи об этом. "
            "Не рекомендуй ничего, если не уверен в соответствии моим предпочтениям.\n\n"
            f"Вот мой запрос:\n{user_prompt}\n\n"
            f"А вот список пива, доступного на полке:\n{beer_list}\n\n"
        )


        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url, json=payload)


        if response.status_code == 200:
            try:
                result = response.json()
                return result.get("output", result.get("response", "<no field>"))
            except ValueError as e:
                return f"Ошибка разбора JSON: {e}"
        else:
            return f"Ошибка запроса: {response.status_code}"
        