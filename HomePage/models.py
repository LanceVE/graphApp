from django.db import models
from django.core.validators import FileExtensionValidator


class GraphModel(models.Model):
    graph = models.FileField(upload_to='graph/upload/', validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    def __str__(self):
        return self.title





