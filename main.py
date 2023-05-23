import socket
import threading
import random

def get_random_question_answer(client_socket):
    random_index = random.randint(0, len(questions) - 1)
    question = questions[random_index]
    answer = answers[random_index]
    client_socket.send(question.encode('utf-8'))
    return random_index, question, answer

def clientthread(client_socket):
    client_score = 0
    client_socket.send("Welcome to the Quiz Game!\nInstructions:\n1. Answer the questions correctly.\n2. Each correct answer will earn you 1 point.\n3. Enjoy the game!".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                # Empty message, client disconnected
                break
            if message.lower() == answers[current_index].lower():
                client_score += 1
                client_socket.send("Correct answer! Your score is now {}".format(client_score).encode('utf-8'))
                remove_question(current_index)
                current_index, current_question, current_answer = get_random_question_answer(client_socket)
            else:
                client_socket.send("Incorrect answer. Try again!".encode('utf-8'))
        except Exception as e:
            print("An error occurred:", str(e))
            break

    client_socket.close()
    clients.remove(client_socket)

def remove_question(index):
    del questions[index]
    del answers[index]

questions = [
    "What is the capital of France?",
    "What is the largest planet in our solar system?",
    "Who painted the Mona Lisa?",
    # Add more questions
]

answers = [
    "Paris",
    "Jupiter",
    "Leonardo da Vinci",
    # Add more answers
]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'  
server_port = 12345 

server_socket.bind((server_ip, server_port))
server_socket.listen(5)

print("Server started on {}:{}".format(server_ip, server_port))

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=clientthread, args=(client_socket,)).start()
