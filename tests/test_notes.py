def test_create_note_then_get_and_list(client, auth_headers):
    payload = {"title": "Test note", "description": "desc", "priority": "low"}
    r = client.post("/notes/", json=payload, headers=auth_headers)
    assert r.status_code == 201, r.text
    note = r.json()
    note_id = note["id"]

    r = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert r.status_code == 200, r.text
    got = r.json()
    assert got["id"] == note_id
    assert got["title"] == payload["title"]

    r = client.get("/notes/all", headers=auth_headers)
    assert r.status_code == 200, r.text
    notes = r.json()
    assert any(n["id"] == note_id for n in notes)

def test_permissions_user_cannot_see_other_users_note(client):
    # user1
    email1 = "u1_" + __import__("uuid").uuid4().hex[:8] + "@example.com"
    pwd1 = "StrongPass123!"
    client.post("/auth/register", json={"email": email1, "password": pwd1})
    r = client.post(
        "/auth/login",
        data={"username": email1, "password": pwd1},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token1 = r.json()["access_token"]
    h1 = {"Authorization": f"Bearer {token1}"}

    # user2
    email2 = "u2_" + __import__("uuid").uuid4().hex[:8] + "@example.com"
    pwd2 = "StrongPass123!"
    client.post("/auth/register", json={"email": email2, "password": pwd2})
    r = client.post(
        "/auth/login",
        data={"username": email2, "password": pwd2},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token2 = r.json()["access_token"]
    h2 = {"Authorization": f"Bearer {token2}"}

    # user1 creates note
    r = client.post("/notes/", json={"title": "Secret", "description": "x", "priority": "low"}, headers=h1)
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # user2 should not see it -> אצלך זה 404 (NoteNotFoundError)
    r = client.get(f"/notes/{note_id}", headers=h2)
    assert r.status_code == 404, r.text
