from django.http import HttpResponse, JsonResponse
from .tasks import sendEmail
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View


def send_email(request):
    sendEmail.delay()
    return HttpResponse("Done sending")


@method_decorator(cache_page(60), name="dispatch")
class TestView(View):
    def get(self, request, *args, **kwargs):
        response = requests.get(
            "https://53a44309-730f-4fa2-b975-5d339bab22a5.mock.pstmn.io/test/delay/5"
        )
        return JsonResponse(response.json())
