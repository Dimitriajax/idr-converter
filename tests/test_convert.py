from fastapi.testclient import TestClient
import pytest
import httpx
from app.main import app
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = TestClient(app)

def get_response(idr: int, suffix: str = None)-> httpx.Response:
    params = {"idr": idr}
    if suffix:
        params["suffix"] = suffix
    headers = {"x-api-key": API_KEY}

    return client.get("/converter", params=params, headers=headers)

@pytest.mark.parametrize("idr, expected", [
    (1, "satu rupiah"),
    (10, "sepuluh rupiah"),
    (11, "sebelas rupiah"),
    (21, "dua puluh satu rupiah"),
    (147, "seratus empat puluh tujuh rupiah"),
    (583, "lima ratus delapan puluh tiga rupiah"),
    (1690, "seribu enam ratus sembilan puluh rupiah"),
    (2151, "dua ribu seratus lima puluh satu rupiah"),
    (10000, "sepuluh ribu rupiah"),
    (10500, "sepuluh ribu lima ratus rupiah"),
    (11030, "sebelas ribu tiga puluh rupiah"),
    (10500, "sepuluh ribu lima ratus rupiah"),
    (100000, "seratus ribu rupiah"),
    (104310, "seratus empat ribu tiga ratus sepuluh rupiah"),
])

def test_idr_writting_output(idr: int, expected: str) -> None:
    response = get_response(idr)
    assert response.status_code == 200
    assert response.json()["writting"] == expected

