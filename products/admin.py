from django.contrib import admin
from products.models.albertheijnProducts import AlbertHeijnProduct
from products.models.jumboProducts import JumboProduct
from products.models.proxyList import ProxyList


class AlbertHeijnProductsAdmin(admin.ModelAdmin):
    pass


class JumboProductsAdmin(admin.ModelAdmin):
    pass


class ProxyListAdmin(admin.ModelAdmin):
    pass


admin.site.register(AlbertHeijnProduct, AlbertHeijnProductsAdmin)
admin.site.register(JumboProduct, JumboProductsAdmin)
admin.site.register(ProxyList, ProxyListAdmin)
