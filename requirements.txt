import json
import random
import time
from kafka import KafkaProducer

# 1. Connect to Kafka broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

categories = ['electronics', 'books', 'clothing', 'home']
order_id = 1

def generate_order():
    global order_id
    order = {
        'order_id': order_id,
        'category': random.choice(categories),
        'amount': round(random.uniform(10.0, 200.0), 2)
    }
    order_id += 1
    return order

if __name__ == '__main__':
    print("Starting producer. Press Ctrl+C to stop.")
    try:
        while True:
            order = generate_order()
            producer.send('orders', value=order)
            print(f"Sent order: {order}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Producer stopped.")
        producer.close()
