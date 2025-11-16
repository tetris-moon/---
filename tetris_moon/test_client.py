import socket
import threading

SERVER_IP = "54.180.92.116"   # 서버 IP (같은 PC면 localhost)
SERVER_PORT = 20001


# --------------------------
# 수신 스레드 (서버 메시지 수신용)
# --------------------------
def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(4096).decode()
            if not msg:
                print("[서버 연결 끊김]")
                break
            print(f"[서버] {msg}")
        except Exception as e:
            print(f"[수신 에러] {e}")
            break


# --------------------------
# 메인 로직
# --------------------------
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #온라인에선 host
    client.connect((SERVER_IP, SERVER_PORT))

    print("✅ 서버에 연결되었습니다.")
    print("명령어 예시:")
    print("  /enter   → 입장 메시지 전송 ([Enter])")
    print("  /exit    → 퇴장 메시지 전송 ([Exit])")
    print("  /defeat  → 패배 메시지 전송 ([Defeat])")
    print("  /msg <내용> → 일반 메시지 전송")
    print("  /quit    → 클라이언트 종료\n")

    # 서버로부터 오는 메시지 계속 받기 (백그라운드 스레드)
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    # 사용자 입력 루프
    while True:
        msg = input("> ").strip()
        if msg == "":
            continue

        # 종료 명령
        if msg == "/quit":
            client.close()
            print("👋 연결 종료")
            break

        # 상황별 명령
        elif msg == "/enter":
            client.send("[Enter]".encode())

        elif msg == "/exit":
            client.send("[Exit]".encode())

        elif msg == "/defeat":
            client.send("[Defeat]".encode())

        elif msg.startswith("/msg "):
            content = msg[5:]
            client.send(content.encode())

        else:
            print("⚠️ 알 수 없는 명령입니다. /enter, /exit, /defeat, /msg, /quit 중 선택하세요.")


if __name__ == "__main__":
    main()









