from django.core.management.base import BaseCommand
import json
from django.contrib.auth.models import User

from authapp.models import ShopUser
from geekshop import settings
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    # {settings.BASE_DIR}/json/{file_name}.json - путь до файла json
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', 'r') as json_file:
        # print(json.load(json_file))
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json("categories")

        # чистим базу
        ProductCategory.objects.all().delete()
        # наполняем
        # **сcategory - распаковка именованных аргументов
        for category in categories:
            ProductCategory.objects.create(**category)

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            # print(f'category_name {category_name}')
            category_item = ProductCategory.objects.get(name=category_name)
            # print(f'category_item {category_item}')
            product['category'] = category_item
            # print(f'product[category] {product["category"]}')
            Product.objects.create(**product)

        ShopUser.objects.create_superuser('django', password='geekbrains', age=18)