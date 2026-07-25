# -*- coding: utf-8 -*-
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.helpers import ApiClient

BASE_URL = "http://localhost:5001"

@pytest.fixture(scope="module")
def base_url():
    return BASE_URL

@pytest.fixture(scope="module")
def api(base_url):
    return ApiClient(base_url)
