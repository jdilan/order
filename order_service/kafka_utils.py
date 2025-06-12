from confluent_kafka import Producer, Consumer
from django.conf import settings
from django.db import transaction

from .models import Order, OrderItem # Import the model where you want to save the data
import json

# Initialize Kafka Producer
producer = Producer({'bootstrap.servers': settings.KAFKA_CONFIG['bootstrap.servers']})

def delivery_report(err, msg):
    """Callback function for Kafka Producer to check delivery status."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_order_update(topic, data_json):
    """Function to send data to Kafka."""
    producer.produce(topic, data_json, callback=delivery_report)
    producer.flush()  # Ensure all messages are sent

# Initialize Kafka Consumer
consumer_order = Consumer({
    'bootstrap.servers': settings.KAFKA_CONFIG['bootstrap.servers'],
    'group.id': settings.KAFKA_CONFIG['group.id'],
    'auto.offset.reset': settings.KAFKA_CONFIG['auto.offset.reset']
})

def consume_order_data():
    """Function to consume messages from Kafka."""
    consumer_order.subscribe([settings.KAFKA_TOPIC_ORDER_NEW, settings.KAFKA_TOPIC_ORDER_UPDATE])

    try:
        while True:
            msg = consumer_order.poll(1.0)  # Timeout of 1 second
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            print(f"Consumer Order Received message: {msg.value().decode('utf-8')}")
            
            topic = msg.topic()

            # Convert the Kafka message back to Python Dict
            order_data = json.loads(msg.value().decode('utf-8'))

            if topic == settings.KAFKA_TOPIC_ORDER_NEW:
                # Save the ORDER to the PostgreSQL database
                # Order.objects.create(**data)
                save_order_to_db(order_data)

                print(f"Record created for order: {order_data}")

                order_data_update = {
                    'order_id':order_data['order_id'],
                    'status':'CREATED'
                }

                # Send order update to KAFKA BROKER
                send_order_update(settings.KAFKA_TOPIC_ORDER_CREATED, json.dumps(order_data_update))

                print(f"Order update sent to kafka: {order_data_update}")
            
            elif topic == settings.KAFKA_TOPIC_ORDER_UPDATE:
                update_order_status(order_data)

    except KeyboardInterrupt:
        pass
    finally:
        consumer_order.close()


def update_order_status(order_data):
    order_id = order_data['order_id']
    order = Order.objects.get(order_id=order_id)
    order.status = order_data['status']
    order.save()


@transaction.atomic
def save_order_to_db(order_data):
    """
    Save order and its items to the database using Django ORM
    """
    # Save order first
    order = Order.objects.create(
        order_id=order_data['order_id'],
        customer_id=order_data['customer_id'],
        order_date=order_data['order_date'],
        shipped_date=order_data['shipped_date'],
        status=order_data['status'],
        email=order_data['email']
    )
    
    # Save each item
    items = order_data.get('items', [])
    for item in items:
        OrderItem.objects.create(
            order_id=order,  # Link the item to the order
            name=item['name'],
            quantity=item['quantity'],
            price=item['price']
        )
