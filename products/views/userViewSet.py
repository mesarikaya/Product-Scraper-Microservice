from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.userSerializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self):
        return self.request.user

    @action(detail=True, methods=['delete'], name='Delete User')
    def delete_user(self, request, pk=None):
        self.destroy(request)

    def destroy(self, request, *args, **kwargs):
        self.destroy(request)

        return Response(status=204)



