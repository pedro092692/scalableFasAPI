from fastapi import status


class TestCreateUser:

    def test_create_user_success(self, client):
        payload = {
            'name': 'Ana garcia',
            'email': 'ana@example.com',
            'password': 'secure123'
        }

        response = client.post('/api/v1/users', json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['email'] == 'ana@example.com'
        assert 'id' in data
        assert 'password' not in data

    def test_create_user_duplicate_email(self, client):
        payload = {
            'name': 'test',
            'email': 'ana@example.com',
            'password': 'secure123'
        }

        client.post('/api/v1/users', json=payload)
        response = client.post('/api/v1/users', json=payload)
        assert response.status_code == status.HTTP_409_CONFLICT


    def test_create_user_invalid_email(self, client):
        payload = {
            'name': 'test',
            'email': 'no-an-email',
            'password': 'notsecure123'
        }
        response = client.post('/api/v1/users', json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestGetUser:
    def test_get_existing_user(self, client):
        create_r = client.post('/api/v1/users', json={
            "name": "Bob", "email": "bob@test.com", "password": "pass1234"
        })
        user_id = create_r.json()['id']
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200

    def test_get_nonexistent_user(self, client):
        response = client.get("/api/v1/users/99999")
        assert response.status_code == 404

    def test_get_all_users(self, client):
        response = client.get('/api/v1/users/all')
        assert response.status_code == status.HTTP_200_OK
