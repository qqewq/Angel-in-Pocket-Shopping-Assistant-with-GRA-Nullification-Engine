"""
GRA Evolution Predictor
Строит персональную дорожную карту желаний на основе
GRA-Core и Hierarchical-Stability-Rank-N.
"""
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np

# Подключаем внешние GRA-библиотеки (должны быть в PYTHONPATH)
sys.path.append(os.environ.get("GRA_LIBS_PATH", "../GRA-Core-new-Unified-Hierarchical-Stability-Library"))
from gra_core import GRAEngine
from hierarchical_stability import StabilityRanker

class EvolutionPredictor:
    def __init__(self):
        self.gra_engine = GRAEngine()
        self.stability_ranker = StabilityRanker()
        # Загружаем эталонные эволюционные треки (можно из файла)
        self.reference_tracks = self._load_reference_tracks()

    def _load_reference_tracks(self) -> Dict:
        # Упрощённо: возрастные паттерны спроса
        return {
            "childhood":  {"age_range": (0,12), "clusters": ["toys", "education", "health"]},
            "teen":       {"age_range": (13,19), "clusters": ["gadgets", "education", "social"]},
            "young":      {"age_range": (20,30), "clusters": ["career", "travel", "housing"]},
            "family":     {"age_range": (31,45), "clusters": ["family", "health", "investment"]},
            "mature":     {"age_range": (46,60), "clusters": ["health", "comfort", "legacy"]},
            "senior":     {"age_range": (61,99), "clusters": ["health", "leisure", "care"]}
        }

    def predict(self, user_profile: dict, horizon_years: int = 5) -> List[Dict]:
        """
        user_profile: содержит возраст, пол, доход, семейный статус, историю покупок, предпочтения.
        Возвращает список предсказаний по годам.
        """
        predictions = []
        current_year = datetime.now().year
        age = user_profile.get("age", 30)
        # Простейшая модель на основе возраста (в реальности GRA строит многослойную карту)
        for year_offset in range(1, horizon_years + 1):
            target_year = current_year + year_offset
            target_age = age + year_offset
            phase = self._get_life_phase(target_age)
            clusters = self.reference_tracks[phase]["clusters"]
            # GRA-обнуление: вычисляем стабильные желания, отсеивая шум
            base_desire = self._gra_predict(user_profile, target_age, clusters)
            # Применяем хиральное ветвление сценариев
            scenario = user_profile.get("life_scenario", "default")
            desire = self._apply_chiral_branch(base_desire, scenario, target_age)
            predictions.append({
                "year": target_year,
                "age": target_age,
                "category": desire["category"],
                "description": desire["description"],
                "confidence": round(desire["confidence"], 2),
                "trigger": desire.get("trigger", "")
            })
        return predictions

    def _get_life_phase(self, age: int) -> str:
        for phase, info in self.reference_tracks.items():
            low, high = info["age_range"]
            if low <= age <= high:
                return phase
        return "mature"

    def _gra_predict(self, user_profile: dict, target_age: int, clusters: list) -> dict:
        # Вызов GRA-Core: он вернёт наиболее стабильную потребность с учётом иерархии
        # Здесь имитация; в реальности обращение к gra_engine.process(...)
        # Возвращаем категорию с наивысшим рангом стабильности
        ranked = self.stability_ranker.rank(clusters, user_profile)
        top = ranked[0]
        return {
            "category": top["cluster"],
            "description": f"Потребность в категории {top['cluster']} с вероятностью {top['score']}",
            "confidence": top["score"]
        }

    def _apply_chiral_branch(self, base_desire: dict, scenario: str, age: int) -> dict:
        # Использует GRA-Chiral-Nullification-Math для зеркальных сценариев
        # Упрощённо: если сценарий «переезд», меняем категорию
        if scenario == "relocation":
            if base_desire["category"] == "housing":
                base_desire["category"] = "travel"
                base_desire["description"] = "В связи с переездом вероятна потребность в аренде жилья и путешествиях"
                base_desire["confidence"] *= 0.9
        return base_desire
