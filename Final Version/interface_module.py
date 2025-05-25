from client_module import connect_to_server, send_username, send_request
import json
import time 
from api import get_flights_by_airport_code

def main():
    
    print("==="*10, "Flight Info Client","==="*10)
   
    name = input("\nEnter your name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("\nEnter your name: ").strip()
        

    icao = input("Enter ICAO code (e.g., OMDB): ").strip()
   
    while not icao:
        print("ICAO cannot be empty.\n")
        icao = input("Enter ICAO code (e.g., OMDB): ").strip()
   
    try:
        flight = get_flights_by_airport_code(icao)
        if not flight:
            return
    except Exception as e:
        print(f"Error fetching flight data: {e}")
        return

    try:
        sock = connect_to_server()
        if not sock:
            print("Failed to connect to server")
            return
            
        sock.send(icao.encode())        # Send ICAO code first
        time.sleep(2)
        print(f"Connected as {name}")
        send_username(sock, name)          # Then send username
        
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    while True:
        try:
            print("\n=== MENU ===")
            print("1. View Arrived Flights")
            print("2. View Delayed Flights")
            print("3. View Flight Details")
            print("4. Quit")

            choice = input("Choose an option (e.g., 2): ").strip()
          
            if choice == '1':
                try:
                    s = send_request(sock, "1")
                    if s is None:
                        print("Error: No response from server")
                        continue
                        
                    if isinstance(s, str):
                        print(s)
                        continue
                        
                    print(f"\n\n\nFound {len(s)} flights:")
                    print("-" * 80)# Separator line
                    
                    # Print each flight on a single line
                    for i, flight in enumerate(s, start=1):

                        print(f"Flight #{i}:")
                        for key, value in flight.items():
                        
                            if isinstance(value, dict):
                                for ik, iv in value.items():
                                    print(f"{ik} : {iv}")
                        
                            else:
                                print(f"{key} : {value}")    
                       
                        print("-" * 80)

                except Exception as e:
                    print(f"Error processing arrived flights: {e}")
          
            elif choice == '2':   
                try:
                    s = send_request(sock, "2")
                    if s is None:
                        print("Error: No response from server")
                        continue
                        
                    if isinstance(s, str):
                        print(s)
                        continue
                        
                    print(f"\n\n\nFound {len(s)} flights:")
                    print("-" * 80)# Separator line
                    
                    # Print each flight on a single line
                    for i, flight in enumerate(s, start=1):
                       
                        print(f"Flight #{i}:")
                        for key, value in flight.items():
                       
                            if isinstance(value, dict):
                                for ik, iv in value.items():
                                    print(f"{ik} : {iv}")
                       
                            else:
                                print(f"{key} : {value}")    
                       
                       
                        print("-" * 80)
                        
                except Exception as e:
                    print(f"Error processing delayed flights: {e}")
          
            elif choice == '3':
                try:
                    code = input("Enter flight code: ").strip()
              
                    if code:
                        s = send_request(sock, f"3:{code}")
                        if s is None:
                            print("Error: No response from server")
                            continue
                            
                        print('\n\n\n')
                        print("-" * 80)
                        
                        if isinstance(s, dict):
                            for key, value in s.items():    
                                print(f"{key} : {value}")
                        else:
                            print(s)  # Print as string if not dict
                            
                        print("-" * 80)
                    else:
                        print("Flight code cannot be empty")
                except Exception as e:
                    print(f"Error processing flight details: {e}")

            elif choice == '4':
                try:
                    send_request(sock, 'quit')
                    print("\nDisconnected.")
                    break
                except Exception as e:
                    print(f"Error during disconnect: {e}")
                    break
          
            else:
                print("\nInvalid option.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            try:
                send_request(sock, 'quit')
            except:
                pass
            break
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            break
    
    try:
        sock.close()
    except Exception as e:
        print(f"Error closing connection: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Application error: {e}")