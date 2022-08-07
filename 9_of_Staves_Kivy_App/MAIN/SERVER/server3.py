import socket
from _thread import *
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
        
        
        #CLIENT VARS
        self.client_list = []
        self.group_list = []
        self.group = []


        
        #bASE VARS
        self.BUFFER_SIZE = 1024 * 4
        self.SEPARATOR = "@"




    def set_deck(self, user):
        try:
            DECK = self.D.shuffleDeck()
            card, DECK = self.D.get_card(user, DECK)
            print("AFTER:  ",card)
            trues = 0
            for card_set in DECK:
                if trues == 13:
                    print("ALL CARDS USED")
                    return "DONE"
                if card_set[1] == False:
                    print(str(card_set[0]), "IS", str(card_set[1]) )
                else:
                    print(str(card_set[0]), "IS ", str(card_set[1]), ":by:", str(card_set[2]))
                    trues +=1

                return card
        except Exception as e:
            print("SET_DECK:: ", str(e))




#    def get_set(self, conn1, conn2, obj_):
#        card1 =  self.set_deck(str(obj_[1][1]))
#
#        card_1 = "MYCARD@"+str(card1[0]) + "@"
#        conn1.send(card_1.encode())
#        card_1 = "OPPCARD@"+str(card1[0]) + "@"
#        conn2.send(card_1.encode())


    def run_to(self, obj_, j, data):
        ##GET UPDATES

        ##SEND UPDATES TO ALL MEMBERS OF GROUP
        print("OBJ_:RUN_TO \n>>", j[1], "\n>>", str(obj_[0][1]), "\n>>", str(obj_[1][1]))
        print("DATA INPUT: ", data)
        
        conn1 = obj_[0][0]
        conn2 = obj_[1][0]

        #CREATE SEPERATE FUNCTION
        #FOR EACH MOVE TYPE IN [DATA]
        
        #SET PLAYER POSITION FOR TURN_BASE
        if "MATCH" in data:
            
            
            
    #        print("M:: SETS", str(j[1]), str(obj_[1][1]))


            if str(j[1]) == str(obj_[1][1]):
                conn1.send("MATCH@FIRST@".encode())

                card1 =  self.set_deck(str(obj_[1][1]))
                card2 =  self.set_deck(str(obj_[1][1]))
                card3 =  self.set_deck(str(obj_[1][1]))
                card4 =  self.set_deck(str(obj_[1][1]))
                
                
                card_1 = "MYCARD@"+str(card1[0]) + "@"
                conn1.send(card_1.encode())
                card_1 = "OPPCARD@"+str(card1[0]) + "@"
                conn2.send(card_1.encode())


                conn1.send("SEP@".encode())
                conn2.send("SEP@".encode())



                card_2 = "MYCARD@"+str(card2[0]) + "@"
                conn1.send(card_2.encode())
                card_2 = "OPPCARD@"+str(card2[0]) + "@"
                conn2.send(card_2.encode())
#
                card_3 = "MYCARD@"+str(card3[0]) + "@"
                conn1.send(card_3.encode())
                card_3 = "OPPCARD@"+str(card3[0]) + "@"
                conn2.send(card_3.encode())
#
#
                card_4 = "MYCARD@"+str(card4[0]) + "@"
                conn1.send(card_4.encode())
                card_4 = "OPPCARD@"+str(card4[0]) + "@"
                conn2.send(card_4.encode())
#



                conn2.send("MATCH@SECOND@".encode())



                card1 =  self.set_deck(str(obj_[0][1]))
                card2 =  self.set_deck(str(obj_[0][1]))
                card3 =  self.set_deck(str(obj_[0][1]))
                card4 =  self.set_deck(str(obj_[0][1]))
                
                
                card_1 = "MYCARD@"+str(card1[0]) + "@"
                conn2.send(card_1.encode())
                card_1 = "OPPCARD@"+str(card1[0]) + "@"
                conn1.send(card_1.encode())
#
                conn1.send("SEP@".encode())
                conn2.send("SEP@".encode())

                card_2 = "MYCARD@"+str(card2[0]) + "@"
                conn2.send(card_2.encode())
                card_2 = "OPPCARD@"+str(card2[0]) + "@"
                conn1.send(card_2.encode())
#
                card_3 = "MYCARD@"+str(card3[0]) + "@"
                conn2.send(card_3.encode())
                card_3 = "OPPCARD@"+str(card3[0]) + "@"
                conn1.send(card_3.encode())
#

                card_4 = "MYCARD@"+str(card4[0]) + "@"
                conn2.send(card_4.encode())
                card_4 = "OPPCARD@"+str(card4[0]) + "@"
                conn1.send(card_4.encode())




            print("MSG_SENT:: MATCH")

        if "SHIFT" in data:
            print("\n!!!\nSHIFT\n!!!")
            if j == obj_[1]:
                conn1.send(data.encode())
                print("SENT:: ", data, " by ", str(j[1]))
            else:
                conn2.send(data.encode())
                print("SENT:: ", data)


        #CREATE SEPERATE FUNCTION
        if "CARD" in data:# or "START" in data: 

            card1 = self.set_deck(str(j[1]))
            if "DONE" not in card1:
                #card2 = self.set_deck()
                if j == obj_[0]:
                    ret1 = str("MY_CARD")+"@"+str(card1[0])
                    ret2 = str("OPP_CARD")+"@"+str(card1[0])
                if j == obj_[1]:
                    ret2 = str("MY_CARD")+"@"+str(card1[0])
                    ret1 = str("OPP_CARD")+"@"+str(card1[0])

                print("SENDING:to_conn1:: ", ret1)
                print("SENDING:to_conn2:: ", ret2)

                conn1.send(ret1.encode())
                conn2.send(ret2.encode())
            
            
            
            #CREATE SEPERATE FUNCTION
            if "DONE" in data:
                print("DECK DEPLETED")
                conn1.send("DONE".encode())
                conn2.send("DONE".encode())

                return "DONE"



    def read_list(self, obj, data):
        self.RL = threading.Event()
        #print("OBJ IN QUESTION:: ", obj)
        obj_q = []
        if obj:
            print("READING CLIENT LIST..")

            try:
                #print("READING....")
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
            print('WAITING...')
            conn = client[0]
            conn.send("LOBBY".encode())
            print("MSG_SENT:: LOBBY")
            

            self.E.wait()

        elif len(self.group) == 2:
            self.group = []
            self.read_list(client, "MATCH")
            





    def check_list(self, client):
        for _ in self.client_list:
            if client == _:
                print(f'FOUND {str(_[1])}')
                return True
            else:
                print("FUCK_UP")




    def handle_client(self, conn, addr):
        print("conn...")
        client = []
        client = [conn, addr]
        self.E = threading.Event()

        while True:
            try:

                data = conn.recv(1024 * 3).decode()
                if not data:
                    self.E.wait()

                else:
                    print("msg..")
                    if "START" in data or "CARD" in data or "SHIFT" in data:
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

                print("NEW_THREAD: ", addr)
                
            except ThreadError as e:
                print(f'SERVER::MAIN:: {str(e)}')
                
                
                
if __name__=="__main__":
    s = server()
    s.Main()