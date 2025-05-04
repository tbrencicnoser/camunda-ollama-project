# Camunda Ollama Project

## 🚀 Project Overview

This project integrates **Camunda 8** running on an AWS instance with an external AI service (**Ollama mistral model**) and a FastAPI web interface. The system allows users to upload a PDF, extract event data, process it through Camunda, and enrich it with AI-generated outputs using REST connectors.

We also provide a **demo video** in the GitHub repository so you can see the live system in action.

👉 **Demo video:** [See in GitHub repo](./AI-Calender-Demo.mp4 )
👉 **Repository:** [https://github.com/tbrencicnoser/camunda-ollama-project](https://github.com/tbrencicnoser/camunda-ollama-project)

---

## 🎯 Project Goal

The goal was to build a realistic, multi-container application that demonstrates:

* Use of Camunda 8 BPMN process modeling
* Integration of at least one external REST API (Ollama AI)
* User interaction via a web interface
* Automated workflow execution and coordination between components

---

## 🔧 How to Start the System

1️⃣ **Log in to your AWS instance**

```bash
ssh -i Ollama.pem ubuntu@<AWS-IP>
```

2️⃣ **Navigate to the project directory**

```bash
cd ~/camunda-ollama-project
```

3️⃣ **Start all containers using the provided script**

```bash
./start_project.sh
```

This will:

* Build and launch the Docker containers
* Ensure the mistral model is loaded into Ollama
* Restart the web container for connectivity

4️⃣ **Access the system:**

* Web app: http\://<AWS-IP>:5000
* Camunda 8: http\://<AWS-IP>:8080 (if exposed)

---

## 🖥 How to Use the System

✅ **Upload a PDF** via the web interface at port 5000.
✅ The system extracts events and sends them into the Camunda process.
✅ The BPMN process triggers REST calls (via connectors) to Ollama AI.
✅ Results are combined and displayed to the user.

---

## 🔍 Explanation of the Camunda Process

* **Start Event** → triggered by the uploaded data.
* **Service Tasks** → using REST Outbound Connectors to call Ollama API.
* **User Tasks** → configured (optional) for user interaction using Camunda Forms.
* **End Event** → marks process completion and delivers results.

We used:

* At least 4 running containers (Camunda, Ollama, Redis, Web App)
* Docker Compose for orchestration
* Redis as caching backend

---

## 📦 Technologies Used

* Camunda 8 (Zeebe)
* Ollama (mistral model)
* FastAPI (Python)
* Docker + Docker Compose
* Redis
* AWS EC2
* GitHub for version control and demo video hosting

---

## 🏁 Final Notes

This project meets the evaluation criteria for grades **4–5–6**:

* External data integration (Ollama API)
* Realistic, user-facing process
* Advanced AI integration

If you want to test or extend the project:

* Clone the repo
* Follow the startup instructions
* Review the provided BPMN models

