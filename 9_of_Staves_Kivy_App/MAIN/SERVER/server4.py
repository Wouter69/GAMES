import socket
from _thread import *
import string
from threading import Thread, ThreadError
import threading
#from file_handle_S import File_man
from deck import Deck



class server():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #INITS
        self.D = Deck()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8085
        self.addr = (self.host, self.port)


        #ADD MAP for CLIENT PROFILES, 

        #CLIENT VARS
        self.client_list = []
        self.group_list = []
        self.group = []
        
        
        group = 0
        conn = ""
        addr = ""
        active = ""
        client = [conn, addr, active]
        cmd = ""
        card = ""
        wid = ""
        action = [cmd, card, wid]

        
        self.CLIENTS = dict([
            (group, [client, action]),
            ])




        #bASE VARS
        self.BUFFER_SIZE = 1024 * 6





    def filter_change(self, data, change):
        if "HAND" in change:
            filt = data.split("@")
            print("\nFILTER\n::->>", change)
            new_data = ""
            for _ in filt:
                val = _.translate(str.maketrans('','',string.punctuation))
                print("VAL::",val)
                new_data += str(val)+"&"
            return(new_data)
        
        if "TABLE" in change:
            print("TABLE:: ", data)
            return("NONE")
        
        if "ELEM" in change:
            return("NONE")





    def run_to(self, obj_, j, data):
        ##GET UPDATES

        ##SEND UPDATES TO ALL MEMBERS OF GROUP
        print("OBJ_:RUN_TO \n>>", j[1], "\n>>", str(obj_[0][1]), "\n>>", str(obj_[1][1]))
        print("DATA INPUT: ", data)
        
        conn1 = obj_[0][0]
        conn2 = obj_[1][0]

        #SET PLAYER POSITION FOR TURN_BASE
        # #ToDo
        if "MATCH" in data:
            DECK = ["DECK",]
            #self.D.shuffleDeck()
            cards = self.D.Deck_List
            for card in cards:
                DECK.append(card)
            print("\n\nDECK::", DECK, "\n\ncars_LEN::",  len(cards))
            if str(j[1]) == str(obj_[1][1]):
                conn1.send("MATCH@".encode())
                conn2.send("MATCH@".encode())
                
                for _ in DECK:
                    #print("ITEMS",_)
                    card = str(_)+"@"
                    conn1.send(card.encode())
                    conn2.send(card.encode())
                print("\nDECK_SENT::\n")

            print("MSG_SENT:: MATCH")
            conn1.send("SET".encode())
            conn2.send("SET".encode())                

            return


        if "HAND" in data:
    

            print("\n!!!\nCARD_SELECTED\n!!!\n::",data)
            #ALTER DATA-->> INFORM CLIENT OF CHANGES
            #FILTER DATA -> self.filter(data, change) change:"TO_HAND"

            sending = self.filter_change(data, "TO_HAND")
            print(sending)
            if j == obj_[1]:
                conn1.send(sending.encode())
                print("SENT:: ", sending, " by ", str(j[1]))
            else:
                conn2.send(sending.encode())
                print("SENT:: ", sending)





            
            
            #CREATE SEPERATE FUNCTION
            if "DONE" in data:
                print("DECK DEPLETED")
                conn1.send("DONE".encode())
                conn2.send("DONE".encode())
                return "DONE"



    def read_list(self, obj, data):
        self.RL = threading.Event()
        obj_q = []
        if obj:
            print("READING CLIENT LIST..")
            try:
                for i in self.group_list:
                    obj_q = i
                    print("READING_GROUP: ")
                    for j in i:
                        print("CONNECTION: ", j[1])
                        if obj == j:
                            obj_j = j
                            print("FOUND OBJ_Q")
                            self.run_to(obj_q, obj_j, data)
            except Exception as e:
                print(f'READ_LIST_ERR:: {str(e)}')
                pass



    def parent_list(self, client):
        self.E = threading.Event()

        num = len(self.client_list)
        if num % 2:
            self.group_list.append(self.group)


        if len(self.client_list) >= 1:
            self.group.append(client)
            
            print(f'[CURRENT_GROUP]::')
            for _ in self.group:
                print(f'>> {str(_[1])}')


        if len(self.group) < 2:
            print('WAITING...FOR OPP')
            

            self.E.wait()

        elif len(self.group) == 2:
            self.group = []
            self.read_list(client, "MATCH")

            





    def check_list(self, client):
        for _ in self.client_list:
            if client == _:
                #print(f'FOUND {str(_[1])}')
                return True
            else:
                print("FUCK_UP", str(_[1]))




    def handle_client(self, conn, addr):
        print("conn...", addr)
        client = []
        client = [conn, addr]
        self.E = threading.Event()

        while True:
            try:

                data = conn.recv(1024 * 6).decode()
                if not data:
                    self.E.wait()

                else:
                    print("msg..", data, " BY ", addr)
                    if "START" in data or "ELEM" in data or "HAND" in data:
                        try:
                            print("___TESTING_IMPLEMENTATION___")
                            #CHECK LIST IF CLIENT EXISTS
                            if len(self.client_list) < 1:
                                print("STARTING")
                                

                            if self.check_list(client) == True:
                                self.read_list(client, data)
                                

                            else:
                                self.client_list.append(client)
                                grouping = threading.Thread(target=self.parent_list, args=(client,))
                                grouping.daemon = True
                                grouping.start()


                        except Exception as e:
                            print(f'BIG_KARADEO:: {str(e)}')
                            pass
                        

            except Exception as e:
                print("[FAILED_TO_RECEIVE]: ", str(e))





    def Main(self):
 
 
        try:
            self.sock.bind(('', self.port))
            print("[BINDING] ")
        except Exception as e:
            print("NOT BINDING: ", str(e))
        
        self.sock.listen(40)
        print("[SERVER LISTENING]:")
        
        while True:
            try:
                conn, addr = self.sock.accept()

            except socket.error as e:
                print("[ERROR_CONNECTING_NEW_CLIENT] :", str(e))        
            
            try:
                t1 = threading.Thread(group=None, target=self.handle_client, args=(conn, addr))
                t1.daemon= True
                t1.start()

                #print("NEW_THREAD: ", addr)
                
            except ThreadError as e:
                print(f'SERVER::MAIN:: {str(e)}')
                
                
                
if __name__=="__main__":
    s = server()
    s.Main()