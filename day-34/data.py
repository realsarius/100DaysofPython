import requests

parameters = {
    "amount": 10,
    "type": "boolean",
}

try:
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status() 

    data = response.json()

    question_data = data["results"]

    for index, question in enumerate(question_data):
        print(f"Question {index + 1}: {question['question']}")
        print(f"Answer: {question['correct_answer']}")
        print()

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")