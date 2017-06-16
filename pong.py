#pong in pygame!

"""
TASKS
set up the window
make ball bounce around every second, obeying laws of momentum and angles at walls/paddles
one paddle is faster (but not as fast as the ball) and follows the mouse cursor
the AI paddle is slightly slower and follows the ball endlessly
ball hitting te side walls (the goals) resets the game and increments the points
"""

import pygame

import ctypes
ctypes.windll.user32.SetProcessDPIAware() #to negate Windows' 125% stretching

from random import choice
from time import sleep
player1Score = 0
player2Score = 0
BLACK = (0,0,0)
GRAY  = (200, 200, 200)
WHITE = (255, 255, 255)


pygame.init()
TREBUCHET = pygame.font.SysFont("couriernew", 200)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
x, y = screen.get_size()
screen.fill(WHITE)

playerPaddle = pygame.Rect(int(x/20), 100, 30, 200)
pygame.draw.rect(screen, BLACK, playerPaddle)

AIPaddle = pygame.Rect(int(x*19/20), 100, 30, 200)
pygame.draw.rect(screen, BLACK, AIPaddle)

ball = pygame.Rect(x/2 - 20, y/2 - 20, 40, 40)
pygame.draw.circle(screen, BLACK, (ball.centerx, ball.centery), int(ball.width/2))

ballMotionX = choice([-5, 5]) #could also have other values in these arrays. the numbers represent the ball's velocity
ballMotionY = choice([-5, 5])

pygame.display.flip() #sets up the window's visuals.
##########################################################

def move_ball(xOffset, yOffset):
	pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), int(ball.width/2))
	ball.move_ip(xOffset, yOffset)
	pygame.draw.circle(screen, BLACK, (ball.centerx, ball.centery), int(ball.width/2))

def reset_ball():
	pygame.draw.rect(screen, WHITE, ball)
	ball.x = x/2 - 20
	ball.y = y/2 - 20
	pygame.draw.circle(screen, BLACK, (ball.centerx, ball.centery), int(ball.width/2))

def blitScores():
	pygame.draw.rect(screen, WHITE, [int(x/5), 100, 700, 200])
	screen.blit(TREBUCHET.render(str(player1Score), 0, GRAY), (int(x/5), 100))
	
	pygame.draw.rect(screen, WHITE, [int(x*(4/5)), 100, 700, 200])
	screen.blit(TREBUCHET.render(str(player2Score), 0, GRAY), (int(x*(4/5)), 100))

	#optional: make the score text change color based on how high the score is

while(True):
	pygame.display.flip()
	screen.blit(pygame.font.SysFont("couriernew", 24).render("Press q to quit", 0, (128, 100, 100)), (10, 10))

	blitScores()
	move_ball(ballMotionX, ballMotionY)
	sleep(.005)

	if ball.top == 0 or ball.bottom == y:
		ballMotionY *= -1

	if ball.left == 0 or ball.right == x:
		
		if ball.left == 0: #left
			player2Score += 1
		else:
			player1Score += 1
		
		reset_ball()
		ballMotionX = choice([-5, 5])
		ballMotionY = choice([-5, 5])
		
	# PADDLE/BALL INTERACTION LOGIC
	if (abs(ball.left-playerPaddle.right)<5 and ball.centery > playerPaddle.top and ball.centery < playerPaddle.bottom):
		ballMotionX *= -1
	elif (abs(ball.right-AIPaddle.left)<5 and ball.centery > AIPaddle.top and ball.centery < AIPaddle.bottom):
		ballMotionX *= -1


	# PLAYER PADDLE MOVEMENT LOGIC
	mouse_y = pygame.mouse.get_pos()[1]
	if playerPaddle.centery-3 > mouse_y:
		pygame.draw.rect(screen, WHITE, playerPaddle)
		playerPaddle.move_ip(0, -3) #paddle velocity
		
	elif playerPaddle.centery < mouse_y:
		pygame.draw.rect(screen, WHITE, playerPaddle)
		playerPaddle.move_ip(0, 3)
	
	pygame.draw.rect(screen, BLACK, playerPaddle)

	# AI PADDLE MOVEMENT LOGIC. It's supposed to move slower than the player paddle because its smarter
	if AIPaddle.centery > ball.centery:
		pygame.draw.rect(screen, WHITE, AIPaddle)
		AIPaddle.move_ip(0, -3)
		
	elif AIPaddle.centery < ball.centery:
		pygame.draw.rect(screen, WHITE, AIPaddle)
		AIPaddle.move_ip(0, 3)
	
	pygame.draw.rect(screen, BLACK, AIPaddle)

	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_F4 or event.key == pygame.K_q)):
				exit()

