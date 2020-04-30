from django.urls import path, include
from rest_framework import routers
from products.views import GroupViewSet, UserViewSet
from products.views import AHScrapedDataViewSet, AHProductDetailsViewSet
from products.views import JumboScrapedDataViewSet, JumboProductDetailsViewSet
from products.views import CoopScrapedDataViewSet, CoopProductDetailsViewSet
from products.views import DeenScrapedDataViewSet, DeenProductDetailsViewSet
from products.views import DirkScrapedDataViewSet, DirkProductDetailsViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/save/ah/json', AHScrapedDataViewSet.AHProductView.as_view(), name="ah_jsonLoad"),
    path('api/v1/save/jumbo/json', JumboScrapedDataViewSet.JumboProductView.as_view(), name="jumbo_jsonLoad"),
    path('api/v1/save/coop/json', CoopScrapedDataViewSet.CoopProductView.as_view(), name="coop_jsonLoad"),
    path('api/v1/save/deen/json', DeenScrapedDataViewSet.DeenProductView.as_view(), name="deen_jsonLoad"),
    path('api/v1/save/dirk/json', DirkScrapedDataViewSet.DirkProductView.as_view(), name="dirk_jsonLoad"),
    path('api/v1/ah/get/details', AHProductDetailsViewSet.as_view(), name="ah_loadProductDetails"),
    path('api/v1/jumbo/get/details', JumboProductDetailsViewSet.as_view(), name="jumbo_loadProductDetails"),
    path('api/v1/coop/get/details', CoopProductDetailsViewSet.as_view(), name="coop_loadProductDetails"),
    path('api/v1/deen/get/details', DeenProductDetailsViewSet.as_view(), name="deen_loadProductDetails"),
    path('api/v1/dirk/get/details', DirkProductDetailsViewSet.as_view(), name="dirk_loadProductDetails")
]


