from django.urls import include, path

from .routers import router

#app_name = 'fomento'

urlpatterns = [
    path('', include(router.urls)),
]