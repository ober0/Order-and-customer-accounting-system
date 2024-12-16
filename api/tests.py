import requests
from pprint import pprint


class TokenManager:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.obtain_tokens()

    def obtain_tokens(self):
        data = {"username": self.username, "password": self.password}
        auth_response = requests.post(f'{self.base_url}/api/token/', data=data)
        if auth_response.status_code != 200:
            exit()
        tokens = auth_response.json()
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def refresh_access_token(self):
        refresh_response = requests.post(f'{self.base_url}/api/token/refresh/', data={'refresh': self.refresh_token})
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            self.access_token = new_tokens.get('access')
        else:
            exit()


class APIClient:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.base_url = token_manager.base_url

    def add_client(self, client_data):
        url = f'{self.base_url}/api/clients/add/'
        headers = {'Authorization': f'Bearer {self.token_manager.access_token}'}
        response = requests.post(url, headers=headers, data=client_data)
        if response.status_code == 200:
            pprint(response.json())
        elif response.status_code == 401:
            self.token_manager.refresh_access_token()
            self.add_client(client_data)
        else:
            print(response.text)

    def get_all_clients(self, start_id):
        url = f'{self.base_url}/api/clients/get/'
        headers = {'Authorization': f'Bearer {self.token_manager.access_token}'}
        data = {'start_id': start_id}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            clients = response.json().get('clients', [])
            pprint(clients)
        elif response.status_code == 401:
            self.token_manager.refresh_access_token()
            self.get_all_clients(start_id)
        else:
            print(response.text)

    def edit_client(self, id, client_data):
        url = f'{self.base_url}/api/clients/edit/{id}/'
        headers = {'Authorization': f'Bearer {self.token_manager.access_token}'}
        response = requests.post(url, headers=headers, data=client_data)
        if response.status_code == 200:
            pprint(response.json())
        elif response.status_code == 401:
            self.token_manager.refresh_access_token()
            self.edit_client(id, client_data)
        else:
            print(response.text)

    def delete_client(self, id):
        url = f'{self.base_url}/api/clients/delete/{id}/'
        headers = {'Authorization': f'Bearer {self.token_manager.access_token}'}
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            pprint(response.json())
        elif response.status_code == 401:
            self.token_manager.refresh_access_token()
            self.delete_client(id)
        else:
            print(response.text)

if __name__ == '__main__':
    BASE_URL = 'http://127.0.0.1:8000'
    USERNAME = 'admin'
    PASSWORD = 'admin'
    token_manager = TokenManager(USERNAME, PASSWORD, BASE_URL)
    api_client = APIClient(token_manager)

    new_client = {
        'first_name': 'Руслан',
        'last_name': 'Онищенко',
        'middle_name': 'Виталиевич',
        'mobile_phone': None,
        'email': 'onishruslan@yandex.ru'
    }

    edit_client_data = {
        'first_name': 'Тестовое имя',
        'last_name': 'Тестовая фамилия'
    }

    api_client.delete_client(id=2   )
