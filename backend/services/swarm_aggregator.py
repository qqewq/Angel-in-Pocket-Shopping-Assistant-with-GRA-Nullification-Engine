"""
GRA-Swarm-Subject Aggregator
Собирает обезличенные дорожные карты, формирует
регионально-отраслевой прогноз спроса (Госплан).
"""
import json
import hashlib
from collections import defaultdict
from datetime import datetime
from typing import List, Dict
import numpy as np
from .evolution_predictor import EvolutionPredictor  # для единообразия

class SwarmAggregator:
    def __init__(self, db_session_factory):
        self.db = db_session_factory
        self.predictor = EvolutionPredictor()

    def aggregate(self, region: str = None, sector: str = None, horizon: int = 5) -> List[Dict]:
        """
        Извлекает из БД анонимизированные профили (хэш user_id),
        строит дорожные карты, суммирует по категориям и годам.
        Возвращает список {year, category, demand_score}.
        """
        profiles = self._fetch_anonymized_profiles(region)
        demand_accum = defaultdict(lambda: defaultdict(float))
        for profile in profiles:
            roadmap = self.predictor.predict(profile, horizon_years=horizon)
            for item in roadmap:
                cat = item["category"]
                demand_accum[item["year"]][cat] += item["confidence"]
        # Преобразуем в список
        result = []
        for year, cats in sorted(demand_accum.items()):
            for cat, score in cats.items():
                if sector and sector != cat:
                    continue
                result.append({
                    "year": year,
                    "category": cat,
                    "demand_score": round(score, 2),
                    "region": region or "global"
                })
        return result

    def _fetch_anonymized_profiles(self, region: str) -> List[Dict]:
        # Имитация запроса к БД пользователей, согласившихся на агрегацию
        # Возвращает список профилей без персональных данных (только возраст, пол, доход, кластер интересов)
        # В реальности – SQL запрос с групповой анонимизацией.
        return [
            {"age": 32, "gender": "F", "income_level": "medium", "interests": ["tech", "health"]},
            {"age": 45, "gender": "M", "income_level": "high", "interests": ["luxury", "travel"]}
        ]
