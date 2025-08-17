import json
from kafka import KafkaConsumer
from collections import defaultdict

# 1. Connect to Kafka and subscribe
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# 2. Aggregation state
category_counts = defaultdict(int)
category_totals = defaultdict(float)

print("Starting consumer. Listening for orders...")

for msg in consumer:
    order = msg.value
    cat = order['category']
    amt = order['amount']

    # Update counts and totals
    category_counts[cat] += 1
    category_totals[cat] += amt

    # Compute average per category
    avg = category_totals[cat] / category_counts[cat]

    # Display running stats
    print(f"Category: {cat} | Count: {category_counts[cat]} | "
          f"Total: ${category_totals[cat]:.2f} | Avg: ${avg:.2f}")
