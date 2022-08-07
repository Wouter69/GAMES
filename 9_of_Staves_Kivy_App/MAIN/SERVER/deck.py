import random


class Deck():
    def __init__(self, *args):
        super(Deck, self).__init__(*args)
        #31 crads total
        #12 t_M_B
        #3 jokers
        #3 x 6 runes cards

        #LIST OF CARDS
        self.rune11 = "R_R_G1"
        self.rune12 = "R_R_G2"
        self.rune13 = "R_R_G3"

        self.rune21 = "R_A_G1"
        self.rune22 = "R_A_G2"
        self.rune23 = "R_A_G3"


        self.rune31 = "R_Y_R1"
        self.rune32 = "R_Y_R2"
        self.rune33 = "R_Y_R3"

        self.joker1 = "J1"
        self.joker2 = "J2"
        self.joker3 = "J3"

        self.top1 = "T1"
        self.top2 = "T2"
        self.top3 = "T3"
        self.top4 = "T4"
        self.top5 = "T5"
        self.top6 = "T6"
        self.top7 = "T7"
        self.top8 = "T8"
        self.top9 = "T9"
        self.top10 = "T10"
        self.top11 = "T11"
        self.top12 = "T12"

        self.mid1 = "M1"
        self.mid2 = "M2"
        self.mid3 = "M3"
        self.mid4 = "M4"
        self.mid5 = "M5"
        self.mid6 = "M6"
        self.mid7 = "M7"
        self.mid8 = "M8"
        self.mid9 = "M9"
        self.mid10 = "M10"
        self.mid11 = "M11"
        self.mid12 = "M12"

        self.bot1 = "B1"
        self.bot2 = "B2"
        self.bot3 = "B3"
        self.bot4 = "B4"
        self.bot5 = "B5"
        self.bot6 = "B6"
        self.bot7 = "B7"
        self.bot8 = "B8"
        self.bot9 = "B9"
        self.bot10 = "B10"
        self.bot11 = "B11"
        self.bot12 = "B12"


        self.Deck_List = [ self.rune11,
                          self.rune12,
                          self.rune13,
                          self.rune21,
                          self.rune22,
                          self.rune23,
                          self.rune31,
                          self.rune32,
                          self.rune33,
                          self.joker1,
                          self.joker2,
                          self.joker3,
                          self.top1,
                          self.top2,
                          self.top3,
                          self.top4,
                          self.top5,
                          self.top6,
                          self.top7,
                          self.top8,
                          self.top9,
                          self.top10,
                          self.top11,
                          self.top12,
                          self.mid1,
                          self.mid2,
                          self.mid3,
                          self.mid4,
                          self.mid5,
                          self.mid6,
                          self.mid7,
                          self.mid8,
                          self.mid9,
                          self.mid10,
                          self.mid11,
                          self.mid12,
                          self.bot1,
                          self.bot2,
                          self.bot3,
                          self.bot4,
                          self.bot5,
                          self.bot6,
                          self.bot7,
                          self.bot8,
                          self.bot9,
                          self.bot10,
                          self.bot11,
                          self.bot12]

        
        
        
        
        
    def shuffleDeck(self):
        random.shuffle(self.Deck_List)
        

#        try:
#            for cardpos in range(len(self.Deck_List)):
#                randPos = random.randint(0, (len(self.Deck_List)-1))
#                self.Deck_List[cardpos], self.Deck_List[randPos] = self.Deck_List[randPos], self.Deck_List[cardpos]
#                DECK = self.Deck_List
#                return DECK
#        except Exception as e:
#            print(str(e), "DECK_RAND FAILED")