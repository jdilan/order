from django.core.management.base import BaseCommand
from order_service.kafka_utils import consume_order_data
from django.conf import settings

class Command(BaseCommand):
    help = 'Run Kafka consumer to consume messages from Kafka topic'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Kafka consumer...")
        consume_order_data()
