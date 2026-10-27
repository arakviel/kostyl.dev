print("Пакет 'shop' ініціалізовано!")

# Імпортуємо ключові функції, щоб їх можна було викликати як shop.list_products()
from .products import list_products, get_product
from .customers import get_customer_info

# Визначаємо, що буде імпортовано через 'from shop import *'
# __all__ = ['list_products', 'get_product', 'get_customer_info']