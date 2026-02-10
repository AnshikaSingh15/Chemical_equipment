from django.db import models

class UploadHistory(models.Model):
    dataset_name = models.CharField(
        max_length=150,
        help_text="Name of the uploaded CSV file"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    total_count = models.PositiveIntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    type_distribution = models.JSONField(
        help_text="Equipment type counts"
    )

    class Meta:
        ordering = ['-uploaded_at']  # newest first
        verbose_name = "Upload History"
        verbose_name_plural = "Upload History"

    def __str__(self):
        return f"{self.dataset_name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
