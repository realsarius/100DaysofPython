import html
from typing import List, Dict

class QuizBrain:
    def __init__(self, q_list: List[Dict[str, str]]):

        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def has_more_questions(self) -> bool:
        return self.question_number < len(self.question_list)

    def get_next_question(self) -> str:
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question['question'])
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer: str) -> bool:
        correct_answer = self.current_question['correct_answer']
        if user_answer.strip().lower() == correct_answer.strip().lower():
            self.score += 1
            return True
        return False
