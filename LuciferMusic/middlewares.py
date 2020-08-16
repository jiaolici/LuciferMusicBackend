# 中间件
from django.utils.deprecation import MiddlewareMixin
class MediaMiddleware(MiddlewareMixin):
    def process_response(self,request, response):
        if(request.path.startswith("/media/audio/")):
            #chrome必须设置这两个，才能设置audio的currentTime
            response["Content-type"] = "application/octet-stream"
            response["Accept-Ranges"] = "bytes"
        return response