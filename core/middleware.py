from .models import Customer, Merchant

class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization

    def __call__(self, request):
        # code to be executed for each request before the view (and later the middleware) are called
        # adding customers directly
        if request.user.is_authenticated and not hasattr(request.user, 'customer'):
            Customer.objects.create(user=request.user)

        if request.user.is_authenticated and not hasattr(request.user, 'merchant'):
            Merchant.objects.create(user=request.user)

        response = self.get_response(request)

        # code to be executed for each request/response after the view is called

        return response