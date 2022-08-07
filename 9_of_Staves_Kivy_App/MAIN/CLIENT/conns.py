#CONNECTION__
import socket
from file_handle_C import File_man

#CONNECTION CLASSES
class connections():
    def __init__(self, **kwargs):
        self.val = ""
        self.FM = File_man()
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(e)
        self.host = '127.0.0.1'
        self.port = 8085
        self.encap = "@"

        
        
        try:
            self.sock.connect((self.host, self.port))
            print("\n[CONNECTED]\n")
        except Exception as e:
            print(e)
       
        

            
    def get_msg(self):
        print("[GET_MSG]:[RUNNING]")
        #WRITE ALL DATA TO FILE
        while True:
            received = ""
            try:
                received = self.sock.recv(1024).decode()
                print("[RECV]: ", received, "\n")

                if "OOP_PROFILE" in received:
                    self.FM.write_file("OppData.txt", received, "w")
                if "LOGIN" in received:
                    print("WRITING...")
                    self.FM.write_file("Player.txt", received, "w")
                else:
                    self.FM.write_file("SERVER.txt", received, "w")

            except Exception as e:
                print("[SOCKET CLOSED]")
                print(str(e)) 
                self.sock.close()   
    
    
    def send_msg(self):
        print("[SEND_MSG]:[RUNNING]")
        #READ ALL DATA FROM FILES>>

        path = "GAME.txt"
        path2 = "Player.txt"
        try:
            self.init_data = str(self.FM.read_file(path))
            self.init_pl = str(self.FM.read_file(path2))

            print("INIT_DATA:: ", self.init_data)
        except:
            pass
        try:
            while True:
 #               time.sleep(1)
                data = str(self.FM.read_file(path))
                data2 = str(self.FM.read_file(path2))
                if self.init_data != data:
                    print(f'[SENDING]:: {data}')
                    self.init_data = data
                    msg = data

                    try:
                        self.sock.send(msg.encode())

                    except Exception as e:
                        print("FUCKUP::SEND_MSG::", str(e))

                if self.init_pl != data2:
                    print(f'[SENDING]:: {data}')
                    self.init_pl = data2
                    msg = data2

                    try:
                        self.sock.send(msg.encode())

                    except Exception as e:
                        print("FUCKUP::SEND_MSG::", str(e))

        except Exception as e:
            print("SENDING_ERROR::", str(e))






