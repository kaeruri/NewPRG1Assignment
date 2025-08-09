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
    # initialize map
    load_map("level1.txt", game_map)

    #name input
    name = input("Greetings, miner! What is your name? ")
    print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")
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

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    #rows
    for y in range(len(game_map)):
     #columns
     for x in range(len(game_map[y])):
         #out of map range
         if not fog[y][x]:
             print(game_map[y][x], end="")
         else:
             #fog of war
             print("?", end="")
     print()
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    #Player position coordinates
    position_x = player['x']
    position_y = player['y']

    #visible range around player (2 tiles in each direction)
    visible_range = 1

    #range of visible rows
    for y in range(position_x-visible_range, position_x+visible_range+1):
        #range of visible columns
        for x in range(position_y-visible_range, position_y+visible_range+1):
            #Ensure coordinates are in map bounds
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[y]):
                #Check if the tile is visible (not covered by fog)
                if not fog[y][x]:
                    print(game_map[y][x], end="")
                else:
                    print("M", end="")
            else:
                print("?", end="")
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
    #earned money
    print(f"GP: {player['GP']}")
    #no. of days
    print(f"Day: {player['day']}")
    #turns left
    print(f"Turns left today: {player['turns']}")
    print("-------------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#   print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    print(f'Day {player["day"]}')
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

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
