from django.db import models

class Simulator(models.Model):
    INTERVAL_CHOICES = [
        ('@hourly', 'Hourly'),
        ('@daily', 'Daily'),
        ('@weekly', 'Weekly'),
        ('@monthly', 'Monthly'),
    ]
    
    start_date = models.DateTimeField()
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    kpi_id = models.IntegerField()
    
    def __str__(self):
        return f"Simulator {self.id} - KPI {self.kpi_id}"