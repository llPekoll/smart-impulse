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
        ventillation_values = [[json.loads(d.json_data).get("2"), d.dt] for d in data]
        eclairage_values = [[json.loads(d.json_data).get("3"), d.dt] for d in data]
        assenseur_values = [[json.loads(d.json_data).get("6"), d.dt] for d in data]
        traitement_values = [[json.loads(d.json_data).get("7"), d.dt] for d in data]
        puissance_values = []
        for d in data:
            ventil = json.loads(d.json_data).get("2")/6 if json.loads(d.json_data).get("2") else 0
            eclairage = json.loads(d.json_data).get("3")/6 if json.loads(d.json_data).get("3") else 0
            assenseur = json.loads(d.json_data).get("6")/6 if json.loads(d.json_data).get("6") else 0
            traitement = json.loads(d.json_data).get("7")/6 if json.loads(d.json_data).get("7") else 0
            all_val = (
                ventil,
                eclairage,
                assenseur,
                traitement
            )
            puissance_values.append([sum(all_val), d.dt])

        return JsonResponse(
            {
                "ventilation": ventillation_values,
                "eclairage": eclairage_values,
                "traitement": traitement_values,
                "puissance": puissance_values,
                "assenseurs": assenseur_values,
            }
        )
