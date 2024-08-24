import pygame
from network import Network
from player import Player 

width = 800
height = 600
treasure_pos = (300,300)
maze = [
    "##########",
    "#        #",
    "#  ##### #",
    "#  #     #",
    "#  #     #",
    "#  #     #",
    "#  #     #",
    "#     #  #",
    "#     #  #",
    "##########"
]
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def draw_maze():
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == "#":
                pygame.draw.rect(win, (0, 0, 0), (x * 40, y * 40, 40, 40))

def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    draw_maze()
    player.draw(win)
    player2.draw(win)
    pygame.draw.circle(win, (255, 255, 0), treasure_pos, 10)

    pygame.display.update()

def main():
    run = True
    n = Network()
    # Attempt to establish the connection
    if not n.connect():
        print("Failed to connect to the server.")
        return

    p = n.getP()
    if p is None:
        print("Failed to receive player data from the server.")
        return
    player = p
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p2 = n.send(p)
        if p2 is None:
            print("Failed to receive updated player data from the server.")
            break
      
        if p.check_treasure_collision() or p2.check_treasure_collision():
          if p.check_treasure_collision() and p2.check_treasure_collision():
            print("Both players reached the treasure! It's a tie!")
          elif p.check_treasure_collision():
             if p == player:
                    print("You win!")
             else:
                    print("You lose!")
          else:
            if p2 == player:
                    print("You win!")
            else:
                    print("You lose!")
          run = False  # End the game loop
          break


        p.move()
        redrawWindow(win, p, p2)
    pygame.quit()

main()
