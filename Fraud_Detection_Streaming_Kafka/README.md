 🔍 Real-Time Fraud Detection with Kafka & PySpark

This mini-project demonstrates a **real-time fraud detection pipeline** using:
- **Apache Kafka** (KRaft mode, no Zookeeper)
- **Python Streaming**
- **Docker Compose**

It simulates a stream of credit card transactions and uses basic business rules to detect potential frauds in real-time.

---

## 🏗️ Project Architecture

![image](https://github.com/user-attachments/assets/955cc503-a211-4585-8727-34b6a70cf64a)

🚀 How to Run

1. Clone the Repo
git clone https://github.com/shrirupdwivedi/Data-Engineering-Portfolio.git
cd Data-Engineering-Portfolio/Fraud_Detection_Streaming_Kafka
2. Start Kafka
docker-compose -f docker-compose.kafka.yml up -d
Wait until logs say: Kafka Server started.
3. Start Generator + Detector Services
docker-compose up --build -d
💡 What It Does

generator: Simulates 1000 transactions per second and pushes to Kafka topic queueing.transactions.
detector: Listens to this topic, applies simple rules, and routes messages to:
streaming.transactions.legit
streaming.transactions.fraud

