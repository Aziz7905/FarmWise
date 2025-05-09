from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RainfallPrediction(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_rainfall = models.FloatField()
    lower_ci = models.FloatField(null=True, blank=True)
    upper_ci = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('region', 'prediction_date')

    def __str__(self):
        return f"{self.region.name} - {self.prediction_date}"
