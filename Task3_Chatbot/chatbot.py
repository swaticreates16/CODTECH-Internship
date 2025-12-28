import json
import random
import nltk
from nltk.tokenize import word_tokenize

with open("sql_data.json") as file:
    data = json.load(file)

last_intent = None
quiz_mode = False
current_q = None
score = 0
total = 0
quiz_questions = []
q_index = 0

mcq_bank = next(item for item in data["intents"] if item["tag"] == "mcq_bank")["questions"]

def ask_question():
    global current_q, q_index
    if q_index >= len(quiz_questions):
        return None

    current_q = quiz_questions[q_index]
    q = current_q["q"]
    opts = current_q["options"]

    return f"MCQ:\n{q}\nA) {opts[0]}\nB) {opts[1]}\nC) {opts[2]}\nD) {opts[3]}\nType A/B/C/D"

def get_response(user_input):
    global last_intent, quiz_mode, score, total, quiz_questions, q_index

    tokens = word_tokenize(user_input.lower())

    # Start quiz
    if any(w in tokens for w in ["mcq", "quiz", "test", "practice"]):
        quiz_mode = True
        score = 0
        total = 0
        quiz_questions = mcq_bank.copy()
        random.shuffle(quiz_questions)
        q_index = 0
        return "Quiz started!\n" + ask_question()

    # Answer quiz
    if quiz_mode and user_input.upper() in ["A", "B", "C", "D"]:
        idx = ord(user_input.upper()) - ord("A")
        total += 1

        if idx == current_q["answer"]:
            score += 1
            reply = "Correct! ✅"
        else:
            correct = ["A","B","C","D"][current_q["answer"]]
            reply = f"Wrong ❌ Correct answer is {correct}"

        q_index += 1
        next_q = ask_question()

        if next_q is None:
            quiz_mode = False
            return f"{reply}\n\nQuiz Over! Your Score: {score}/{total}"
        else:
            return reply + "\n\n" + next_q

    # Normal SQL Q&A
    best_match = None
    max_overlap = 0

    for intent in data["intents"]:
        if "patterns" not in intent:
            continue
        for pattern in intent["patterns"]:
            pattern_tokens = word_tokenize(pattern.lower())
            overlap = len(set(tokens) & set(pattern_tokens))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = intent

    if best_match:
        last_intent = best_match["tag"]
        return random.choice(best_match["responses"])
    else:
        return "Sorry, I didn't understand that."

print("SQL Chatbot  (type 'quit' to exit)")
while True:
    user = input("You: ")
    if user.lower() == "quit":
        break
    print("Bot:", get_response(user))
