class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session.setdefault('request_count', 0)
        request.session['request_count'] += 1
        response = self.get_response(request)
        return response
