"""
Фильтр этичности: скрывает предсказания, которые могут
нанести психологический вред при прямой выдаче.
"""
SENSITIVE_PATTERNS = [
    "divorce", "disease", "death", "bankruptcy", "addiction"
]

class EthicalFilter:
    @staticmethod
    def filter(roadmap_item: dict) -> dict:
        desc = roadmap_item.get("description", "").lower()
        if any(pattern in desc for pattern in SENSITIVE_PATTERNS):
            # Смягчаем формулировку
            roadmap_item["description"] = "Возможны изменения в личной/финансовой сфере. Рекомендуем консультацию специалиста."
            roadmap_item["confidence"] = 0.0   # не показываем процент
        return roadmap_item
