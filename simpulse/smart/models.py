from django.db import models


class GraphsInstallation(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "graphs_installation"


class GraphsCategory(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "graphs_category"


class GraphsData(models.Model):
    installation = models.ForeignKey(
        GraphsInstallation, related_name="data", on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now=True)
    json_data = models.TextField()
    power = models.FloatField()

    def __str__(self):
        return f"{self.installation}_{self.dt}"

    class Meta:
        managed = False
        db_table = "graphs_data"
