# Task 3 – SQL Chatbot using NLP

This project implements an intelligent SQL Chatbot using Natural Language Processing (NLP). The chatbot is designed to understand user questions related to SQL and provide accurate explanations, examples, and interactive learning support.

The system can:

Answer queries about SQL concepts such as DDL, DML, normalization, CREATE, INSERT, and more

Respond to follow-up questions in a conversational way

Conduct an MCQ-based quiz to test the user’s SQL knowledge and track their score

The goal of this project is to demonstrate how NLP techniques and Python programming can be used to build a smart assistant that helps users learn and practice SQL in an interactive way.

## Objective
To build an AI chatbot using NLP that can answer SQL-related queries and conduct MCQ-based quizzes.

## Features
- Answers SQL concepts (DDL, DML, Normalization, etc.)
- Supports follow-up questions
- MCQ Quiz Mode
- Score tracking

## Technologies Used
- Python
- NLTK
- JSON

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the chatbot:
   python chatbot.py

3. Type:
   - SQL questions (e.g. "what is insert")
   - `mcq` to start quiz

## Example
User: what is normalization  
Bot: Normalization organizes data to reduce redundancy.

