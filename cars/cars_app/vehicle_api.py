import requests
from django.core.cache import cache
import logging

URL = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"
MODEL_NAME_FIELD = "Model_Name"
RESULTS_FIELD = "Results"


def vehicle_exists(make: str, model_name: str) -> bool:
    for model in get_models_of_a_make(make)[RESULTS_FIELD]:
        if model[MODEL_NAME_FIELD].lower() == model_name.lower():
            return True
    return False


def get_models_of_a_make(make: str) -> dict:
    return cache.get_or_set(make, lambda: requests.get(URL.format(make)).json())
