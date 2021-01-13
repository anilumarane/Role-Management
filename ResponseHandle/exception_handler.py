from  rest_framework.response import Response
from rest_framework import status


#==============  error exceptions========================================================
from Account.models import MyUser


def error_handling(errMsg=None, array_error=None, data=None,status_code=None, pagination=None):
    if errMsg:
        error = {"errMsg":errMsg, "status":"FAILED","array_error":array_error, "data":data}
        return Response(error, status = status.HTTP_400_BAD_REQUEST)
    elif array_error:
        result = {"errMsg":errMsg, "status":"FAILED","array_error":array_error, "data":data}
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    elif status_code==200:
        result = {"errMsg": errMsg, "status": "SUCCESS", "array_error": array_error, "data": data}
        return Response(result, status=status.HTTP_200_OK)

    #  delete the item then status code will be call
    elif status_code==204:
        result = {"errMsg": errMsg, "status": "SUCCESS", "array_error": array_error, "data": data}
        return Response(result, status=status.HTTP_200_OK)

    elif pagination:
        result = {"errMsg": errMsg, "status": "SUCCESS", "array_error": array_error,"page_detail":pagination, "data": data,}
        return Response(result, status=status.HTTP_200_OK)

    else:
        result = {"errMsg": errMsg, "status": "SUCCESS", "array_error": array_error, "data": data}
        return Response(result, status=status.HTTP_201_CREATED)


#===================end exceptions================================================================
