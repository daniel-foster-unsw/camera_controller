import socket
import json

HOST = "127.0.0.1"      # Change if testing over the network
PORT = 5000             # Your server port

request = {
    "version": "1.0",
    "command": "DOWNLOAD_IMAGE",
    "parameters": {
        "filename": "20260704_1652_CAM01_000001.jpg"
    }
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    # Send command
#    s.sendall(json.dumps(request).encode("utf-8"))
    message = json.dumps(request) + "\n"
    s.sendall(message.encode("utf-8"))

    # Receive response
    response = s.recv(4096).decode("utf-8")

    print("Raw response:")
    print(response)

    result = json.loads(response)

    print("\nParsed response:")
    print(f"Status : {result['status']}")
print(f"Message: {result['message']}")

if result["status"] == "OK":
    print(f"Filename : {result['data']['filename']}")
    print(f"Filesize : {result['data']['filesize']}")
else:
    print("Download failed.")