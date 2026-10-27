# Спосіб 3: Використання "фасаду" з __init__.py
import shop

print("\n--- Спосіб 3 (через __init__.py) ---")
# Тепер ці функції доступні напряму з 'shop'
products_via_facade = shop.list_products()
customer_via_facade = shop.get_customer_info("CUST-008")
print(f"Товари з фасаду: {products_via_facade}")
print(customer_via_facade)