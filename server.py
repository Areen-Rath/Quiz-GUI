import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

server.bind((ip_address, port))
server.listen()

clients = []
nicknames = []

print("Server has started...")

questions = [
    "Which of these is an elementary particle?\na. Proton\nb. Neutron\nc. Electron\nd. None of the above",
    "How many laws of thermodynamics are there?\na. 1\nb. 2\nc. 3\nd. 4",
    "Which is the only reptile having 4 chambered heart?\na. Snake\nb. Crocodile\nc. Komodo Dragon\nd. Chameleon",
    "What is the fastest sport in the world?\na. Badminton\nb. Table Tennis\nc. Tennis\nd. Squash",
    "Where did Denim originate from?\na. USA \nb. UK\nc. France\nd. Italy"
]

answers = ["c", "d", "b", "a", "c"]

def client_thread(conn, address):
    score = 0
    conn.send("Welcome to the quiz!".encode("utf-8"))
    conn.send("You will receive a question. Answer it in a, b, c or d.".encode("utf-8"))
    conn.send("Good Luck!\n\n".encode("utf-8"))
    index, question, answer = get_qa(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Correct Answer! Your score is {score}\n\n".encode("utf-8"))
                else:
                    conn.send(f"Incorrect Answer! Better luck next time!\n\n".encode("utf-8"))
                remove_qa(index)
                index, question, answer = get_qa(conn)
                if index == '':
                    break
            else:
                remove(conn)
        except:
            continue
    conn.send(f"We're done! Your final score is {score}.".encode("utf-8"))
    conn.send("Thank you for playing our quiz!")

def get_qa(conn):
    if questions != []:
        index = random.randint(0, len(questions) - 1)
        question = questions[index]
        answer = answers[index]
        conn.send(question.encode("utf-8"))
    else:
        index = ''
        question = ''
        answer = ''
    return index, question, answer

def remove_qa(index):
    questions.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in clients:
        clients.remove(conn)

while True:
    conn, address = server.accept()
    conn.send("nickname".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    
    new_thread = Thread(target= client_thread,args=(conn, nickname))
    new_thread.start()