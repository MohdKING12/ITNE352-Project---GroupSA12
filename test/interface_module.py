from client_module import connect_to_server, send_username, send_request
import json
import time 

def main():
    
    print("==="*10, "Flight Info Client","==="*10)
   
    name = input("\nEnter your name: ").strip()
    while (not name):
        print("Name cannot be empty.")
        name = input("\nEnter your name: ").strip()
        

    icao = input("Enter ICAO code (e.g., OMDB): ").strip()
    while (not icao):
        print("ICAO cannot be empty.\n")
        icao = input("Enter ICAO code (e.g., OMDB): ").strip()

    try:
        sock = connect_to_server()
        sock.send(icao.encode())        # Send ICAO code first
        time.sleep(2)
        print(f"Connected as {name}")
        send_username(sock, name)          # Then send username
        
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    while True:
        print("\n=== MENU ===")
        print("1. View Arrived Flights")
        print("2. View Delayed Flights")
        print("3. View Flight Details")
        print("4. Quit")

        choice = input("Choose an option: (e.g., 2)").strip()
      
        if choice == '1':
            response = send_request(sock, "1")
            print_response(response)
      
        elif choice == '2':
            response = send_request(sock, "2")
            print_response(response)
      
        elif choice == '3':
            code = input("Enter flight code: ").strip()
      
            if code:
                response = send_request(sock, f"3:{code}")
                print_response(response)
      
        elif choice == '4':
            send_request(sock, "quit")
            print("Disconnected.")
            break
      
        else:
            print("Invalid option.")

def print_response(response):
    if not response:
        print("Sorry, there is no data.")
    elif isinstance(response, (dict, list)):
        print(json.dumps(response, indent=2))
    else:
        print(response)


if __name__ == "__main__":
    main()
