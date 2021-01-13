from Account.models import Question
from Account.serializers import QuestionSerializer
from ResponseHandle import exception_handler
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ResponseHandle.permissions import IsUserWrite, IsUserRead, IsUserUpdate, IsUserDelete


@api_view(['GET'])
def get_questions(request):
    question = Question.objects.all().values()
    return exception_handler.error_handling(data=question, status_code=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, question_id):
    result = IsUserRead(request.user.id)
    if result:
        return exception_handler.error_handling(result)


    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        exception_handler.error_handling(errMsg='id does not exist', )
    serializer = QuestionSerializer(question)
    return exception_handler.error_handling(data=serializer.data, status_code=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_question(request, question_id):
    result = IsUserUpdate(request.user.id)
    if result:
        return exception_handler.error_handling(result)

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return exception_handler.error_handling(errMsg='id does not exist', )

    serializer = QuestionSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return exception_handler.error_handling(data=serializer.data, status_code=200)
    return exception_handler.error_handling(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    result = IsUserWrite(request.user.id)
    if result:
        return exception_handler.error_handling(result)
    request.data['user_id'] = request.user.id
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return exception_handler.error_handling(data=serializer.data)
    return exception_handler.error_handling(errMsg=serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_question(request, role_id):
    result = IsUserDelete(request.user.id)
    if result:
        return exception_handler.error_handling(result)
    try:
        question = Question.objects.get(id=role_id)
    except Question.DoesNotExist:
        exception_handler.error_handling(errMsg='role id does not exist', )
    question.delete()
    return exception_handler.error_handling(data='role id delete succefully', status_code=200)
