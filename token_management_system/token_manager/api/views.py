from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, \
    UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from token_management_system.token_manager.api.serializers import TokenSerializer

from token_management_system.token_manager.models import Token


class TokenViewset(RetrieveModelMixin, UpdateModelMixin,
                    DestroyModelMixin, GenericViewSet):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)


    def get_queryset(self):

        return Token.objects.all()

    def list(self, request, *args, **kwargs):
        result = Token.assign()
        if result:
            return Response(data={'token': result }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True,url_path='unblock')
    def unblock(self, request, pk=None):
        object = self.get_object()
        print(object.__dict__)
        print( object.status == Token.FREE)
        print(object.status)
        if object.status == Token.FREE:
            return Response({"success": False, "message":"You can not unblock a free token "}, status=status.HTTP_400_BAD_REQUEST)
        object.unblock_token()
        return Response({"success":True},status=status.HTTP_200_OK)


    @action(methods=['get'], detail=True, url_path='keep-alive')
    def alive(self, request, pk=None):
        object = self.get_object()
        print()
        print(object.status == Token.FREE)
        if object.status == Token.FREE:
            return Response({"success": False, "message": "You can not keep alive a already free token"},
                     status=status.HTTP_400_BAD_REQUEST)
        object.mark_token_alive()
        return Response({"success": True}, status=status.HTTP_200_OK)

# class GetPlanView(ListModelMixin, GenericViewSet):
#     serializer_class = serializers.PlanValiditySerializer
#     permission_classes = (ServerPermission,)
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['customer__user_id', 'customer__product__name']
#
#     def get_queryset(self):
#         return Subscription.objects.filter(expires_at__gte=datetime.date.today()-datetime.timedelta(days=7))


# class HostedPageView(GenericViewSet, CreateModelMixin):
#     serializer_class = serializers.HostedPageSerialzer
#     permission_classes = [ServerPermission]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class PlanPaymentViewSet(GenericViewSet, CreateModelMixin):
#     serializer_class = serializers.HostedPagePaymentSerialzer
#     permission_classes = [ServerPermission]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class RenewSubscriptionPaymentViewSet(GenericViewSet, CreateModelMixin):
#     serializer_class = serializers.SubscriptionRenewPaymentSerialzer
#     permission_classes = [ServerPermission]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
