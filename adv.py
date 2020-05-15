from room import Room
from player import Player
from world import World
from util import Queue, Stack
import random
from ast import literal_eval
import sys
sys.setrecursionlimit(1500)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
s = Stack() # stack for backtracking

visited[player.current_room.id] = player.current_room.get_exits()

opposites = {'n' : 's', 's' : 'n', 'e' : 'w', 'w' : 'e'}

def dft_recursive(room):

    if room.id not in visited: # if we haven't been to the room
        visited[room.id] = room.get_exits() # store it and it's exits in visited
        to_last_room = opposites[traversal_path[-1]] # get inverse direction of our last move
        visited[room.id].remove(to_last_room) # and remove that exit

    if len(visited[player.current_room.id]) < 1: # if there are no exits left
        # print(player.current_room.id)
        to_last_room = s.pop() # take our last move off the stack
        traversal_path.append(to_last_room) # and backtrack
        player.travel(to_last_room)

    else: # we have exits
        direction = visited[player.current_room.id].pop() # grab the last exit
        s.push(opposites[direction]) # put it on the stack
        traversal_path.append(direction) # add it to the path
        player.travel(direction) # travel to it

    if len(visited) < len(room_graph): # if we don't have all the rooms
        dft_recursive(player.current_room) # call it again
            
dft_recursive(player.current_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
