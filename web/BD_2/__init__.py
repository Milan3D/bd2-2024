import django
django.setup()  # Ensure Django is fully loaded before importing

from .models_mongo import *  # Import additional model file
from .modelsextra import *
