from django.http import JsonResponse

class Process500:
    def __init__(self, get_responce):
        self._get_responce = get_responce

    def __call__(self,request):
        return self._get_responce(request)

    def process_exception(self, request, exception):
        return JsonResponse({
            "success": False,
            "error": str(exception),
        })