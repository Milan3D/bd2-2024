from django.apps import AppConfig

class BD2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BD_2'

    def ready(self):
        import BD_2.models_mongo  # Import additional model file
        import BD_2.modelsextra  # Import additional model file
