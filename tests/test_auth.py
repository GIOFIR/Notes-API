def test_register_and_login_flow(client, unique_email, password):
    r = client.post("/auth/register", json={"email": unique_email, "password": password})
    assert r.status_code == 201, r.text

    r = client.post(
        "/auth/login",
        data={"username": unique_email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"
