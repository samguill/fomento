from rest_framework.routers import DefaultRouter
from .views import (
    FomentoViewSet
)

router = DefaultRouter()
router.register(r'api/fomento', FomentoViewSet, 'fomento')

urlpatterns = router.urls

