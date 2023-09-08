from django.utils.deprecation import MiddlewareMixin

from assets.models import Type


class AimsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.asset_types = Type.objects.all()
