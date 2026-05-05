from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Load sample products for testing'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Power Tools', 'slug': 'power-tools', 'description': 'Professional power tools for construction'},
            {'name': 'Hand Tools', 'slug': 'hand-tools', 'description': 'Essential hand tools for every project'},
            {'name': 'Safety Equipment', 'slug': 'safety-equipment', 'description': 'Safety gear and protective equipment'},
            {'name': 'Building Materials', 'slug': 'building-materials', 'description': 'Quality building materials'},
            {'name': 'Fasteners', 'slug': 'fasteners', 'description': 'Bolts, screws, nails and fasteners'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        # Sample products data
        products_data = [
            {
                'category': 'power-tools',
                'name': 'Professional Cordless Drill',
                'slug': 'cordless-drill-pro',
                'description': 'High-powered cordless drill perfect for all drilling and fastening tasks. Features variable speed control and powerful motor.',
                'short_description': 'Cordless drill with variable speed',
                'price': Decimal('4999.00'),
                'discount_price': Decimal('3999.00'),
                'cost_price': Decimal('2500.00'),
                'stock': 50,
                'sku': 'DRILL-PRO-001',
                'manufacturer': 'ToolsPro',
                'weight': 1.8,
                'warranty_months': 24,
            },
            {
                'category': 'hand-tools',
                'name': 'Professional Hammer Set',
                'slug': 'hammer-set',
                'description': 'Complete hammer set with various sizes and ergonomic handles for comfortable use.',
                'short_description': 'Set of 5 hammers with ergonomic handles',
                'price': Decimal('1299.00'),
                'discount_price': Decimal('999.00'),
                'cost_price': Decimal('500.00'),
                'stock': 100,
                'sku': 'HAMMER-SET-001',
                'manufacturer': 'ToolsPro',
                'weight': 2.5,
                'warranty_months': 12,
            },
            {
                'category': 'safety-equipment',
                'name': 'Safety Helmet',
                'slug': 'safety-helmet',
                'description': 'ISO certified safety helmet with comfortable padding and adjustable chin strap.',
                'short_description': 'Safety helmet with comfortable padding',
                'price': Decimal('549.00'),
                'discount_price': None,
                'cost_price': Decimal('250.00'),
                'stock': 200,
                'sku': 'HELMET-SAFE-001',
                'manufacturer': 'SafeGear',
                'weight': 0.35,
                'warranty_months': 6,
            },
            {
                'category': 'building-materials',
                'name': 'Cement Bag 50kg',
                'slug': 'cement-50kg',
                'description': 'High-quality Portland cement suitable for all construction purposes.',
                'short_description': '50kg bag of premium cement',
                'price': Decimal('399.00'),
                'discount_price': Decimal('349.00'),
                'cost_price': Decimal('200.00'),
                'stock': 500,
                'sku': 'CEMENT-50-001',
                'manufacturer': 'CementCorp',
                'weight': 50,
                'warranty_months': None,
            },
            {
                'category': 'fasteners',
                'name': 'Assorted Screw Set',
                'slug': 'screw-set',
                'description': 'Complete box with various types and sizes of screws for all projects.',
                'short_description': 'Box with 1000+ assorted screws',
                'price': Decimal('799.00'),
                'discount_price': Decimal('599.00'),
                'cost_price': Decimal('300.00'),
                'stock': 150,
                'sku': 'SCREW-ASSORT-001',
                'manufacturer': 'FastenerPro',
                'weight': 2,
                'warranty_months': None,
            },
            {
                'category': 'power-tools',
                'name': 'Electric Circular Saw',
                'slug': 'circular-saw',
                'description': 'Powerful circular saw for cutting wood and other materials. Includes safety guards and dust collection.',
                'short_description': 'Electric saw with dust collection',
                'price': Decimal('6999.00'),
                'discount_price': Decimal('5499.00'),
                'cost_price': Decimal('3000.00'),
                'stock': 30,
                'sku': 'SAW-CIRC-001',
                'manufacturer': 'PowerTools',
                'weight': 2.5,
                'warranty_months': 24,
            },
            {
                'category': 'hand-tools',
                'name': 'Adjustable Wrench Set',
                'slug': 'wrench-set',
                'description': 'Set of premium quality adjustable wrenches in various sizes.',
                'short_description': '6-piece adjustable wrench set',
                'price': Decimal('1499.00'),
                'discount_price': Decimal('1199.00'),
                'cost_price': Decimal('600.00'),
                'stock': 80,
                'sku': 'WRENCH-SET-001',
                'manufacturer': 'ToolsPro',
                'weight': 1.5,
                'warranty_months': 12,
            },
            {
                'category': 'safety-equipment',
                'name': 'Work Gloves',
                'slug': 'work-gloves',
                'description': 'Durable work gloves with grip protection for safe handling of materials.',
                'short_description': 'Pair of professional work gloves',
                'price': Decimal('299.00'),
                'discount_price': None,
                'cost_price': Decimal('100.00'),
                'stock': 300,
                'sku': 'GLOVES-WORK-001',
                'manufacturer': 'SafeGear',
                'weight': 0.1,
                'warranty_months': None,
            },
        ]

        for product_data in products_data:
            category = categories[product_data.pop('category')]
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={**product_data, 'category': category, 'is_active': True, 'is_featured': created}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample products!'))
