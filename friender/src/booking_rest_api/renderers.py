from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        code = renderer_context['response'].status_code
        return super().render({'code': code, 'data': data})