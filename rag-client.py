import socket
import time

SOCKET_TYPE = "internet"  # "internet" or "local"
SOCKET_PATH = "/tmp/gymapp_rag_llm.sock"
HOST = ''
PORT = 6000 # 6000 is cache 5000 is llm
END_MARKER = b"##__END__##"

def chat_session():
    print("🤝 Connected to GymApp RAG. Type 'exit' or 'quit' to end.")

    while True:
        try:
            prompt = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Exiting session.")
            break

        if prompt.lower() in {"exit", "quit"}:
            break
        if not prompt:
            continue

        try:
            if SOCKET_TYPE == "local":
                client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client.connect(SOCKET_PATH)
            elif SOCKET_TYPE == "internet":
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))
            else:
                raise ValueError("❌ Invalid SOCKET_TYPE. Use 'local' or 'internet'.")

            with client:
                client.sendall(prompt.encode("utf-8"))
                print("🤖 ", end="", flush=True)

                buffer = b""
                start_time = time.perf_counter()

                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    buffer += data
                    print(data.decode("utf-8"), end="", flush=True)
                    if buffer.endswith(END_MARKER):
                        break

                end_time = time.perf_counter()
                elapsed = end_time - start_time
                print(f"\n⏱️ Took {elapsed:.2f} seconds.\n")

        except FileNotFoundError:
            print(f"\n❌ Socket not found at {SOCKET_PATH}")
        except (ConnectionResetError, BrokenPipeError):
            print("\n❌ Connection error.")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    chat_session()
