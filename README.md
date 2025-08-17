# Kafka Orders Demo (Producer/Consumer with Dockerized Kafka)

A minimal end‑to‑end example that spins up **Kafka + Zookeeper** via Docker, then runs a **Python producer** that streams random orders and a **Python consumer** that aggregates stats by category in real time.

> You’ll get from zero to messages flowing in minutes. This README is designed as a step‑by‑step guide with commands you can copy‑paste.

---

## 🚀 What You’ll Build

* **Dockerized Kafka + Zookeeper** (Bitnami images)
* **Python Producer** (`producer.py`) that sends JSON orders to the `orders` topic
* **Python Consumer** (`consumer.py`) that prints running counts, totals, and average by category

---

## ✅ Prerequisites

* **Docker** and **Docker Compose** (Compose V2 works: `docker compose ...`)
* **Python 3.8+** (3.10+ recommended)
* **pip** (Python package manager)

> If you’re on Windows, WSL2 is recommended for the smoothest Docker/Kafka experience.

---

## 🗂 Project Structure

```
.
├─ docker-compose.yml
├─ producer.py
├─ consumer.py
└─ requirements.txt  
```

**requirements.txt** 

```
kafka-python>=2.0.2
```

---

## ⚙️ Docker Compose (Zookeeper mode)

Use the following `docker-compose.yml` (Zookeeper-based; simplified for reliability):

```yaml
version: '3.8'

services:
  zookeeper:
    image: bitnami/zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes

  kafka:
    image: bitnami/kafka:latest
    ports:
      - "9092:9092"
    environment:
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    depends_on:
      - zookeeper
```





## 🏃‍♂️ Quick Start

### 1) Bring up Kafka

```bash
# From the project folder
docker compose up -d

#Create topics mannually is recommended
docker exec -it <kafka_container> bash
kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1



### 3) Set up Python environment

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

```

### 4) Run the consumer (terminal A)

```bash
python consumer.py
```

You should see output like:

```
Starting consumer. Listening for orders...
Category: books | Count: 1 | Total: $57.43 | Avg: $57.43
Category: books | Count: 2 | Total: $130.12 | Avg: $65.06
...
```

### 5) Run the producer (terminal B)

```bash
python producer.py
```

You’ll see:

```
Starting producer. Press Ctrl+C to stop.
Sent order: {'order_id': 1, 'category': 'home', 'amount': 145.77}
Sent order: {'order_id': 2, 'category': 'books', 'amount': 22.09}
...
```

Stop either with **Ctrl+C**.

---

## 🧰 Useful Admin Commands

**Describe topic**

```bash
docker exec -it "$KAFKA_CID" /opt/bitnami/kafka/bin/kafka-topics.sh \
  --describe --topic orders --bootstrap-server localhost:9092
```

**Console consumer (for debugging)**

```bash
docker exec -it "$KAFKA_CID" /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
  --topic orders --bootstrap-server localhost:9092 --from-beginning
```

---

## ❗️Troubleshooting

**1) `NoBrokersAvailable` or connection refused**

* Ensure Docker is running and `docker compose up -d` completed.
* Confirm Kafka is listening on `localhost:9092` from your host (we set `ADVERTISED_LISTENERS` accordingly).
* Some corporate VPNs/security tools block `localhost:9092`; try disabling temporarily or change port.

**2) Producer sends but consumer prints nothing**

* Ensure both point to the same broker `localhost:9092` and the same topic `orders`.
* If you started consumer **after** producing, keep `auto_offset_reset='earliest'` (already set) or start a new consumer group.

**3) Topic not found**

* Create it explicitly with the `kafka-topics.sh --create` command above.

**4) Windows/WSL gotchas**

* Prefer running Python apps on the **same side** (both in Windows or both in WSL) that Docker is bound to.
* If Docker Desktop is on Windows, `localhost:9092` from Windows should work. With WSL, ensure interop is enabled.

**5) Mixed KRaft/Zookeeper configs**

* Use the compose file provided here (Zookeeper only). Don’t mix KRaft and Zookeeper env vars.

---

## ♻️ Stop & Clean Up

```bash
# Stop containers
docker compose down

# Remove containers + volumes (wipes data)
docker compose down -v
```

---


## 💡 FAQ

**Q: Do I need to install Kafka locally?**
A: No. Docker runs Kafka for you.

**Q: Do I have to create the topic?**
A: Many dev images auto-create topics on first publish. Creating it explicitly is more predictable.

**Q: Can I run both apps at once?**
A: Yes—open two terminals: one for `consumer.py`, one for `producer.py`.

---

Happy streaming! If you want, you can extend this with a dashboard or a REST API that shows the live aggregates.
