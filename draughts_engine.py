#!/usr/bin/python3

import re

def draw_checkerboard(status,space="▒",white_norm="h",white_knight="H",black_norm="b",black_knight="B",empty=" ",column="12345678",frstrow=" abcdefgh\n"):
	""" Draw a checkerboard, status is the virtual representation of the board, as a bi-dimensional array, white/black norm/knight are the representation of the pieces
	space is a non-walkable cell, empty is a walkable cell, column contains labels for the left column, frstrow the labels for the first row.
	"""
	bstr = ""
	bstr += frstrow
	for row in range(0,len(status)):
		bstr += column[row]		
		if row % 2 == 0:
			bstr += space 
		for cell in range(0,int(len(status)/2)):
			if status[row][cell] == 1:    #black normal piece
				bstr += black_norm
			elif status[row][cell] == 2:  #white normal piece
				bstr += white_norm
			elif status[row][cell] == 3:  #black knight piece
				bstr += black_knight
			elif status[row][cell] == 4:  #white knight piece
				bstr += white_knight
			else:						  #empty 
				bstr += empty
			if (cell < 3):
				bstr += space
		if row % 2 !=0: #odd lines ends with space and a line feed, even ones just with the line feed
			bstr += space+"\n"
		else:
			bstr += "\n"
	return bstr
		
def position_resolver(pos,board):
	"""Checks if the position is valid and wether it contains a piece or not"""
	row,col = row_column_translation(pos[1],pos[0])
	if (col == -1):
		return -1
	else:
		return board[row][col]

def row_column_translation(row,col):
	"""Converts a coordinate made by a letter/number couple in the index usable with the array that represents the board"""

	row = int(row) - 1
	if row % 2 != 0:
		cols = range(ord("a"),ord("a")+7,2)
	else:
		cols = range(ord("b"),ord("b")+7,2)
	if ord(col) not in cols:
		return -1,-1
	else:
		return row,cols.index(ord(col))

def traslate_coord(pos):
	for en,p in enumerate(pos):
		temp_col = chr( (int(pos[en][1])-1)+ord("a") )
		temp_row = ord(pos[en][0])-ord("a")
		pos[en] = temp_col
		pos[en] += str(temp_row +1)
	return pos

def valid_move(pos_toParse,turn,board,inversion=False):
	"""Checks if the move is valid, execute it and returns the updated board"""
	#pos = pos_toParse.split(" ") #tricky part, pos[0] is the starting cell, pos[1] to pos[n] the destination point(s), for every coord, [x][0] is the column (the letter) and [x][1] the row (the number)
	pos = re.findall("\\b[abcdefgh][12345678]\\b",pos_toParse)	#both row-col and col-row are accepted
	if len(pos) == 0:											
		pos = re.findall("\\b[12345678][abcdefgh]\\b",pos_toParse)
		for en,x in enumerate(pos):
			pos[en] = x[1]+x[0]
	
	if inversion:
		pos = traslate_coord(pos)
	
	if len(pos) < 2: #less than 2 coords were given, movement is invalid
		return -1
	row_start,col_start = row_column_translation(pos[0][1],pos[0][0])
	if(row_start == -1):
		return -1
	if turn == 1:			#black turn
		valid_piece = (1,3)
		foe_piece = (2,4)
	else:					#white turn
		valid_piece = (2,4)
		foe_piece = (1,3)
	start_cell = position_resolver(pos[0],board)
	if start_cell not in valid_piece: #selected an opponent's piece or an empty cell
		return -1
	if ((start_cell == 1 and abs(ord(pos[1][0]) - ord(pos[0][0])) == 1 and ord(pos[0][1]) - ord(pos[1][1]) == -1) or (start_cell == 2 and abs(ord(pos[1][0]) - ord(pos[0][0])) == 1 and ord(pos[0][1]) - ord(pos[1][1]) == 1) or ((start_cell == 4 or start_cell == 3) and abs(ord(pos[1][0]) - ord(pos[0][0])) == 1 and abs(ord(pos[1][1]) - ord(pos[0][1])) == 1) and len(pos) == 2 ):		
		move_to = position_resolver(pos[1],board) #check non-capturing movement, to be valid it must be 1 col shift and 1 row shift, for norm pieces direction is important, and it must be a single move
		if (move_to == 0): #if the cell is empty, the move is valid
			row,col = row_column_translation(pos[0][1],pos[0][0])
			board[row][col] = 0
			row,col = row_column_translation(pos[1][1],pos[1][0])
			if ((row == 0) and start_cell == 2): #piece promotion
				start_cell = 4
			if ((row == 7) and start_cell == 1):
				start_cell = 3
			board[row][col] = start_cell
			return board
		else: #destination cell is not empty
			return -1
	else:
		for x in range(0,len(pos) -1):
			if (start_cell == 1 and abs(ord(pos[1][0]) - ord(pos[0][0])) == 2 and ord(pos[0][1]) - ord(pos[1][1]) == -2) or (start_cell == 2 and abs(ord(pos[1][0]) - ord(pos[0][0])) == 2 and ord(pos[0][1]) - ord(pos[1][1]) == 2) or ((start_cell == 4 or start_cell == 3) and abs(ord(pos[1][0]) - ord(pos[0][0])) == 2 and abs(ord(pos[1][1]) - ord(pos[0][1])) == 2):
				move_to = position_resolver(pos[1],board)
				if (move_to == 0): #check if destination is empty
					shift_x = int((ord(pos[1][0]) - ord(pos[0][0]))/2)
					shift_y = int((ord(pos[1][1]) - ord(pos[0][1]))/2)
					if (start_cell == 1):#normal pieces can capture kings (to do: optional rule)
						foe_piece = (2,4)
						#foe_piece = (2,)
					elif (start_cell == 2):
						foe_piece = (1,3)
						#foe_piece = (1,)
					row,col = row_column_translation(chr(ord(pos[0][1])+shift_y),chr(ord(pos[0][0])+shift_x)) #check if an opponent piece lies in between start and destination
					if (board[row][col] in foe_piece):
						board[row][col] = 0
						row,col = row_column_translation(pos[0][1],pos[0][0])
						board[row][col] = 0
						row,col = row_column_translation(pos[1][1],pos[1][0])
						board[row][col] = start_cell
						if ((row == 0) and start_cell == 2): #piece promotion
							start_cell = 4
						if ((row == 7) and start_cell == 1):
							start_cell = 3
						pos.pop(0) #if there are other moves this check loops
					else: #one of the pieces moves are invalid
						return -1
				else: #destination not empty
					return -1
			else:
				return -1
		return board

def init_board():
	checkerboard = []
	for row in range(0,8):
		if (row <= 2):
			checkerboard.append([1,1,1,1])
		elif (row >= 5):
			checkerboard.append([2,2,2,2])
		else:
			checkerboard.append([0,0,0,0])
	return checkerboard

def checkWin(board):
	black_won = True
	white_won = True
	for row in board:
		if (1 in row) or (3 in row):
			white_won = False
		if (2 in row) or (4 in row):
			black_won = False
	return (white_won,black_won)

def main():
	import sys
	column_i = "12345678"
	frstrow_i = " abcdefgh\n"
	inverted = False
	try:
		if sys.argv[1] == "i":
			column_i = "abcdefgh"
			frstrow_i = " 12345678\n"
			inverted = True
	except IndexError:
		pass
	main_board = init_board()
	s = ""
	turn = False
	while (s !="q"):
		vis_board = draw_checkerboard(main_board,column=column_i,frstrow=frstrow_i)
		print(vis_board)
		if turn:
			s = input("Black move:")
		else:
			s = input("White move:")
		if (s !="q"):
			result = valid_move(s,turn,main_board,inversion=inverted)
			if result != -1:
				main_board = result
				winner = checkWin(main_board)
				if winner[0]:
					print("White won this game.")
					return turn
				if winner[1]:
					print("Black won this game.")
					return turn
				turn = not turn
			else:
				print("Invalid move")
	return -1

if __name__ == "__main__":
	main()
	quit()
