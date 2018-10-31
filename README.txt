README.txt

1) start game button, gets user input

2) instantiate underlying Table class with user input(from table.py)

3) table seats players, deals cards and posts blinds for first hand

4) active player is determined (skip all-in players, only 1 player not-all-in auto checks down)

5) get_legal_actions called with active player, returns legal actions to gui

6) apply_action() is called with user input, changes table state

7) check for end of hand (only 1 player in hand OR showdown() no players left2act and round == river)
  7b) if end of hand, reward player, next hand
  7c) if showdown, check for sidepots, call showdown on successive sidepots(pot), next_hand()

8) go to 4
