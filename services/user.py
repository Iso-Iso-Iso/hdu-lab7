import requests


def validate(status_code):
    if status_code == 400:
        raise Exception("Incorrect request data")
    if status_code == 401:
        raise Exception("Incorrect credentials")
    if status_code > 400:
        raise Exception("Woops! Somthing went wrong :(")


class UserServices:
    @staticmethod
    def login(username, password):
        response = requests.post(
            "https://ksu24.kspu.edu/api/v2/login/",
            data={
                "username": username,
                "password": password
            }
        )
        print(response)
        validate(response.status_code)
        if response.ok:
            return {"refresh": response.cookies.get_dict()['JWT']}

    @staticmethod
    def get_profile(token):
        res = requests.get(
            "https://ksu24.kspu.edu/api/v2/my/students/",
            cookies={
                "JWT": token
            }
        )
        validate(res.status_code)
        return res.json()['results'][0]

    @staticmethod
    def get_recordbooks(id, token):
        res = requests.get(
            f"https://ksu24.kspu.edu/api/v2/my/students/{id}/recordbooks/",
            cookies={
                "JWT": token
            }
        )
        validate(res.status_code)
        return res.json()

    @staticmethod
    def get_recordbooks_record(id, token):
        res = requests.get(
            f"https://ksu24.kspu.edu/api/v2/my/students/{id}/recordbooks/c7ff068d-7bee-4b59-a13c-dbdde46ba151/records/",
            cookies={
                "JWT": token
            }
        )
        validate(res.status_code)
        return res.json()

    @staticmethod
    def get_gradebook(token):
        res = requests.get(
            f"https://ksu24.kspu.edu/api/gradebook/student_gradebook/",
            cookies={
                "JWT": token
            }
        )
        validate(res.status_code)
        return res.json()

    @staticmethod
    def get_phonebook(token, search_name):
        res = requests.get(
            f"https://ksu24.kspu.edu/api/phone_book/",
            cookies={
                "JWT": token
            },
            params={
                "search": search_name
            }
        )
        validate(res.status_code)
        return res.json()
