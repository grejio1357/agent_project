# MCP-based AI Search System


## Overview

HA hybrid AI search agent system for agricultural data.

## Problem & Motivation

Agricultural data is largely composed of numerical records such as yields,
making it difficult to retrieve specific measurements or values
for a given period or condition.
At the same time, novice users often require theoretical or explanatory
information that is not easily accessible through structured data queries.

This project was motivated by the need for a unified search system
that supports both structured SQL-based retrieval and
unstructured knowledge retrieval through RAG.

## Key Features

- Rule-based query intent classification using keyword patterns
  to determine whether SQL, RAG, or hybrid retrieval is required
- Dual-agent hybrid retrieval combining SQL-based structured data queries
  with RAG-based unstructured knowledge search
- LangGraph-orchestrated workflow for agent execution and state management
- Unified answer generation integrating results from multiple agents
- Modular architecture enabling easy extension of retrieval agents

## System Architecture
(architecture diagram image)
("agent_project/docs/system_architecture.drawio.png")

## Retrieval Strategy

The system separates retrieval paths for unstructured and structured data.

- For unstructured knowledge retrieval, the RAG agent uses a three-stage pipeline:

1. OpenSearch: performs initial keyword-based filtering to quickly narrow down the candidate set.
2. FAISS: applies semantic similarity search on the reduced set for more precise retrieval.
3. LLM-based reranker: selects the most relevant documents from the FAISS results to feed into the final LLM-generated answer.

- For structured data retrieval, the SQL agent follows a clear pipeline:

1. Intent classification: determines if the query requires structured retrieval.
2. LLM-based text-to-SQL: generates the corresponding SQL statement from the user query.
3. PostgreSQL execution: runs the generated SQL inside a Dockerized database to fetch the actual numerical or categorical data.

This approach ensures that structured queries are accurately translated into SQL and reliably return the correct data for the final answer.

## Development Process

The project began with designing the overall folder structure
and defining clear responsibilities for each agent and service.

The initial development phase focused on the SQL pipeline.
PostgreSQL was set up in a Docker container, and numerical data
from official Korean agricultural statistics sources was ingested
into structured tables. The SQL agent was then implemented and
tested to ensure reliable structured data retrieval.

Next, the RAG pipeline was developed using FAISS for semantic
retrieval. After validating the RAG agent independently,
OpenSearch was integrated to support keyword-based filtering
as the first-stage retriever.

Once both retrieval pipelines were stable, they were orchestrated
using a LangGraph workflow to enable coordinated agent execution.
The backend services were exposed via FastAPI, and finally,
a React-based frontend was implemented to provide a unified
user interface for the entire system.

## Challenges & Solutions

During development, two main challenges were encountered.

- 1 Text-to-SQL Accuracy

The first challenge involved inaccurate SQL generation in
multi-condition queries. In cases where multiple values needed
to be compared simultaneously, the LLM initially generated
queries that retrieved only a single condition.
This issue was resolved through prompt engineering by explicitly
specifying comparison requirements and output constraints,
which significantly improved the accuracy of generated SQL queries.

- 2 Docker Environment Stability

The second challenge was related to Docker container instability.
The problem was resolved by removing existing containers and volumes,
reinitializing the environment, and restarting the services
with a clean Docker setup.

## Tech Stack

- Backend 
  FastAPI

- Orchestration
  LangGraph

- Retrieval & Search
  FAISS (vector-based semantic retrieval)
  OpenSearch (keyword-based retrieval)

- Database
  PostgreSQL

- Frontend
  React

- Infrastructure
  Docker

## How to Run

- Prerequisites
  Docker
  Python 3.10+
  Node.js 18+

- 1. Start required services
  Run the PostgreSQL and OpenSearch containers:

 bash
 docker-compose up -d postgres opensearch

- 2. Run the backend server
  cd backend
  python -m venv venv
  venv/Scripts/activate   
  pip install -r requirements.txt
  uvicorn main:app --reload

- 3. Run the frontend server
  cd frontend
  npm install
  npm start