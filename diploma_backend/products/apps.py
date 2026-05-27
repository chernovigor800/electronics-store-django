from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        try:
            import products.signals
            print("Signals imported successfully")
        except Exception as e:
            print("Error importing signals:", e)