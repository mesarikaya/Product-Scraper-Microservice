from django.db import models


class ProxyList(models.Model):
    proxy = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '{proxyList:' + self.proxyList + '}'
