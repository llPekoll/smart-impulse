import json
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import GraphsData, GraphsInstallation, GraphsCategory

from rest_framework import serializers
from rest_framework import mixins
from rest_framework import generics


class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphsInstallation
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphsCategory
        fields = "__all__"


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphsData
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "json_data": json.loads(instance.json_data),
            "dt": instance.dt,
            "power": instance.power,
            "installation": instance.installation.name,
        }


class InstallationList(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = GraphsInstallation.objects.all()
    serializer_class = InstallationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryList(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = GraphsCategory.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DataList(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = GraphsData.objects.all()
    serializer_class = DataSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetPointCloud(APIView):
    def get(self, request):
        data = GraphsData.objects.all()
        ventillation_values = [[json.loads(d.json_data).get('2')/6,d.dt] for d in data if json.loads(d.json_data).get('2')]
        eclairage_values = [[json.loads(d.json_data).get('3')/6,d.dt] for d in data if json.loads(d.json_data).get('3')]
        traitement_values = [[json.loads(d.json_data).get('7')/6,d.dt] for d in data if json.loads(d.json_data).get('7')]

        return JsonResponse({"ventilation": ventillation_values, "eclairage": eclairage_values, "traitement": traitement_values})
