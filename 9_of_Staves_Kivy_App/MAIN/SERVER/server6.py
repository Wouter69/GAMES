import socket
from _thread import *
import string
from threading import Thread, ThreadError
import threading
from File_S import File_man
from deck import Deck
import time


class server():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #INITS
        self.FM = File_man()
        self.D = Deck()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8085
        self.addr = (self.host, self.port)

        #ADD MAP for CLIENT PROFILES, 

        #CLIENT VARS
        self.group_num = 0
        self.client_list = []
        self.group_list = []
        self.group = []
        
        
        self.CLIENT_LIST = []
       
        
        #ACTIVE PLAYING GROUPS
        self.CLIENT_GROUPS = []
        self.LOGGED_IN = []


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

    def run_to(self, group_obj, obj1, obj2, obj, data):
        ##GET UPDATES
        try:
            # PL_# -> player :: NAME, ICON
            # Conn -> Player :: CONN,
            pl_1 = "OPP_PROFILE@"+str(obj1[0][1])+"@"+str(obj1[0][2])+"@"
            conn1 = obj1[0][0][0]
            pl_2 = "OPP_PROFILE@"+str(obj2[0][1])+"@"+str(obj2[0][2])+"@"
            conn2 = obj2[0][0][0]
            print(f"PL_1:: {pl_1}\nCONN1:: {conn1}\n+++++++++\nPL_2:: {pl_2}\nCONN2:: {conn2}\n")
        except Exception as e:
            print("\n!!!!!!!!!\nINIT_SEND_ERROR::: ", str(e))

        try:
            ##SEND UPDATES TO ALL MEMBERS OF GROUP
            #obj_q = str(obj)
            print(f"\nRUN_TO_DATA: \n   [FROM]: {obj}\n     ::{data}\n################")
            print("\nRUN_TO:: _OBJs \n", ">>::OBJ_1:[0][0][0]:\n", str(pl_1),"", "\n>>::OBJ_2:[0][0][0]:\n", str(pl_2))
        except:
            pass

        try:
            if "QUIT" in data:
                print("OPPONENT_QUIT")
                if str(obj[0]) == str(obj1):
                    print("SENDING...", data)
                    obj2.send(data.encode())
                if str(obj[0]) == str(obj2):
                    print("SENDING...", data)
                    obj1.send(data.encode())
                return
        except Exception as e:
            print("QUIT:ERROR::RUN_TO:: ", str(e))

        try:
            if "END" in data:
                print("\n!![GAME_OVER]!!", str(group_obj))
                print("MSG_TO_SEND_:: >>>>>>", data)
                if str(obj[0]) == str(obj1):
                    print("SENDING...", data)
                    obj2.send(data.encode())
                if str(obj[0]) == str(obj2):
                    print("SENDING...", data)
                    obj1.send(data.encode())
        except Exception as e:
            print("END:ERROR:RUN_TO:: ", str(e))

        try:
            #INIT_ACTIVE_GAME_DATA
            if "MATCH" in data:
                print("###################\n[SENDING]:[MATCH_DATA]\n")
                conn1.send("MATCH1@".encode())
                conn2.send("MATCH2@".encode())
                time.sleep(0.005)
                conn1.send(pl_2.encode())
                conn2.send(pl_1.encode())
                time.sleep(0.005)

                DECK = ["DECK@",]
                self.D.shuffleDeck()
                cards = self.D.Deck_List

                for card in cards:
                    DECK.append("C&"+card+"@")

                for card in DECK:
                    conn1.send(card.encode())
                    conn2.send(card.encode())
                print("DECK_SENT\n**")
                return
        except Exception as e:
            print("MATCH_INIT:ERROR:RUN_TO:: ", str(e))


        try:
            if "MOVE" in data:
                print(f"\nGOT_[FROM]: {obj}\n     ::{data}\n################")

                if str(obj1[0][0][0]) in str(obj):
                    try:
                        print(f"SENDING:{data}..TO:.{str(conn2)}")
                        conn2.send(data.encode())
                    except Exception as e:
                        print("WTF:: ", str(e))
                if str(obj2[0][0][0]) in str(obj):
                    try:
                        print(f"SENDING:{data}..TO:.{str(conn1)}")
                        conn1.send(data.encode())
                    except Exception as e:
                        print("WTF:: ", str(e))
        except Exception as e:
            print("MOVE:EROOR: ", str(e))          



    def read_list(self, obj, data):
        #IF "END" IN DATA :: REMOVE FROM ACTIVE LIST
        #FIND CLIENT IN GROUP >> SEND DATA in RUN_TO
        #[#, [[[conn, addr],active], [data]]]
        print("READ_LIST:\n:CLIENT IS HERE  \n>>", obj[1])
        print("WITH DATA::: ", str(data))

        obj1 = []
        obj2 = []
        group_obj = []

        if obj:
            print("READING CLIENT LIST..")
            try:
                #FIND THE MATCHING ADDR in GROUP NUM_VAL
                for i, group_obj in enumerate(self.CLIENT_GROUPS):
                    print("OBJ_IN_Q:: ::", str(i), str(group_obj))
                    for j, cl in enumerate(group_obj):
                        if len(cl) == 1:
                            print("GROUP>>", cl, "\n", j, "\n")
                        if len(cl) >= 2:
                            obj1 = group_obj[1]#[0][0]
                            obj2 = group_obj[2]#[0][0]
                            print(f"OBJ(S)_IN_Q::\n   {obj1}::\n   {obj2}")
                        if "QUIT" in data or "END" in data:
                            try:
                                self.CLIENT_GROUPS.remove(group_obj)
                                print("GROUP_OBJ REMOVED")
                            except Exception as e:
                                print("GROUP NOT REMOVED::", str(e), str(group_obj))

                try:
                    self.run_to(group_obj, obj1, obj2, obj, data)
                    print("RUNN__TO:: obj[1] ", str(obj))
                except Exception as e:
                    print("RUN_TO_ERROR :: ", str(e))
            except Exception as e:
                print(f'READ_LIST_ERR:: {str(e)}')
                pass

    #CREATE ACTIVE GAME GROUPS
    def parent_list(self, client, data):
        self.E = threading.Event()

        print("DATA:: ")
        fl_data = data.split("@")
        for _ in fl_data:
            print("FL_DATA:: ", str(_))
        name = str(fl_data[1])
        icon = str(fl_data[2])
        p_data = [client, name, icon]


        if len(self.group) <= 1:
            self.group.append(p_data)

        if len(self.group) < 2:
            print('WAITING...FOR OPP')
            self.E.wait()

        #INIT GROUP NUMBER >> APPEND MEMEBERS TO GROUP
        if len(self.group) == 2:
            group_obj = [[self.group_num],]
            #CREAT_GROUP_OBJ
            #print("[CURRENT_GROUP]:: ", self.group_num)
            for cl in self.group:
                mem_obj = [cl, "ACTIVE"]
                group_obj.append(mem_obj)

            print("GROUP_OBJ:MADE:: ")
            for _ in group_obj:
                print("OBJ_ITEM:: ", str(_))

            self.CLIENT_GROUPS.append(group_obj)
            self.group_num +=1
            self.group = []
            self.read_list(client, "MATCH")
            print("MATCH_MADE::PARENT_LIST")

    def check_list(self, client):
        try:
            print("\n\nCHECKING...CLIENT...:\n")
            if len(self.CLIENT_LIST) < 1:
                return False
            for _ in self.CLIENT_LIST:  
                print("$$_ACTIVE_CLIENTS::\n    ls>>", str(_[1]), "\n    cl>>", str(client[1]))      
                if str(client[1]) == str(_[1]):
                    print(f'FOUND {str(_[1])}\n')
                    return True
                else:
                    print("NO_SUCH_CLIENT:: \n", str(_[1]))
                    return False
        except Exception as e:
            print(str(e), "CHECK_LIST")

    def check_player(self, data):
        print("CHECKING_PLAYER", str(data))
        user = data.split("@")
        User = str(user[1]).translate(str.maketrans('','',string.punctuation))
        Date = str(user[2]).translate(str.maketrans('','',string.punctuation))
        Country = str(user[3]).translate(str.maketrans('','',string.punctuation))

        print("USER   ::", User)
        print("DATE   ::", Date)
        print("COUNTRY::", Country)
        
        file_name = "USERS/"+User+Date+".txt"




        if self.FM.check_file(file_name) != True:
            return "NEW"

        if self.FM.check_file(file_name) == True:
            print("WELCOME_BACK")
            return "OLD"

    def create_pl(self, data):
        print("CHECKING_PLAYER", data)
        user = data.split("@")
        User = str(user[1]).translate(str.maketrans('','',string.punctuation))
        Date = str(user[2]).translate(str.maketrans('','',string.punctuation))
        Country = str(user[3]).translate(str.maketrans('','',string.punctuation))

        print("USER   ::", User)
        print("DATE   ::", Date)
        print("COUNTRY::", Country)
        
        file_name = "USERS/"+User+Date+".txt"
        self.FM.write_file(file_name, data, "w")

    def handle_client(self, conn, addr):
        print("conn...", conn)
        client = []
        client = [conn, addr]
        self.E = threading.Event()

        while True:
            try:

                data = conn.recv(1024 * 6).decode()
                print("DATA RECVED:: ", str(data))
                if not data:
                    self.E.wait()

                else:
                    
                    print("msg..", data, " BY ", addr)

                    if "PLAYER" in data or "PROFILE" in data:
                        print("PLAYER_UPDATE::: ", str(data))
                        try:
                            t = self.check_player(data)
                            if "NEW" in t:
                                self.create_pl(data)
                                conn.send("WELCOME_NEW".encode())
                            if "OLD" in t:
                                conn.send("LOGIN".encode())


                        except Exception as e:
                            print("CHECK_PLAYER::ERROR:: ", str(e))

                    if "END" in data or "QUIT" in data:
                        try:
                            self.read_list(client, data)
                        except Exception as e:
                            print("GAME_END_ERROR:: ", str(e))  



                    if "MOVE" in data:
                        print("****\nHAND\n****")
                        try:
                            self.read_list(client, data)
                        except Exception as e:
                            print("HAND_ERROR::", str(e))
                     
                     
                    if "TABLE" in data:
                        print("****\nTABLE\n****")
                        try:
                            #if self.check_list(client) == True:
                            self.read_list(client, data)
                        except Exception as e:
                            print("HAND_ERROR::", str(e))
                     
                     
                                      
                                      
                    if "ELIM" in data:
                        try:
                            self.read_list(client, data)
                        except Exception as e:
                            print("ELIM_ERROR", str(e))

                    if "START" in data:
                        try:
                            #CHECK LIST IF CLIENT EXISTS
                            if len(self.CLIENT_LIST) == 1:
                                print("\n**PLAYER_ONE", str(self.CLIENT_LIST[0]))
                                
                            self.CLIENT_LIST.append(client)

                            grouping = threading.Thread(target=self.parent_list, args=(client, data))
                            grouping.start()


                        except Exception as e:
                            print(f'START_GAME_ERROR:: {str(e)}')
                            pass
                        

            except Exception as e:
                print("[FAILED_TO_RECEIVE]: ", str(e))

    def Main(self):
 
 
        try:
            self.sock.bind(('', self.port))
            print("[BINDING] ")
        except Exception as e:
            print("NOT BINDING: ", str(e))
        
        self.sock.listen(500)
        print("[LISTENING]:")
        
        while True:
            try:
                conn, addr = self.sock.accept()

            except socket.error as e:
                print("[ERROR_CONNECTING_NEW_CLIENT] :", str(e))        
            
            try:
                t1 = threading.Thread(group=None, target=self.handle_client, args=(conn, addr))
                t1.daemon= True
                t1.start()

                
            except ThreadError as e:
                print(f'SERVER::MAIN:: {str(e)}')

if __name__=="__main__":
    s = server()
    s.Main()