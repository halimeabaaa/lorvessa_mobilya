class MediaCacheMiddleware:
    """Optimize edilmiş medya dosyalarına uzun tarayıcı cache’i ekler."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if path.startswith('/media/') and response.status_code == 200:
            if path.endswith(('.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.woff2')):
                response['Cache-Control'] = 'public, max-age=2592000, immutable'
        elif path.startswith('/static/') and response.status_code == 200:
            response['Cache-Control'] = 'public, max-age=2592000, immutable'
        return response
