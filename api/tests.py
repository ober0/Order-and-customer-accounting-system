import requests


class CheckAccessToApi:
    def __init__(self):
        data = {
            "username": "admin",
            "password": "admin"
        }

        # Получаем токены
        auth_response = requests.post('http://127.0.0.1:8000/api/token/', data=data)
        if auth_response.status_code != 200:
            exit()

        tokens = auth_response.json()
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

        # Делаем защищённый запрос
        self.make_protected_request()

    def make_protected_request(self):
        data = {
            'first_name': 'Руслан',
            'last_name': 'Онищенко',
            'middle_name': 'Виталиевич',
            'mobile_phone': None,
            'email': 'onishruslan@yandex.ru'
        }
        protected_response = requests.post('http://127.0.0.1:8000/api/clients/add/',
                                           headers={'Authorization': f'Bearer {self.access_token}'}, data=data)

        if protected_response.status_code == 200:
            print("Success:", protected_response.json())
        elif protected_response.status_code == 401:
            response_data = protected_response.json()
            if 'error' in response_data and response_data['error'] == 'Token has expired':
                print("Access token has expired. Attempting to refresh...")
                self.refresh_access_token()
                self.make_protected_request()
            else:
                print("Unauthorized:", response_data)
        else:
            print(f"Error {protected_response.status_code}:", protected_response.text)

    def refresh_access_token(self):
        refresh_response = requests.post('http://127.0.0.1:8000/api/token/refresh/',
                                         data={'refresh': self.refresh_token})
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            self.access_token = new_tokens.get('access')
            print("Access token refreshed.")
        else:
            print("Failed to refresh token:", refresh_response.json())
            exit()


if __name__ == '__main__':
    CheckAccessToApi()
