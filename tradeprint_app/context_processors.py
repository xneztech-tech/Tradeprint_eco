from .views import frontend_base_context

def menu_processor(request):
    return frontend_base_context(request)
