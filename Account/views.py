from ResponseHandle import exception_handler
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .models import MyUser, SystemAccess
from .serializers import RoleSerializer, MyUserSerializer, SystemAccessSerializer
from ResponseHandle.permissions import IsAdminAuth

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class Role(APIView):
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return exception_handler.error_handling(data=serializer.data, )
        return exception_handler.error_handling(errMsg=serializer.errors)


@api_view(['POST'])
def signup(request):
    if not request.data:
        return exception_handler.error_handling(errMsg="invalid access")

    email = MyUser.objects.filter(email=request.data['email'])

    if len(email) != 0:
        return exception_handler.error_handling(errMsg="Email id is already register.")

    serializer = MyUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        access_request = {
            'user_id': serializer.data['id']
        }
        access_serializer = SystemAccessSerializer(data=access_request)
        if access_serializer.is_valid():
            access_serializer.save()
        return exception_handler.error_handling(data=serializer.data)
    return exception_handler.error_handling(errMsg=serializer.errors)


@api_view(['POST'])
def user_login(request):
    try:
        email = request.data['email']
        password = request.data['password']

        try:
            myuser = MyUser.objects.get(email__exact=email)
        except MyUser.DoesNotExist:
            output = "email is not registered......"
            return exception_handler.error_handling(errMsg=output)

        if not check_password(password, myuser.password):
            output = "password  is wrong"
            return exception_handler.error_handling(errMsg=output)

        user = authenticate(email=email, password=password)
        # refresh = RefreshToken.for_user(user)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            data = {
                'id': user.id,
                'email': user.email,
                'role_id': user.role_id.id,
                'role_type': user.role_id.role_type,
                'token': token,
                # 'access': str(refresh.access_token),
            }
            return exception_handler.error_handling(data=data)
        else:
            output = 'can not authenticate with the given credentials or the account has been deactivated'
            return exception_handler.error_handling(errMsg=output)
    except KeyError:
        output = 'please provide a email and a password'
        return exception_handler.error_handling(errMsg=output)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminAuth])
def get_user_access_detail(request, access_id):
    try:
        access_obj = SystemAccess.objects.get(id=access_id)
    except SystemAccess.DoesNotExist:
        return exception_handler.error_handling(errMsg='id does not exist')

    serializer = SystemAccessSerializer(access_obj)
    return exception_handler.error_handling(data=serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminAuth])
def update_user_access(request, access_id):
    try:
        access_obj = SystemAccess.objects.get(id=access_id)
    except SystemAccess.DoesNotExist:
        return exception_handler.error_handling(errMsg='id does not exist')
    serializer = SystemAccessSerializer(access_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return exception_handler.error_handling(data=serializer.data)
    return exception_handler.error_handling(data=serializer.errors)
