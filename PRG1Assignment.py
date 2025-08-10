#Program by: Likaelle Chua Ying Zhi Student ID:S10273207E
#PRG1 Assignment
#Game: Sundrop Caves
from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    #insert path to map file
    path = 'C:\\Users\\HomePC\\OneDrive\\Documents\\PRG1Assignment\\'
    map_file = open(path +filename, 'r')

    #sets changes to be effective globally (throughout program)
    global MAP_WIDTH
    global MAP_HEIGHT
    
    #deletes previous map structure
    map_struct.clear()
    
    for line in map_file:
        line = line.strip()
        #Defines lines as lists (becomes lists in a list)
        row = list(line)
        #Appends each line into the map structure
        map_struct.append(row)

    #Map width and height updated according to items in map_struct
    #with reference to first row/list
    MAP_WIDTH = len(map_struct[0])
    #with reference to number of rows/lists
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    #Player x-coordinate/column no.
    x = player['x']
    #Player y-coordinate/row no.
    y = player['y']

    #Player's movement range (1 step)/ the visible 3x3 area
    for row in range(y - 1, y + 2):  
        for column in range(x - 1, x + 2):  
            #Ensure that player will be in map range
            if 0 <= row < len(fog) and 0 <= column < len(fog[row]):
                #Clear fog when player moves
                fog[row][column] = False
    return

def initialize_game(game_map, fog, player):
    #name input
    name = input("Greetings, miner! What is your name? ")
    print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")

    # initialize map
    load_map("level1.txt", game_map)

    #initializes fog for new game
    fog.clear()
    #initial layout and grid for fog
    for row in game_map:
        fog.append([True] * len(row))

    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY

    #initialize player
    player['name'] = name                  #store the name you asked for
    player['capacity'] = 10                #starting backpack size
    player['pickaxe_level'] = 1            #1=copper, 2=silver, 3=gold
    player['portal_x'] = player['x']       #portal at starting position
    player['portal_y'] = player['y']

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    if not game_map:
        return

    height = len(game_map)
    width = len(game_map[0])

    # Top border
    print("+" + "-" * width + "+")

    for y in range(height):
        print("|", end="")
        for x in range(width):
            #Overlay player and portal regardless of fog
            if x == player.get('x', -1) and y == player.get('y', -1):
                tile = "M"
            elif x == player.get('portal_x', -9999) and y == player.get('portal_y', -9999):
                tile = "P"
            else:
                #Show real tile only if not fogged, otherwise '?'
                tile = game_map[y][x] if not fog[y][x] else "?"
            print(tile, end="")
        print("|")
    #Bottom border
    print("+" + "-" * width + "+")
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    #Player position coordinates
    position_x = player['x']
    position_y = player['y']

    #visible range around player (1 tiles in each direction)
    visible_range = 1

    #range of visible rows
    for y in range(position_y-visible_range, position_y+visible_range+1):
        #range of visible columns
        for x in range(position_x-visible_range, position_x+visible_range+1):
            #Ensure coordinates are in map bounds
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[y]):
                if x == position_x and y == position_y:
                    print("M", end="")  #Player
                elif fog[y][x]:
                    print("?", end="")  #Fog
                else:
                    print(game_map[y][x], end="") 
            else:
                print(" ", end="") 
        print()
    return

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    #x-coordinates, y-coordinates
    print(f"Location: ({player['x']}, {player['y']})")
    #mined materials
    print(f"Copper: {player['copper']}")
    print(f"Silver: {player['silver']}")
    print(f"Gold: {player['gold']}")
    #no. of days
    print(f"Day: {player['day']}")
    #turns left
    print(f"Turns left today: {player['turns']}")
    if 'name' in player:
       print(f"Name: {player['name']}")
       # portal position
       px = player.get('portal_x', player['x'])
       py = player.get('portal_y', player['y'])
       print(f"Portal position: ({px}, {py})")
       # pickaxe level label
       lvl = player.get('pickaxe_level', 1)
       lvl_name = {1: 'copper', 2: 'silver', 3: 'gold'}.get(lvl, '?')
       print(f"Pickaxe level: {lvl} ({lvl_name})")
       print("------------------------------")
       # load / capacity
       load = player.get('copper', 0) + player.get('silver', 0) + player.get('gold', 0)
       cap = player.get('capacity', 10)
       print(f"Load: {load} / {cap}")
       print("------------------------------")
       # GP and steps
       print(f"GP: {player.get('GP', 0)}")
       print(f"Steps taken: {player.get('steps', 0)}")
       print("-------------------------------")
       return

# This function saves the game
import json
def save_game(game_map, fog, player):
    data = {"game_map": game_map,
        "fog": fog,
        "player": player}
    try:
        with open('gameprogress.json', "w") as f:
            json.dump(data, f)
        print("Game saved.")
    except Exception as e:
        print(f"Save failed: {e}")
    return
        
# This function loads the game
import json
def load_game(game_map, fog, player):
    try:
        with open('gameprogress.json', "r") as f:
            data = json.load(f)

        #Restore game_map
        game_map.clear()
        for row in data["game_map"]:
            game_map.append(row)
        global MAP_WIDTH, MAP_HEIGHT
        MAP_HEIGHT = len(game_map)
        MAP_WIDTH = len(game_map[0]) if MAP_HEIGHT > 0 else 0

        #Restore fog
        fog.clear()
        for row in data["fog"]:
            fog.append(row)

        #Restore player dictionary
        player.clear()
        for key, value in data["player"].items():
            player[key] = value

        print("Game loaded.")
    except FileNotFoundError:
        print("No saved game found.")
    except Exception as e:
        print(f"Load failed: {e}")
    return


#Highscores
SCORES_FILE = "highscores.json"

def _load_scores():
    try:
        with open(SCORES_FILE, "r") as f:
            data = json.load(f)
            # old files or bad data guard
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except Exception:
        return []

def _save_scores(scores):
    try:
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f)
    except Exception as e:
        print(f"Could not save scores: {e}")

def _score_key(s):
    # sort by fewer days, then fewer steps, then HIGHER GP
    return (s.get("days", 999999), s.get("steps", 999999), -s.get("gp", 0))

def record_high_score(player):
    """Call this right AFTER a win is detected."""
    entry = {
        "name": player.get("name", "miner"),
        "days": player.get("day", 0),      # day count AFTER selling (your code already increments)
        "steps": player.get("steps", 0),
        "gp": player.get("GP", 0)
    }
    scores = _load_scores()
    scores.append(entry)
    scores.sort(key=_score_key)
    scores = scores[:5]  # keep top 5
    _save_scores(scores)

def show_high_scores():
    scores = _load_scores()
    print()
    print("----- Top Scores -----")
    if not scores:
        print("No scores yet. Win a game to create one!")
        print("----------------------")
        return
    # header
    print("Rank  Name                Days   Steps   GP")
    print("--------------------------------------------")
    for i, s in enumerate(scores, start=1):
        print(f"{i:>4}  {s.get('name','miner'):<18} {s.get('days',0):>4}   {s.get('steps',0):>5}   {s.get('gp',0):>4}")
    print("--------------------------------------------")

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    print(f'Day {player["day"]+1}')
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")



def buy_shop(player):
    while True:
        print()
        print("---------------------- Shop Menu ----------------------")
        upgrade_cost = player['capacity'] * 2     #price = 2 × current capacity
        print(f"(B)ackpack upgrade to carry {player['capacity'] + 2} items for {upgrade_cost} GP")
        print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
        print("(L)eave shop")
        print("-------------------------------------------------------")
        print(f"GP: {player['GP']}")
        print("-------------------------------------------------------")

        choice = input("Your choice? ").strip().lower()

        if choice == 'b':
            if player['GP'] >= upgrade_cost:
                player['GP'] -= upgrade_cost
                player['capacity'] += 2
                print(f"Congratulations! You can now carry {player['capacity']} items!")
            else:
                print("You don't have enough GP to upgrade your backpack.")
        elif choice == 'p':   #pickaxe upgrade handling
            if player['pickaxe_level'] == 1 and player['GP'] >= 50:
               player['GP'] -= 50
               player['pickaxe_level'] = 2
               print("Your pickaxe is now Level 2! You can mine silver.")
            else:
               print("Cannot upgrade pickaxe (not enough GP or already upgraded).")
        elif choice == 'l':
            break
        else:
            print("Invalid choice. Please choose again.")



def current_load(player):
    """Return the current number of ores carried."""
    return player.get('copper', 0) + player.get('silver', 0) + player.get('gold', 0)

def capacity_left(player):
    return player.get('capacity', 10) - current_load(player)

def can_mine(tile, player):
    """Pickaxe gate: C=1, S=2, G=3."""
    req = {'C':1, 'S':2, 'G':3}
    return tile in req and player.get('pickaxe_level',1) >= req[tile]

def print_mine_screen(game_map, fog, player):
    """Show the mine viewport and HUD similar to screenshots."""
    print("----------------------------------------------------------")
    print(f"                          DAY {player['day'] + 1}")
    print("----------------------------------------------------------")
    print(f"DAY {player['day'] + 1}")
    print("+---+")
    draw_view(game_map, fog, player)  #existing 3×3 function
    print("+---+")
    print(f"Turns left: {player['turns']:2}    Load: {current_load(player)} / {player['capacity']}    Steps: {player['steps']}")
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

def sell_all_ore(player):
    """
    Sell all ores using the assignment's random price ranges:
      copper: 1–3, silver: 5–8, gold: 10–18 (per piece)
    """
    price_c = randint(*prices['copper'])
    price_s = randint(*prices['silver'])
    price_g = randint(*prices['gold'])

    c = player.get('copper', 0)
    s = player.get('silver', 0)
    g = player.get('gold', 0)

    total_earn = 0

    if c > 0:
        earn = c * price_c
        print(f"You sell {c} copper ore for {earn} GP.")
        total_earn += earn
        player['copper'] = 0

    if s > 0:
        earn = s * price_s
        print(f"You sell {s} silver ore for {earn} GP.")
        total_earn += earn
        player['silver'] = 0

    if g > 0:
        earn = g * price_g
        print(f"You sell {g} gold ore for {earn} GP.")
        total_earn += earn
        player['gold'] = 0

    player['GP'] = player.get('GP', 0) + total_earn
    print(f"You now have {player['GP']} GP!")

def arrive_in_town_from_mine(game_map, fog, player):
    """
    Handle returning to town:
      - sell all ore (prints each line + 'You now have ... GP!')
      - advance to next day
      - reset turns
      - check win and bounce to main if >= WIN_GP
      - move player to town tile (0,0)
    """
    sell_all_ore(player)                 #prints sale lines + balance line
    player['day'] += 1                  
    player['turns'] = TURNS_PER_DAY

    #WIN check (do it right after starting the new day)
    if check_win_and_go_main(player):
        # we already set game_state = 'main' above
        return

    #back to town position & reveal
    player['x'], player['y'] = 0, 0
    clear_fog(fog, player)


def move_player(action, game_map, fog, player):
    """Handle WASD, mining, turns/steps, and return a status dict."""
    dx = dy = 0
    if action == 'W': dy = -1
    elif action == 'S': dy = 1
    elif action == 'A': dx = -1
    elif action == 'D': dx = 1
    else:
        return {"to_town": False, "exhausted": False, "stepped_on_town": False}

    nx = player['x'] + dx
    ny = player['y'] + dy

    to_town = False
    exhausted = False
    stepped_on_town = False

    def consume_time():
        player['steps'] += 1
        if player['turns'] > 0:
            player['turns'] -= 1

    #off-map (still costs a turn)
    if not (0 <= ny < len(game_map) and 0 <= nx < len(game_map[ny])):
        print("You can't go there.")
        consume_time()
    else:
        tile = game_map[ny][nx]

        #full pack + mineral destination -> block
        if tile in ('C','S','G') and capacity_left(player) <= 0:
            print("You can't carry any more, so you can't go that way.")
            consume_time()
        else:
            #move
            player['x'], player['y'] = nx, ny
            clear_fog(fog, player)

            #mine (if allowed by pickaxe)
            if tile in ('C','S','G') and can_mine(tile, player):
                if tile == 'C': want = randint(1,5); ore = 'copper'
                elif tile == 'S': want = randint(1,3); ore = 'silver'
                else:             want = randint(1,2); ore = 'gold'

                left = max(0, capacity_left(player))
                take = min(want, left)
                if take > 0:
                    player[ore] += take
                    print("------------------------------------------------")
                    print(f"You mined {take} piece(s) of {ore}.")
                    if take < want:
                        print(f"...but you can only carry {take} more piece(s)!")

            #stepped on T?
            if tile == 'T':
                print("You return to town.")
                to_town = True
                stepped_on_town = True

            consume_time()

    #exhausted auto-portal
    if player['turns'] == 0 and not to_town:
        print("You are exhausted.")
        print("You place your portal stone here and zap back to town.")
        player['portal_x'], player['portal_y'] = player['x'], player['y']
        exhausted = True
        to_town = True
    return {"to_town": to_town, "exhausted": exhausted, "stepped_on_town": stepped_on_town}



def enter_mine(game_map, fog, player):
    #appear at portal if set, else town (0,0)
    start_x = player.get('portal_x', 0)
    start_y = player.get('portal_y', 0)
    player['x'], player['y'] = start_x, start_y
    clear_fog(fog, player)

    while True:
        print_mine_screen(game_map, fog, player)
        action = input("Action? ").strip().upper()

        if action in ('W','A','S','D'):
            status = move_player(action, game_map, fog, player)
            if status["to_town"]:
                arrive_in_town_from_mine(game_map, fog, player)
                return  #back to town

        elif action == 'M':
            draw_map(game_map, fog, player)

        elif action == 'I':
            show_information(player)

        elif action == 'P':
            print("----------------------------------------------------------")
            print("You place your portal stone here and zap back to town.")
            player['portal_x'], player['portal_y'] = player['x'], player['y']
            arrive_in_town_from_mine(game_map, fog, player)
            return

        elif action == 'Q':
            #quit mine to main menu 
            return

        else:
            print("Invalid action.")


def check_win_and_go_main(player):
    if player.get('GP', 0) >= WIN_GP:
        print("----------------------------------------------------------")
        print(f"Woo-hoo! Well done, {player.get('name','miner')}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
        print("----------------------------------------------------------")
        #record your run in highscores
        record_high_score(player) 
        #jump to main menu
        global game_state
        game_state = 'main'
        return True
    return False
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
while game_state == 'main':
    show_main_menu()
    choice = input("Your choice? ").upper()
    if choice == "N":
       #start new game
       initialize_game(game_map,fog,player)
       game_state = 'town'
    elif choice == "L":
       #load saved game
       load_game(game_map, fog, player)
       game_state = 'town'
    elif choice == "H":
       #display high scores
       show_high_scores()
    elif choice == "Q":
       #quit game
       print("Thanks for playing Sundrop Caves!")
       break
    else:
       print("Invalid choice. Please choose N, L, H, or Q.")
       game_state = 'main'


while game_state == 'town':
   show_town_menu()
   choice_town = input("Your choice? ").upper()
   if choice_town == 'B':
       buy_shop(player)                
   elif choice_town == 'I':
       show_information(player)
   elif choice_town == 'M':
       draw_map(game_map, fog, player)  
   elif choice_town == 'E':
       enter_mine(game_map, fog, player)
       if game_state == 'main':   #player won
          break 
   elif choice_town == 'V':
       save_game(game_map, fog, player)
   elif choice_town == 'Q':
       game_state = 'main'