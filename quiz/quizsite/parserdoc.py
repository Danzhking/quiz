import re
from docx import Document
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizsite.settings")
django.setup()

from myapp.models import Question, Answer

def parse_questions_from_word(document_path):
    doc = Document(document_path)
    questions = []

    current_question = None
    answer_regex = re.compile(r'^[A-Z]\)')

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if not text:  # Пропускаем пустые строки
            continue

        if text[0].isdigit():
            
            if current_question is not None:
                questions.append(current_question)

            current_question = {"text": text, "answers": []}
        elif current_question is not None and answer_regex.match(text):
            
            current_question["answers"].append(text)

    # Добавим последний вопрос
    if current_question is not None:
        questions.append(current_question)

    return questions

def extract_correct_answer(answer_text):

    answer_parts = answer_text.split('~')
    if len(answer_parts) > 1:
        return answer_parts[-1].strip()
    else:
        return None

def save_questions_to_database(questions):
    for question_data in questions:
        # Создаем вопрос в базе данных
        question = Question.objects.create(text=question_data["text"])

        # Создаем ответы к вопросу
        for answer_text in question_data["answers"]:
            is_correct = extract_correct_answer(answer_text) == answer_text.strip(')')

            Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)

def main():
    document_path = 'C:\\Users\\79038\\Downloads\\Gornostaev.docx'
    questions = parse_questions_from_word(document_path)

    # Сохраняем вопросы в базу данных
    save_questions_to_database(questions)

    print("Вопросы успешно добавлены в базу данных.")

if __name__ == "__main__":
    main()
