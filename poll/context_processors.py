from poll.models import Question 

def polls_count(request):
    count = Question.objects.count()
    print("Polls count - ", count)
    return {"polls_count": count}