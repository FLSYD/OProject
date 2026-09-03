from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def success(data=None, msg="操作成功", status=200):
    return Response({"code": status, "msg": msg, "data": data}, status=status)


def error(msg, status=400, data=None):
    return Response({"code": status, "msg": msg, "data": data}, status=status)


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    message = "请求失败"
    if isinstance(response.data, dict) and response.data.get("detail"):
        message = str(response.data["detail"])
    return Response({"code": response.status_code, "msg": message, "data": response.data}, status=response.status_code)

