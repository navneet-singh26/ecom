import os
import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product


def check_file_path(filepath):
    if os.path.exists(filepath):
        return True

    return False


class Command(BaseCommand):
    help = 'Upload and clean product data from CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filepath',
            type=str,
            help='Specify filepath of the csv file with product data.',
        )

    def handle(self, *args, **kwargs):
        # Load data from CSV
        csv_file_path = kwargs.get('filepath')

        mandatory_columns = ['product_id', 'product_name', 'category', 'price', 'quantity_sold', 'rating', 'review_count']
        if check_file_path(csv_file_path):
            df = pd.read_csv(csv_file_path)

            if not mandatory_columns.issubset(df.columns):
                self.stdout.write(self.style.ERROR('Mandatory columns are missing from data.'))
                return

            # Data cleaning
            df['price'].fillna(df['price'].median(), inplace=True)
            df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
            df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))

            # Ensure numeric types
            df['price'] = pd.to_numeric(df['price'])
            df['quantity_sold'] = pd.to_numeric(df['quantity_sold'])
            df['rating'] = pd.to_numeric(df['rating'])

            # Bulk upload to database
            for index, row in df.iterrows():
                Product.objects.update_or_create(
                    product_id=row['product_id'],
                    defaults={
                        'product_name': row['product_name'],
                        'category': row['category'],
                        'price': row['price'],
                        'quantity_sold': row['quantity_sold'],
                        'rating': row['rating'],
                        'review_count': row['review_count']
                    }
                )
            self.stdout.write(self.style.SUCCESS('Data uploaded and cleaned successfully'))
        else:
            self.stdout.write(self.style.ERROR('File path is invalid.'))
