# Import required libraries
import json
import random
import nltk
from nltk.tokenize import word_tokenize

# Load SQL knowledge from JSON file
with open("data.json") as file:
    data = json.load(file)

# Variables to keep track of conversation and quiz
last_intent = None        # stores last SQL topic
quiz_mode = False        # tells if quiz is active
current_q = None         # stores current MCQ
score = 0                # quiz score
total = 0                # total questions attempted
quiz_questions = []      # shuffled list of MCQs
q_index = 0              # which question we are on

# Extract MCQ questions from JSON
mcq_bank = next(item for item in data["intents"] if item["tag"] == "mcq_bank")["questions"]

# Function to display the next quiz question
def ask_question():
    global current_q, q_index

    # If all questions are finished
    if q_index >= len(quiz_questions):
        return None

    # Get current question
    current_q = quiz_questions[q_index]

    q = current_q["q"]
    opts = current_q["options"]

    # Format the MCQ nicely
    return f"MCQ:\n{q}\nA) {opts[0]}\nB) {opts[1]}\nC) {opts[2]}\nD) {opts[3]}\nType A/B/C/D"

# Main function that processes user input
def get_response(user_input):
    global last_intent, quiz_mode, score, total, quiz_questions, q_index

    # Convert user input into tokens using NLP
    tokens = word_tokenize(user_input.lower())

    # If user wants to start quiz mode
    if any(w in tokens for w in ["mcq", "quiz", "test", "practice"]):
        quiz_mode = True
        score = 0
        total = 0

        # Shuffle the MCQ questions so they don't repeat in same order
        quiz_questions = mcq_bank.copy()
        random.shuffle(quiz_questions)

        q_index = 0
        return "Quiz started!\n" + ask_question()

    # If quiz is active and user gives an answer
    if quiz_mode and user_input.upper() in ["A", "B", "C", "D"]:
        idx = ord(user_input.upper()) - ord("A")   # Convert A/B/C/D to index (0-3)
        total += 1

        # Check if answer is correct
        if idx == current_q["answer"]:
            score += 1
            reply = "Correct! ✅"
        else:
            correct = ["A", "B", "C", "D"][current_q["answer"]]
            reply = f"Wrong ❌ Correct answer is {correct}"

        # Move to next question
        q_index += 1
        next_q = ask_question()

        # If no more questions left, end quiz
        if next_q is None:
            quiz_mode = False
            return f"{reply}\n\nQuiz Over! Your Score: {score}/{total}"
        else:
            return reply + "\n\n" + next_q

    # Normal SQL question answering mode
    best_match = None
    max_overlap = 0

    # Find the best matching SQL intent using word overlap
    for intent in data["intents"]:
        if "patterns" not in intent:
            continue

        for pattern in intent["patterns"]:
            pattern_tokens = word_tokenize(pattern.lower())
            overlap = len(set(tokens) & set(pattern_tokens))

            if overlap > max_overlap:
                max_overlap = overlap
                best_match = intent

    # If we found a matching SQL topic
    if best_match:
        last_intent = best_match["tag"]
        return random.choice(best_match["responses"])
    else:
        return "Sorry, I didn't understand that."

# Start the chatbot
print("SQL Chatbot  (type 'quit' to exit)")

while True:
    user = input("You: ")
    if user.lower() == "quit":
        break
    print("Bot:", get_response(user))

