from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import GroupViewSet, UserViewSet
from products.views import AHScrapedDataViewSet, AHProductDetailsViewSet
from products.views import JumboScrapedDataViewSet, JumboProductDetailsViewSet
from products.views import CoopScrapedDataViewSet, CoopProductDetailsViewSet
from products.views import DeenScrapedDataViewSet, DeenProductDetailsViewSet
from products.views import DirkScrapedDataViewSet, DirkProductDetailsViewSet
from products.views import VomarScrapedDataViewSet, VomarProductDetailsViewSet
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('save/ah/json', AHScrapedDataViewSet.AHProductView.as_view(), name="ah_jsonLoad"),
    path('save/jumbo/json', JumboScrapedDataViewSet.JumboProductView.as_view(), name="jumbo_jsonLoad"),
    path('save/coop/json', CoopScrapedDataViewSet.CoopProductView.as_view(), name="coop_jsonLoad"),
    path('save/deen/json', DeenScrapedDataViewSet.DeenProductView.as_view(), name="deen_jsonLoad"),
    path('save/dirk/json', DirkScrapedDataViewSet.DirkProductView.as_view(), name="dirk_jsonLoad"),
    path('save/vomar/json', VomarScrapedDataViewSet.VomarProductView.as_view(), name="vomar_jsonLoad"),
    path('v1/ah/get/details', AHProductDetailsViewSet.as_view(), name="ah_loadProductDetails"),
    path('v1/jumbo/get/details', JumboProductDetailsViewSet.as_view(), name="jumbo_loadProductDetails"),
    path('v1/coop/get/details', CoopProductDetailsViewSet.as_view(), name="coop_loadProductDetails"),
    path('v1/deen/get/details', DeenProductDetailsViewSet.as_view(), name="deen_loadProductDetails"),
    path('v1/dirk/get/details', DirkProductDetailsViewSet.as_view(), name="dirk_loadProductDetails"),
    path('v1/vomar/get/details', VomarProductDetailsViewSet.as_view(), name="vomar_loadProductDetails")
]


