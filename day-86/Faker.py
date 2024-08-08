import requests

class Faker:
    def __init__(self):
        response = requests.get("https://fakerapi.it/api/v1/texts?_quantity=1")
        response.raise_for_status()

        self.fake_sentence = response.json()

    def get_sentence(self):
        # print(self.fake_sentence)
        return self.fake_sentence["data"][0]
    
    def get_new_sentence(self):
        response = requests.get("https://fakerapi.it/api/v1/texts?_quantity=1")
        response.raise_for_status()

        self.fake_instance = response.json()
        self.fake_sentence = self.fake_instance["data"][0]
        return self.fake_sentence
        