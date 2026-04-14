from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from coderr_app.models import Offer, OfferDetail
from coderr_app.api.serializer import OfferDetailSerializer, UserSerializer, OfferSerializer, OfferDetailListSerializer


class OfferView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = [IsAuthenticated]

    #Nur Boards anzeigen, wo User Owner oder Mitglied ist
    def get_queryset(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    #GET Liste
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    #POST 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Setzt den business_user auf den aktuell angemeldeten Benutzer
        serializer.save(business_user=self.request.user)

class OfferSingleView (mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView,):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = [IsAuthenticated, IsOfferMemberOrOwner]

    #GET 
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    #PATCH 
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    #DELETE 
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
 
