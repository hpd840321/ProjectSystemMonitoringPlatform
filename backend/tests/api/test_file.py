import pytest
from pathlib import Path

async def test_file_upload(client, admin_token):
    """测试文件上传"""
    test_file = Path(__file__).parent / "test_data" / "test.txt"
    with open(test_file, "rb") as f:
        response = await client.post(
            "/api/v1/files/upload",
            files={"file": ("test.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data

async def test_file_download(client, admin_token):
    """测试文件下载"""
    # 先上传文件
    test_file = Path(__file__).parent / "test_data" / "test.txt"
    with open(test_file, "rb") as f:
        upload_response = await client.post(
            "/api/v1/files/upload",
            files={"file": ("test.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    file_id = upload_response.json()["file_id"]
    
    # 测试下载
    response = await client.get(
        f"/api/v1/files/{file_id}/download",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain"

async def test_file_list(client, admin_token):
    """测试文件列表"""
    response = await client.get(
        "/api/v1/files",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 