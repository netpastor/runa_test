from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

router = DefaultRouter()

router.register(prefix=r"categories", viewset=CategoryViewSet, basename="categories")
urlpatterns = router.urls
