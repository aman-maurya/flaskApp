import json
from flask import url_for


class TestUser(object):
    def test_user_list(self, client):
        """ Home page should respond with a success 200. """
        response = client.get(url_for('user_v1.user_list'))
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        # print(json.loads(response.data))
        # resp_body = response.json()
        # assert resp_body == {'ok'}

