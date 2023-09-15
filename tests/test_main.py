import os
from fastapi.testclient import TestClient
from mic_racoon_challange import app

client = TestClient(app)


def test_read_api():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_read_not_found():
    response = client.get("/api/foo/bar")
    assert response.status_code == 200
    assert response.json() == {"error": "not found"}


def test_upload_api():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fpath = dir_path + '/files/logo.jpg'
    response = client.post("/api/upload/", files={"file": ("filename", open(fpath, "rb"), "image/jpeg")})
    assert response.status_code == 200
    assert response.json() == {
            "filename": "",
            "volume": -1,
            "status": "failed",
        }



