# TO DO

# 2 player preflop bot play..., rare raise amount is too much, fold to min_raises often, check-raises, reraises

# make 'show hands' function in gui start_game_bar

'''
tbs should be list of lists, when elems are exhausted, first elem should be empty list, something destructed somewhere
    if tbs[0] == []: # no more elements to tiebreak
IndexError: list index out of range
'''
'''
rand call act true_cost 40
apply bot action player2 raise 153
Raise gui error prob from bot which doesnt use wagerEntry
options in populate call_options
rand check act table.min_bet 20
Exception in Tkinter callback
Traceback (most recent call last):
  File "/Users/crazyfox/anaconda3/lib/python3.7/tkinter/__init__.py", line 1702, in __call__
    return self.func(*args)
  File "gui.py", line 262, in <lambda>
    self.b1 = tk.Button(self,text='Call '+str(min(room.table.plyr_dict[plyr].stack,room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round)),highlightbackground='black',font=('Helvetica',16),command=lambda:self.call(plyr))
  File "gui.py", line 349, in call
    room.player_window.get_actions()
  File "gui.py", line 223, in get_actions
    room.player_window.populate(plyr, options)
  File "gui.py", line 298, in populate
    bot_action, maybe_amount = room.table.plyr_dict[plyr].get_random_bot_action(plyr, room.table)
  File "/Users/crazyfox/Desktop/organized/githubProjects/rewrite_pokerthief/bot_profiles.py", line 40, in get_random_bot_action
    return self.get_random_check_action(p, table)
  File "/Users/crazyfox/Desktop/organized/githubProjects/rewrite_pokerthief/bot_profiles.py", line 49, in get_random_check_action
    amount = randrange(max(table.pot//3,table.min_bet), min((2*table.pot),table.plyr_dict[p].stack)+1)
  File "/Users/crazyfox/anaconda3/lib/python3.7/random.py", line 200, in randrange
    raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))
ValueError: empty range for randrange() (145,128, -17)
'''

'''
more than enough to call but not enough for legal raise, in get_random_call_action-->raise
 File "gui.py", line 131, in populate
    bot_action, maybe_amount = room.table.plyr_dict[plyr].get_random_bot_action(plyr, room.table)
  File "/Users/crazyfox/Desktop/organized/githubProjects/rewrite_pokerthief/player.py", line 68, in get_random_bot_action
    if table.cost_to_play == table.plyr_dict[p].chips_this_round:
  File "/Users/crazyfox/Desktop/organized/githubProjects/rewrite_pokerthief/player.py", line 90, in get_random_call_action
    if table.plyr_dict[p].stack <= (2 * true_cost):
  File "/Users/crazyfox/anaconda3/lib/python3.7/random.py", line 200, in randrange
    raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))
ValueError: empty range for randrange() (1089,444, -645)

'''
'''
still some errors in create_pots() tests, possibly just created by illegal player/pot configurations in tests

begin hand chips 928
chips in pot 472
stack 456
player5
begin hand chips 535
chips in pot 535
stack 0
player8
begin hand chips 934
chips in pot 934
stack 0
player6
begin hand chips 243
chips in pot 243
stack 0
player1
begin hand chips 595
chips in pot 79
stack 516
player3
begin hand chips 523
chips in pot 455
stack 68
player4
begin hand chips 727
chips in pot 561
stack 166
player2
begin hand chips 352
chips in pot 352
stack 0
player7
begin hand chips 718
chips in pot 649
stack 69
['player8']
returned this many chips 399
pre-subtract small stacks [243, 352, 535]
post-subtract small stacks [243, 352, 535]
pots [2023, 2786, 3741]
return pots_plyrs  [(2023, ['player5', 'player8', 'player6', 'player2']), (763, ['player5', 'player8', 'player2']), (955, ['player5', 'player8'])]
sum_pots 3741 created_chips_total 3881
Traceback (most recent call last):
  File "table.py", line 508, in <module>
    assert(created_chips_total == sum_pots)
AssertionError
####################################
player9
begin hand chips 767
chips in pot 238
stack 529
player4
begin hand chips 560
chips in pot 328
stack 232
player2
begin hand chips 925
chips in pot 849
stack 76
player5
begin hand chips 117
chips in pot 83
stack 34
player1
begin hand chips 110
chips in pot 8
stack 102
player3
begin hand chips 544
chips in pot 544
stack 0
player6
begin hand chips 88
chips in pot 88
stack 0
player7
begin hand chips 671
chips in pot 671
stack 0
player8
begin hand chips 150
chips in pot 150
stack 0
['player7']
returned this many chips 127
pre-subtract small stacks [88, 150, 544]
post-subtract small stacks [88, 150, 544]
pots [707, 1079, 2527]
return pots_plyrs  [(707, ['player3', 'player6', 'player7', 'player8']), (372, ['player3', 'player7', 'player8']), (1448, ['player3', 'player7'])]
sum_pots 2527 created_chips_total 2832
Traceback (most recent call last):
  File "table.py", line 508, in <module>
    assert(created_chips_total == sum_pots)
AssertionError
#####################################
player5
begin hand chips 482
chips in pot 482
stack 0
player4
begin hand chips 522
chips in pot 522
stack 0
player1
begin hand chips 149
chips in pot 149
stack 0
player6
begin hand chips 31
chips in pot 8
stack 23
player9
begin hand chips 522
chips in pot 16
stack 506
player2
begin hand chips 799
chips in pot 628
stack 171
player3
begin hand chips 619
chips in pot 619
stack 0
player7
begin hand chips 433
chips in pot 433
stack 0
player8
begin hand chips 107
chips in pot 51
stack 56
['player3']
returned this many chips 97
pre-subtract small stacks [149, 433, 482, 522]
post-subtract small stacks [149, 433, 482, 522]
pots [969, 2389, 2585, 2705]
return pots_plyrs  [(969, ['player5', 'player4', 'player1', 'player3', 'player7']), (1420, ['player5', 'player4', 'player3', 'player7']), (196, ['player5', 'player4', 'player3']), (120, ['player4', 'player3'])]
sum_pots 2705 created_chips_total 2811
Traceback (most recent call last):
  File "table.py", line 508, in <module>
    assert(created_chips_total == sum_pots)
AssertionError
####################################
'''


# prob with less than legal all-in/raise/call and blinds folding
# error 3 player, dealer has less than legal call (less than sb/bb), goes all-in stack say 4 with bb 20, next bot FOLDS
# is fold expected? what to do about less than legal all-in/call/raise? if bb can fold but ss cannot win even the entire
# bb, chips should be in main_pot for sb player non-ss non-bb, should be returned to remaining player in hand with ss


# gui wagerEntry slider rounds up or down to nearest ten, resulting in input of illegal amounts

# gui show call / all-in amounts

# unique player image faces

# One player remains, end screen/new table

# fix gui grid layout? should use place for exact x,y coords of N plyrs equidistant from each other around an oval 

# post_blinds() using floor division without accounting for remainder with odd stacks (happens after chip split)

# Tell hand type, highlight community cards used in hand

import pdb
import table
import tkinter as tk
from PIL import Image, ImageTk
import sys

class Player_window(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
        tmpImage = Image.open('res/placeholder.gif').resize((130,130))
        self.playerImage = ImageTk.PhotoImage(tmpImage)
        self.playerImg = tk.Label(self, image=self.playerImage, bg='black')
        self.playerImg.pack(side='left')
        self.plyrMsg = tk.Label(self,text='Welcome to Poker',bg='black',fg='maroon')
        self.plyrMsg.pack()
        self.card1 = tk.Label(self,image=None,bg='black')
        self.card1.pack(side='left')
        self.card2 = tk.Label(self,image=None,bg='black')
        self.card2.pack(side='left')
        
    # calls populate(), gets legal actions from underlying table object
    def get_actions(self):
        options = room.table.get_actions()
        plyr = room.table.left_to_act[0]
        room.player_window.populate(plyr, options)
        
    def create_all_in_buttons(self, plyr):
        self.b1 = tk.Button(self,text='Check',highlightbackground='black',font=('Helvetica',16),command=lambda:self.check(plyr))
        self.b1.pack(side='left')
        
    def create_bb_option_buttons(self, plyr):
        self.b1 =  tk.Button(self,text='Check',highlightbackground='black',font=('Helvetica',16),command=lambda:self.check(plyr))
        self.b1.pack(side='left')
        self.b2 = tk.Button(self,text='Raise',highlightbackground='black',font=('Helvetica',16),command=lambda:self.Raise(plyr))
        self.b2.pack(side='left')
        self.wagerEntry = tk.Scale(self,from_=min(room.table.plyr_dict[plyr].stack,room.table.min_bet),to=room.table.plyr_dict[plyr].stack,orient='horizontal',resolution=10,bg='black',fg='wheat3')
        self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    def create_call_all_in_buttons(self, plyr):
        self.b1 = tk.Button(self,text='Call '+str(min(room.table.plyr_dict[plyr].stack,room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round)),highlightbackground='black',font=('Helvetica',16),command=lambda:self.call(plyr))
        self.b1.pack(side='left')
        # player cannot raise if only enough to call, do not create the button
        if room.table.plyr_dict[plyr].stack > room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round:
            self.b2 = tk.Button(self,text='All-In',highlightbackground='black',font=('Helvetica',16),command=lambda:self.all_in(plyr))
            self.b2.pack(side='left')
            self.wagerEntry = tk.Scale(self,from_=room.table.plyr_dict[plyr].stack,to=room.table.plyr_dict[plyr].stack,orient='horizontal',resolution=10,bg='black',fg='wheat3')
            self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    def create_check_buttons(self,plyr):
        self.b1 =  tk.Button(self,text='Check',highlightbackground='black',font=('Helvetica',16),command=lambda:self.check(plyr))
        self.b1.pack(side='left')
        self.b2 = tk.Button(self,text='Bet',highlightbackground='black',font=('Helvetica',16),command=lambda:self.bet(plyr))
        self.b2.pack(side='left')
        self.wagerEntry = tk.Scale(self,from_=min(room.table.plyr_dict[plyr].stack,room.table.min_bet),to=room.table.plyr_dict[plyr].stack,orient='horizontal',resolution=10,bg='black',fg='wheat3')
        self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    def create_call_buttons(self,plyr):
        self.b1 = tk.Button(self,text='Call '+str(min(room.table.plyr_dict[plyr].stack,room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round)),highlightbackground='black',font=('Helvetica',16),command=lambda:self.call(plyr))
        self.b1.pack(side='left')
        # player cannot raise if only enough to call, do not create the button
        if room.table.plyr_dict[plyr].stack > room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round:
            self.b2 = tk.Button(self,text='Raise',highlightbackground='black',font=('Helvetica',16),command=lambda:self.Raise(plyr))
            self.b2.pack(side='left')
            self.wagerEntry = tk.Scale(self,from_=min(room.table.plyr_dict[plyr].stack-room.table.cost_to_play+room.table.plyr_dict[plyr].chips_this_round,room.table.min_bet),to=min(room.table.plyr_dict[plyr].stack,room.table.plyr_dict[plyr].stack-room.table.cost_to_play+room.table.plyr_dict[plyr].chips_this_round),orient='horizontal',resolution=10,bg='black',fg='wheat3')
            self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    def create_current_plyr_image(self,plyr):
        self.plyrMsg.configure(text='What will '+plyr+' do?')
        self.cardimg1 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[plyr].str_hand()[0]+'.gif'))
        self.card1.configure(image=self.cardimg1)
        self.cardimg2 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[plyr].str_hand()[1]+'.gif'))
        self.card2.configure(image=self.cardimg2)
        
    # working here, bots after refactor
    def create_bot_plyr_img(self,plyr):
        self.plyrMsg.configure(text='Robot '+plyr+' is thinking...')
        # WORKING HERE
        self.card1.configure(image=room.card_back)
        self.card2.configure(image=room.card_back)
    
    def show_bot_action(self, p, act, amt=0):
        room.table_window.update_table_window_cards_and_chips()
        self.plyrMsg.configure(text='Robot ' + p + act + ' ' + str(amt))

    # Called by get_actions(), figures out what buttons/images in player_window
    def populate(self, plyr, options):
        # FOR BOTS FROM THE FUTURE
        if room.table.plyr_dict[plyr].human == 0:
            room.player_window.destroy_buttons()
            self.create_bot_plyr_img(plyr)
            # working here bug BUG not really bug add bot action print and delay
            bot_action, maybe_amount = room.table.plyr_dict[plyr].get_random_bot_action(plyr, room.table)
            room.after(1000, self.show_bot_action, plyr, bot_action, maybe_amount)
            room.after(3000, self.apply_bot_action, plyr, bot_action, maybe_amount)
        else:# PUNY HUMANS
            self.create_current_plyr_image(plyr)
            print('options in populate ' + options[0])
            if options[0] == 'all-in':
                self.create_all_in_buttons(plyr)
            elif options[0] == 'bb_options':
                self.create_bb_option_buttons(plyr)
            elif options[0] == 'check_options':
                self.create_check_buttons(plyr)
            elif options[0] == 'call_options':
                self.create_call_buttons(plyr)
            elif options[0] == 'call_all_in_options':
                self.create_call_all_in_buttons(plyr)
            room.table_window.update_table_window_cards_and_chips()
        
    def apply_bot_action(self, p, act, amt=0):
        print('apply bot action ' + p + ' ' + act + ' ' + str(amt))
        if act == 'fold':
            self.fold(p)
        elif act == 'check':
            self.check(p)
        elif act == 'raise':
            self.Raise(p, amt)
        elif act == 'all_in':
            self.all_in(p)
        elif act == 'bet':
            self.bet(p, amt)
        elif act == 'call':
            self.call(p)
        
    def all_in(self, plyr):
        amount = room.table.plyr_dict[plyr].stack
        room.table_window.update_table_window_cards_and_chips()
        maybe_winner = room.table.apply_action(plyr, 'all_in', amount)
        self.destroy_buttons()
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
        
    def call(self, plyr):
        amount = min(room.table.plyr_dict[plyr].stack,room.table.cost_to_play-room.table.plyr_dict[plyr].chips_this_round)
        room.table_window.update_table_window_cards_and_chips()
        self.destroy_buttons()
        maybe_winner = room.table.apply_action(plyr, 'call', amount)
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
        
    # note Raise instead of raise
    def Raise(self,plyr,amount=0):
        try:
            amount = self.wagerEntry.get()
        except:
            print('Raise gui error prob from bot which doesnt use wagerEntry')
        room.table_window.update_table_window_cards_and_chips()
        maybe_winner = room.table.apply_action(plyr, 'raise', amount)
        self.destroy_buttons()
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
        
    def fold(self,plyr):
#        pdb.set_trace()
        maybe_winner = room.table.apply_action(plyr, 'fold')
        room.table_window.update_table_window_cards_and_chips()
        room.imageList[plyr].c1.configure(image=room.no_card)
        room.imageList[plyr].c2.configure(image=room.no_card)
        self.destroy_buttons()
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
        
    def bet(self,plyr,amount=0):
        try:
            amount = self.wagerEntry.get()
        except:
            pass
        maybe_winner = room.table.apply_action(plyr, 'bet', amount)
        room.table_window.update_table_window_cards_and_chips()
        self.destroy_buttons()
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
    
    def check(self,plyr):
        maybe_winner = room.table.apply_action(plyr, 'check')
        room.table_window.update_table_window_cards_and_chips()
        self.destroy_buttons()
        if maybe_winner:
            self.display_winners(maybe_winner[1])
        else:
            room.player_window.get_actions()
            
    def next_hand(self):
        for plyr in room.table.seat_order:
            if room.table.plyr_dict[plyr].stack == 0:
                room.imageList[plyr].destroy()
        room.table.next_hand()
        room.table_window.rotate_dealer_button()
        room.table_window.create_chip_and_card_images()
        for plyr in room.table.seat_order:
            room.imageList[plyr].c1.configure(image=room.card_back)
            room.imageList[plyr].c2.configure(image=room.card_back)
        self.get_actions()
        
    
    def destroy_buttons(self):
        try:
            self.b1.destroy()
        except:
            pass
        try:
            self.b2.destroy()
        except:
            pass
        try:
            self.b3.destroy()
        except:
            pass
        try:
            self.wagerEntry.destroy()
        except:
            pass
        try:
            self.card1.configure(image=None)
            self.card2.configure(image=None)
        except:
            pass
            
            
    def display_winners(self, winner_dict):
        wnr, amt = winner_dict.popitem()
        print('DEBUG ' + wnr + ' wins ' + str(amt))
        self.plyrMsg.configure(text= wnr + ' wins ' + str(amt))
        self.cardimg1 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[wnr].str_hand()[0]+'.gif'))
        self.card1.configure(image=self.cardimg1)
        self.cardimg2 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[wnr].str_hand()[1]+'.gif'))
        self.card2.configure(image=self.cardimg2)
        room.imageList[wnr].c1.configure(image=self.cardimg1)
        room.imageList[wnr].c2.configure(image=self.cardimg2)
        if winner_dict != {}:
            self.after(3000, self.display_winners, winner_dict)
        else:
            self.after(3000, self.next_hand)

    
class Start_game_bar(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
        self.b = tk.Button(self,takefocus=1,text="Start Game!",highlightbackground='black',command=self.startGameEntries)
        self.b.pack(side='left')
        self.quitButton = tk.Button(self,takefocus=1,text='Quit',highlightbackground='black',command=self.areYouSureQuit)
        self.quitButton.pack(side='left')
        self.b2 = tk.Button(self, takefocus=1, text= 'Show All Hands', highlightbackground='black', command=self.show_hands)
        self.b2.pack(side='left')
        
    def show_hands(self):
        for p in room.table.seat_order:
            room.imageList[p].img1 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[p].str_hand()[0]+'.gif'))
            room.imageList[p].img2 = ImageTk.PhotoImage(Image.open('res/'+room.table.plyr_dict[p].str_hand()[1]+'.gif'))
            room.imageList[p].c1.configure(image=room.imageList[p].img1)
            room.imageList[p].c2.configure(image=room.imageList[p].img2)
    
    def areYouSureQuit(self):
        self.quitGamePopup = QuitGamePopup(self)
        
    def startGameEntries(self):
        self.startGamePopup = StartGamePopup(self)
        self.wait_window(self.startGamePopup.top)
    
    
# holds all gui elements in middle window ("table" area), images for each player, community cards, chips
class Table_window(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,relief='ridge',bd=4)
        self.image = Image.open("res/background.gif") # open image as instance of self
        self.img_copy= self.image.copy() # copy made for later resizing
        self.background_image = ImageTk.PhotoImage(self.image) # changed to ImageTk
        self.background = tk.Label(self, image=self.background_image) # label as background
        self.background.bind('<Configure>', self._resize_image) # bind to resize window
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        
    # Initialize pot and community cards gui area
    def create_chip_and_card_images(self):
        self.chip_frame = tk.Frame(self.background,bg='black',relief='groove',bd=4)
        self.num_frame = tk.Frame(self.chip_frame,bg='black',relief='raised',bd=3)
        self.chips = tk.Label(self.num_frame,text=0,font=('Helvetica',22),bg='black',fg='wheat3')
        self.chips.pack(side='top')
        self.chip_img = tk.Label(self.num_frame,image=room.chips,bg='black')
        self.chip_img.pack(side='top')
        self.num_frame.pack(side='left')
        self.chip_frame.grid(row=2,column=1,columnspan=2)
        self.card1 = tk.Label(self.chip_frame,image=room.no_card,bg='black')
        self.card1.pack(side='left')
        self.card2 = tk.Label(self.chip_frame,image=room.no_card,bg='black')
        self.card2.pack(side='left')
        self.card3 = tk.Label(self.chip_frame,image=room.no_card,bg='black')
        self.card3.pack(side='left')
        self.card4 = tk.Label(self.chip_frame,image=room.no_card,bg='black')
        self.card4.pack(side='left')
        self.card5 = tk.Label(self.chip_frame,image=room.no_card,bg='black')
        self.card5.pack(side='left')
        
    # Called after player decisions, update all player chips and pot chip amount
    def update_table_window_cards_and_chips(self):
        self.chips.configure(text=room.table.pot)
        for plyr in room.table.seat_order:
            room.imageList[plyr].stack.configure(text=room.table.plyr_dict[plyr].stack)
        # for card in table.com_cards: update table_window card image
        if room.table.round == 2:
            self.deal_flop()
        elif room.table.round == 3:
            self.deal_turn()
        elif room.table.round == 4:
            self.deal_river()
        
    def rotate_dealer_button(self):
        for i,p in enumerate(room.table.seat_order):
            if i == 0:
                room.imageList[p].dealerButton.configure(text = 'dealer')
            else:
                room.imageList[p].dealerButton.configure(text = '')
        
    # Get and reveal gui images of dealt cards
    def deal_flop(self):
        self.card1img = ImageTk.PhotoImage(Image.open('res/'+str(room.table.com_cards[0][0])+str(room.table.com_cards[0][1])+'.gif'))
        self.card1.configure(image=self.card1img)
        self.card2img = ImageTk.PhotoImage(Image.open('res/'+str(room.table.com_cards[1][0])+str(room.table.com_cards[1][1])+'.gif'))
        self.card2.configure(image=self.card2img)
        self.card3img = ImageTk.PhotoImage(Image.open('res/'+str(room.table.com_cards[2][0])+str(room.table.com_cards[2][1])+'.gif'))
        self.card3.configure(image=self.card3img)
        
    def deal_turn(self):
        self.card4img = ImageTk.PhotoImage(Image.open('res/'+str(room.table.com_cards[3][0])+str(room.table.com_cards[3][1])+'.gif'))
        self.card4.configure(image=self.card4img)
        
    def deal_river(self):
        self.card5img = ImageTk.PhotoImage(Image.open('res/'+str(room.table.com_cards[4][0])+str(room.table.com_cards[4][1])+'.gif'))
        self.card5.configure(image=self.card5img)
        
    # create room.imagelist dictionary, places images in seating order
    # reference the IMAGES on each players window like so:
    # room.imageList['player1'].stack, .c1 (card1), .c2 (card2)
    # create grid layout depending on number of players
    # maybe fix crappy grid layout
    def create_player_images(self,plyrOrder):
        room.imageList = {}
        row = 1
        column = 1
        counter = 1
        for plyr in plyrOrder:
            self.w = tk.Frame(self.background,relief='ridge',bd=4,background='black')
            self.w.info = tk.Frame(self.w,relief='ridge',bd=3,background='black')
            if room.table.plyr_dict[plyr].bot_profile == 'stop_n_go':
                self.w.plyrImg = ImageTk.PhotoImage(Image.open('res/stop_n_go.gif').resize((60,50)))  
            else:
                self.w.plyrImg = ImageTk.PhotoImage(Image.open('res/playerImage.gif').resize((60,50)))
            self.w.pic = tk.Label(self.w.info,image=self.w.plyrImg,bg='black')
            self.w.pic.pack(side='left')
            self.w.player = tk.Label(self.w.info,text=plyr,fg='wheat3',bg='black')
            self.w.player.pack(side='top')
            self.w.stack = tk.Label(self.w.info,text=room.table.plyr_dict[plyr].stack,bg='black',fg='wheat3')
            self.w.stack.pack(side='top')
            self.w.dealerButton = tk.Label(self.w.info,text = '',fg='wheat3',bg='black')
            self.w.dealerButton.pack(side='top')
            self.w.info.pack(side='top')
            self.w.c1 = tk.Label(self.w,image=room.no_card,background='black')
            self.w.c1.pack(side='left')
            self.w.c2 = tk.Label(self.w,image=room.no_card,background='black')
            self.w.c2.pack(side='left')
            self.w.grid(row=row,column=column,padx=25,pady=4)
            room.imageList[plyr] = self.w
            counter += 1
            # uses tkinter grid layout
            if counter < 5:
                column += 1
            elif counter == 5:
                column = 4
                row = 2
            elif counter == 6:
                column = 4
                row = 3
            elif counter == 7:
                column = 3
                row = 3
            elif counter == 8:
                column = 2
                row = 3
            elif counter == 9:
                column = 1
                row = 3
        room.imageList[room.table.seat_order[0]].dealerButton.configure(text='Dealer')
            
            
    # clean all gui elements for next hand, calls underlying table clean
    def clean(self):
        room.table.clean()
        for plyr in room.table.playerOrder:
            room.imageList[plyr].c1.configure(image=room.no_card)
            room.imageList[plyr].c2.configure(image=room.no_card)
        self.card1.configure(image=room.no_card)
        self.card2.configure(image=room.no_card)
        self.card3.configure(image=room.no_card)
        self.card4.configure(image=room.no_card)
        self.card5.configure(image=room.no_card)
        self.updateTableChips()
        room.playerWindow.card1.configure(image=room.no_card)
        room.playerWindow.card2.configure(image=room.no_card)
        room.playerWindow.plyrMsg.configure(text='')
        room.playerWindow.b1.destroy()
        room.playerWindow.b2.destroy()
        room.playerWindow.b3.destroy()
        room.playerWindow.wagerEntry.destroy()
        
    # resize background image
    def _resize_image(self,event):
        new_width = event.width # event.width is new window width
        new_height = event.height # event.height is new window height
        self.image = self.img_copy.resize((new_width, new_height)) # image becomes same size as window
        self.background_image = ImageTk.PhotoImage(self.image) # change to ImageTk
        self.background.configure(image =  self.background_image) 

class QuitGamePopup(object):
    def __init__(self,parent):
        self.top = tk.Toplevel(parent,bg='black',relief='ridge',bd=4)
        self.top.minsize(420,120)
        self.top.maxsize(420,120)
        self.players = tk.Label(self.top,text="Would You Like To Quit?",fg='burlywood1',bg='black',font=("Courier bold", 28))
        self.players.pack()
        self.yes = tk.Button(self.top,text='Yes',takefocus=1,font=("Gothic", 16),highlightbackground='black',command=self.getMeOutOfHere)
        self.yes.pack()
        self.no = tk.Button(self.top,takefocus=1,text="No, don't quit",font=("Gothic", 16),highlightbackground='black', command=self.top.destroy)
        self.no.pack()
        
    def getMeOutOfHere(self):
        self.top.destroy()
        sys.exit()

# Gets input from user numPlayers,stack_size,bigBlind 
class StartGamePopup(object):
    def __init__(self,root):
        self.top = tk.Toplevel(root,bg='black',relief='ridge',bd=4)
        self.top.geometry('700x360')
        self.top.grab_set()
        self.players = tk.Label(self.top,bg='black',fg='plum3',text="How Many players?\n2-9",font=('Courier bold',26))
        self.players.pack()
        self.playersEntry = tk.Scale(self.top,relief='raised',from_=2,to=9,orient='horizontal',bg='azure4',fg='gold')
        self.playersEntry.pack()
        self.stack_size = tk.Label(self.top,bg='black',fg='plum3',text="What is the starting stack size?\nIncrements of 10, at least 100",font=('Courier bold',26))
        self.stack_size.pack()
        self.stack_sizeEntry = tk.Scale(self.top,relief='raised',from_=200,to=10000,length=300,orient='horizontal',bg='azure4',fg='gold',resolution=10,command=lambda x: self.bigBlindEntry.config(to=(self.stack_sizeEntry.get()//10)))
        self.stack_sizeEntry.pack() 
        self.bigBlind = tk.Label(self.top,bg='black',fg='plum3',text="What is the big blind value?\nIncrements of 20,\n at most, ten percent of stack size",font=('Courier bold',26))
        self.bigBlind.pack()
        self.bigBlindEntry = tk.Scale(self.top,relief='raised',from_=20,to=self.stack_sizeEntry.get(),resolution=20,orient='horizontal',fg='gold',bg='azure4')
        self.bigBlindEntry.pack()
        self.okay_b=tk.Button(self.top,bg='black',highlightbackground='plum3',relief='raised',text='Ok',fg='gold',font=("Helvetica bold italic",26)\
       ,takefocus=1,command=self.start_game)
        self.okay_b.pack()
    
    # When 'OK' is pressed after 'Start Game'
    def start_game(self):
        room.num_plyrs = self.playersEntry.get()
        room.stack_size = self.stack_sizeEntry.get()
        room.bb_size = self.bigBlindEntry.get()
        room.table = table.Table(big_blind=room.bb_size,num_players=room.num_plyrs,num_chips=room.stack_size)
        #plyrList = ['player'+str(x+1) for x in range(room.num_plyrs)]
        self.top.destroy()
        room.table_window.create_player_images(room.table.seat_order)
        room.table_window.create_chip_and_card_images()
        for plyr in room.table.seat_order:
            room.imageList[plyr].c1.configure(image=room.card_back)
            room.imageList[plyr].c2.configure(image=room.card_back)
        room.player_window.populate(room.table.left_to_act[0], room.table.get_actions())
        

# just a geometry organizer for other classes
class Main_application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # 3 child widgets
        self.player_window = Player_window(self)
        self.start_game_bar = Start_game_bar(self)
        self.table_window = Table_window(self)
        # geometry packer
        self.player_window.pack(side="bottom", fill="x")
        self.start_game_bar.pack(side="top", fill="x")
        self.table_window.pack(side="right", fill="both", expand=True)
        # constant image references held in class that inherits from TK root
        self.card_back = ImageTk.PhotoImage(Image.open('res/cardBack.gif'))
        self.no_card = ImageTk.PhotoImage(Image.open('res/noCard.gif'))
        self.chips = ImageTk.PhotoImage(Image.open('res/chips.gif'))
        

root = tk.Tk()
root.geometry('1000x700')

room = Main_application(root)
room.pack(fill=tk.BOTH, expand=tk.YES)

pdb.run(root.mainloop())

