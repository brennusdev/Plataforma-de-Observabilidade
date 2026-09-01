# 🔭 Observability Platform

> Plataforma de observabilidade distribuída para monitoramento, diagnóstico e análise de sistemas modernos.

A **Observability Platform** é uma plataforma construída em Python para centralizar métricas, logs, traces, alertas, SLOs, incidentes, dependências e informações de performance de aplicações e infraestrutura.

O projeto foi desenvolvido com foco em **engenharia de software, observabilidade, SRE, sistemas distribuídos, confiabilidade e análise operacional**.

A plataforma evolui progressivamente de um sistema de monitoramento tradicional para uma solução capaz de **correlacionar sinais, identificar causas prováveis, analisar impacto e antecipar problemas**.

---

## 🎯 Objetivo

O objetivo do projeto é responder não apenas:

> **"O sistema está funcionando?"**

mas também:

> **"O que está acontecendo?"**

> **"Por que aconteceu?"**

> **"Qual serviço causou o problema?"**

> **"Quais componentes serão afetados?"**

> **"Qual é o impacto para o usuário?"**

> **"Esse comportamento é uma anomalia?"**

> **"Podemos detectar o problema antes de virar um incidente?"**

A plataforma combina diferentes sinais de observabilidade para construir uma visão operacional integrada da aplicação.

---

# 🧠 Conceito

A arquitetura é baseada nos principais pilares de observabilidade:

```text
                    ┌───────────────┐
                    │   APPLICATION │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       METRICS             LOGS             TRACES
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                  OBSERVABILITY ENGINE
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       ALERTING          INCIDENTS          SLO
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                  INCIDENT INTELLIGENCE
                            │
                            ▼
                   ROOT CAUSE ANALYSIS
                            │
                            ▼
                  DEPENDENCY GRAPH
                            │
                            ▼
                    BLAST RADIUS
                            │
                            ▼
                 CONTINUOUS PROFILING
```

---

# 🚀 Principais funcionalidades

## 📊 Metrics

Coleta e exposição de métricas operacionais:

* throughput;
* latência;
* taxa de erros;
* utilização de CPU;
* utilização de memória;
* consumer lag;
* processadores ativos;
* métricas customizadas;
* métricas de infraestrutura.

As métricas podem ser expostas para sistemas de monitoramento compatíveis com Prometheus.

---

## 📝 Centralized Logging

Sistema estruturado de logging para permitir:

* correlação de eventos;
* identificação de erros;
* níveis de severidade;
* timestamps;
* contexto da requisição;
* identificação do serviço;
* análise de incidentes.

Exemplo conceitual:

```text
timestamp
service
level
trace_id
request_id
message
metadata
```

---

## 🔎 Distributed Tracing

A plataforma acompanha requisições através de diferentes componentes:

```text
Client
  │
  ▼
API Gateway
  │
  ├──────► User Service
  │
  ├──────► Order Service
  │
  └──────► Payment Service
                │
                ▼
             Database
```

Isso permite investigar onde uma requisição gastou tempo e quais serviços participaram da operação.

---

# 🚨 Alerting

O sistema permite identificar condições anormais através de regras de alerta.

Exemplos:

```text
CPU > 80%
```

```text
Error Rate > 5%
```

```text
Latency P95 > 500ms
```

```text
Consumer Lag > Threshold
```

Os alertas podem ser relacionados a serviços, infraestrutura e indicadores de confiabilidade.

---

# 🎯 SLO & Error Budget

A plataforma possui suporte conceitual para **Service Level Objectives (SLOs)** e **Error Budgets**.

Exemplo:

```text
SLO
99.9% availability
```

Error Budget:

```text
0.1%
```

Isso permite relacionar disponibilidade técnica com confiabilidade operacional.

---

# 🧩 Incident Intelligence

A plataforma não trata um alerta simplesmente como uma notificação.

Um incidente passa por um processo de análise:

```text
Alert
  ↓
Incident
  ↓
Signal Correlation
  ↓
Service Analysis
  ↓
Root Cause Candidates
  ↓
Impact Analysis
```

O objetivo é reduzir o tempo necessário para descobrir a origem de uma falha.

---

# 🌐 Dependency Graph

A partir da V12, a plataforma passou a representar relações entre serviços.

Exemplo:

```text
                 FRONTEND
                     │
                     ▼
                API GATEWAY
                 /       \
                /         \
               ▼           ▼
            REDIS       POSTGRES
                           │
                           ▼
                          KAFKA
                           │
                           ▼
                         WORKER
```

Isso permite analisar:

* dependências;
* serviços críticos;
* caminhos de comunicação;
* componentes upstream;
* componentes downstream;
* possíveis single points of failure.

---

# 💥 Blast Radius Analysis

Uma das funcionalidades centrais da plataforma é calcular o possível impacto de uma falha.

Exemplo:

```text
POSTGRES
   │
   ▼
API GATEWAY
   │
   ▼
FRONTEND
```

Se PostgreSQL apresentar uma falha:

```text
POSTGRES
   │
   ├── API GATEWAY
   │
   └── FRONTEND
```

A plataforma consegue estimar quais componentes podem ser afetados e calcular um **impact score**.

---

# 🔬 Continuous Profiling

Na V13 foi introduzido o mecanismo de profiling.

O objetivo é responder:

> **Onde exatamente o processo está gastando recursos?**

Exemplo:

```text
CPU HOTSPOTS

process_request()        47%
serialize_response()     31%
database_query()         15%
middleware()              7%
```

Também são analisadas alocações e alterações de memória.

A implementação utiliza ferramentas nativas do ecossistema Python, como:

* `cProfile`;
* `pstats`;
* `tracemalloc`.

---

# 🏗️ Arquitetura

Estrutura atual do projeto:

```text
observability-platform/
│
├── app/
│   │
│   ├── api/
│   │   ├── dependency_routes.py
│   │   ├── profiling_routes.py
│   │   └── ...
│   │
│   ├── dependency/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── blast_radius.py
│   │   ├── edge.py
│   │   ├── graph.py
│   │   └── node.py
│   │
│   ├── profiling/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── cpu.py
│   │   ├── memory.py
│   │   ├── profiler.py
│   │   └── snapshot.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── dependency.py
│   │   ├── profiling.py
│   │   └── ...
│   │
│   ├── observability/
│   │   ├── metrics.py
│   │   ├── dependency_metrics.py
│   │   └── profiling_metrics.py
│   │
│   └── main.py
│
├── tests/
│   │
│   ├── dependency/
│   │   ├── test_analyzer.py
│   │   ├── test_blast_radius.py
│   │   └── test_graph.py
│   │
│   ├── profiling/
│   │   ├── test_analyzer.py
│   │   ├── test_cpu.py
│   │   └── test_profiler.py
│   │
│   └── ...
│
├── database/
│
├── docker/
│
├── docs/
│
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# 🛠️ Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Pytest

## Observability

* Prometheus
* OpenTelemetry
* Distributed Tracing
* Structured Logging
* Continuous Profiling

## Database

* MySQL / PostgreSQL

## Infrastructure

* Docker
* Docker Compose
* Linux

## Frontend

* HTML
* CSS
* JavaScript

---

# 🐳 Docker

O ambiente pode ser executado utilizando containers.

Arquitetura conceitual:

```text
                 Docker Compose
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      API          DATABASE       PROMETHEUS
        │
        │
        ▼
   OBSERVABILITY
      ENGINE
```

Isso permite reproduzir o ambiente de desenvolvimento de maneira consistente.

---

# ⚙️ Instalação

Clone o repositório:

```bash
git clone <repository-url>
```

Entre no diretório:

```bash
cd observability-platform
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

---

# 🐳 Executando com Docker

Construa os containers:

```bash
docker compose build
```

Execute:

```bash
docker compose up
```

Para executar em background:

```bash
docker compose up -d
```

Verifique os containers:

```bash
docker compose ps
```

---

# 🧪 Testes

O projeto utiliza Pytest.

Execute:

```bash
pytest
```

Com informações detalhadas:

```bash
pytest -v
```

Exemplo:

```text
============================= test session =============================

tests/dependency/test_graph.py ........
tests/dependency/test_blast_radius.py ..
tests/dependency/test_analyzer.py ...
tests/profiling/test_cpu.py ..
tests/profiling/test_profiler.py ..
tests/profiling/test_analyzer.py ..

============================== PASSED ==================================
```

---

# 🔌 API

A aplicação disponibiliza endpoints para interação com os mecanismos de observabilidade.

## Dependency Graph

Criar serviço:

```http
POST /api/dependencies/services
```

Criar dependência:

```http
POST /api/dependencies/relationships
```

Consultar grafo:

```http
GET /api/dependencies/graph
```

Analisar serviço:

```http
GET /api/dependencies/services/{service_name}
```

---

## Continuous Profiling

Executar profiling:

```http
POST /api/profiling/run
```

Exemplo:

```json
{
  "service": "api-gateway"
}
```

---

# 📈 Observability Flow

Uma requisição pode seguir o seguinte fluxo:

```text
REQUEST
   │
   ▼
MIDDLEWARE
   │
   ├──────────────► LOG
   │
   ├──────────────► METRIC
   │
   └──────────────► TRACE
                         │
                         ▼
                  SERVICE ANALYSIS
                         │
                         ▼
                  DEPENDENCY GRAPH
                         │
                         ▼
                  INCIDENT ENGINE
                         │
                         ▼
                   RCA ENGINE
                         │
                         ▼
                  IMPACT ANALYSIS
```

---

# 🧱 Roadmap

O projeto está sendo desenvolvido de forma incremental.

| Versão  | Foco                            | Status |
| ------- | ------------------------------- | ------ |
| V1      | Foundation                      | ✅      |
| V2      | Structured Logging              | ✅      |
| V3      | Alerting                        | ✅      |
| V4      | Application Metrics             | ✅      |
| V5      | Prometheus + Grafana            | ✅      |
| V6      | Distributed Tracing             | ✅      |
| V7      | Production Observability        | ✅      |
| V8      | Resilience Engineering          | ✅      |
| V9      | Chaos Engineering               | ✅      |
| V10     | SLO + Error Budget              | ✅      |
| V11     | Incident Intelligence + RCA     | ✅      |
| V12     | Dependency Graph + Blast Radius | ✅      |
| **V13** | **Continuous Profiling**        | **✅**  |
| V14     | Anomaly Detection               | 🔜     |
| V15     | Predictive Reliability          | 🔜     |
| V16     | Automated Incident Response     | 🔜     |
| V17     | AI Reliability Copilot          | 🔜     |
| V18     | Self-Healing Infrastructure     | 🔜     |

---

# 🧭 Evolução arquitetural

A evolução do projeto segue uma estratégia deliberada:

```text
V1–V4
OBSERVE
   │
   ▼
V5–V7
CORRELATE
   │
   ▼
V8–V10
MEASURE RELIABILITY
   │
   ▼
V11
UNDERSTAND INCIDENTS
   │
   ▼
V12
UNDERSTAND DEPENDENCIES
   │
   ▼
V13
UNDERSTAND PERFORMANCE
   │
   ▼
V14
DETECT ANOMALIES
   │
   ▼
V15
PREDICT FAILURES
   │
   ▼
V16
RESPOND AUTOMATICALLY
   │
   ▼
V17
ASSIST ENGINEERS
   │
   ▼
V18
CONTROLLED SELF-HEALING
```

---

# 🔐 Princípios de engenharia

O projeto segue alguns princípios fundamentais:

### Separation of Concerns

Cada componente possui uma responsabilidade bem definida.

### Observability by Design

Observabilidade não é tratada como funcionalidade adicionada posteriormente.

### Fail Fast

Falhas devem ser detectadas e reportadas rapidamente.

### Explicit Dependencies

Dependências entre serviços devem ser conhecidas e mensuráveis.

### Testability

Componentes críticos devem possuir testes automatizados.

### Reproducibility

O ambiente deve ser reproduzível através de containers.

### Incremental Architecture

Cada versão adiciona uma capacidade arquitetural significativa.

### Human-in-the-Loop

Automação de incidentes deve possuir mecanismos de segurança e controle antes de executar ações potencialmente destrutivas.

---

# 📚 Objetivos de aprendizado

Além de funcionar como aplicação, o projeto foi desenvolvido para consolidar conhecimentos em:

* Python;
* programação orientada a objetos;
* APIs REST;
* FastAPI;
* SQL;
* bancos relacionais;
* Docker;
* Linux;
* métricas;
* logging;
* tracing;
* Prometheus;
* OpenTelemetry;
* sistemas distribuídos;
* arquitetura de software;
* testes automatizados;
* SRE;
* engenharia de confiabilidade;
* análise de performance;
* profiling;
* detecção de anomalias;
* automação operacional.

---

# 📊 Estado atual

### V13 — Continuous Profiling

A plataforma atualmente possui uma arquitetura capaz de trabalhar com:

```text
                    OBSERVABILITY PLATFORM
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
     METRICS                LOGS                 TRACES
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                     INCIDENT INTELLIGENCE
                              │
                              ▼
                         RCA ENGINE
                              │
                              ▼
                     DEPENDENCY GRAPH
                              │
                              ▼
                       BLAST RADIUS
                              │
                              ▼
                   CONTINUOUS PROFILING
                              │
                              ▼
                      PERFORMANCE DATA
```

A próxima etapa será transformar esses dados em **detecção automática de comportamento anômalo**.

---

# 🚧 Próxima versão

## V14 — Anomaly Detection

A V14 introduzirá um mecanismo capaz de diferenciar:

```text
NORMAL
   │
   │
   ├── CPU: 20–35%
   ├── Latency P95: 120–180ms
   └── Error Rate: < 1%
```

de:

```text
ANOMALY
   │
   ├── CPU: 82%
   ├── Latency P95: 740ms
   └── Error Rate: 8.4%
```

O objetivo será detectar mudanças significativas de comportamento em vez de depender exclusivamente de thresholds estáticos.

---

# 🏆 Visão final

A visão de longo prazo da plataforma é evoluir de:

```text
MONITORING
```

para:

```text
OBSERVABILITY
```

depois:

```text
INTELLIGENCE
```

e finalmente:

```text
RELIABILITY AUTOMATION
```

A arquitetura final deverá ser capaz de:

```text
OBSERVE
   ↓
CORRELATE
   ↓
UNDERSTAND
   ↓
DETECT
   ↓
PREDICT
   ↓
RESPOND
   ↓
RECOVER
```

---

## 👨‍💻 Projeto

**Observability Platform**

Projeto desenvolvido com foco em engenharia de software, observabilidade e confiabilidade de sistemas distribuídos.

```text
Python • FastAPI • SQL • Docker
Prometheus • OpenTelemetry • Pytest
SRE • Distributed Systems • Reliability Engineering
```

> Este projeto é desenvolvido como um laboratório de engenharia para estudar e implementar, de forma incremental, conceitos utilizados em plataformas modernas de observabilidade e confiabilidade.
