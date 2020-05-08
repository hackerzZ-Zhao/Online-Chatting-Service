#chatting client
import socket
import json
import threading

client = socket.socket()
client.connect(("127.0.0.1", 8000))

user = "Alice"

#1. login
login_template = {
    "action":"login",
    "user":user
}
client.send(json.dumps(login_template).encode("utf8"))
res = client.recv(1024)
print(res.decode("utf8"))

#2. get active users
get_user_template = {
    "action":"list_user"
}
client.send(json.dumps(get_user_template).encode("utf8"))
res = client.recv(1024)
print("Active Users:{}".format(res.decode("utf8")))

#3. get offline messages
offline_msg_template = {
    "action":"history_msg",
    "user":user
}
client.send(json.dumps(offline_msg_template).encode("utf8"))
res = client.recv(1024)
print("History Messages:{}".format(res.decode("utf8")))

exit = False
def hanle_receive():
    while True:
        if not exit:
            try:
                res = client.recv(1024)
            except:
                break
            res = res.decode("utf8")
            try:
                res_json = json.loads(res)
                msg = res_json["data"]
                from_user = res_json["from"]
                print("")
                print("Get message from ({}): {}".format(from_user, msg))
            except:
                print("")
                print(res)
        else:
            break

def handle_send():
    while True:
        op_type = input("The operation you need: 1. send message, 2. logout, 3. get active users")
        if op_type not in ["1","2","3"]:
            print("Invaild Number!!!")
            op_type = input("The operation you need: 1. send message, 2. logout, 3. get active users")
        elif op_type == "1":
            to_user = input("The person you want to connect:")
            msg = input("Enter your message:")
            send_data_template = {
                "action": "send_msg",
                "to": to_user,
                "from": user,
                "data": msg
            }
            client.send(json.dumps(send_data_template).encode("utf8"))
        elif op_type == "2":
            exit_template = {
                "action": "exit",
                "user": user
            }
            client.send(json.dumps(exit_template).encode("utf8"))
            exit = True
            client.close()
            break
        elif op_type == "3":
            get_user_template = {
                "action": "list_user"
            }
            client.send(json.dumps(get_user_template).encode("utf8"))

if __name__ == "__main__":
    send_thread = threading.Thread(target=handle_send)
    receive_thread = threading.Thread(target=hanle_receive)
    send_thread.start()
    receive_thread.start()




