from django.shortcuts import render
from django.http import JsonResponse
from .models import Question


def quiz_view(request):
    if request.method == 'POST':
        selected_answers_ids = request.POST.getlist('answers[]')
        current_question_index = request.session.get('current_question_index', 0)
        questions = Question.objects.all()

        if current_question_index < len(questions):
            current_question = questions[current_question_index]
            correct_answers_ids = [str(answer) for answer in current_question.answers.filter(is_correct=True)]
            selected_answers_id = [str(answer) for answer in selected_answers_ids]
            
            if set(correct_answers_ids) == set(selected_answers_id):
            
                request.session['score'] = request.session.get('score', 0) + 1
                request.session.modified = True
                print("Correct answer! New score:", request.session['score'])
            
            request.session['current_question_index'] += 1
            request.session.save()

            if request.session['current_question_index'] < len(questions):
                next_question = questions[request.session['current_question_index']]
                return JsonResponse({'question_text': next_question.text, 'answers': [answer.text for answer in next_question.answers.all()]})
            else:
                score = request.session.get('score', 0)
                return JsonResponse({'question_text': 'Вопросы закончились!', 'score': score})

    else:
        request.session['current_question_index'] = 0
        request.session['score'] = 0
        current_question = Question.objects.first()
        context = {'current_question': current_question}
        return render(request, 'myapp/quiz_template.html', context)


def index(request):
    return render(request, 'myapp/index.html')

def result_page(request):
    
    score = request.GET.get('score', 0)  # Получаем значение параметра score из GET-запроса
    # Обработка страницы с результатами
    context = {'score': score}
    
    return render(request, 'myapp/resultpage.html', context)