#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import logging
import random
import webapp2

# Reads json description of the board and provides simple interface.
weight = [[5,0,4,4,4,4,0,5],
[0,0,1,1,1,1,0,0],
[4,1,3,3,3,3,1,4],
[4,1,3,2,2,3,1,4],
[4,1,3,2,2,3,1,4],
[4,1,3,3,3,3,1,4],
[0,0,1,1,1,1,0,0],
[5,0,4,4,4,4,0,5]]

depth =3
class Game:
	# Takes json or a board directly.
	def __init__(self, body=None, board=None):
                if body:
		        game = json.loads(body)
                        self._board = game["board"]
                else:
                        self._board = board
	def Pos(self, x, y):
		return Pos(self._board["Pieces"], x, y)

	def Next(self):
		return self._board["Next"]
	def evaluate(self, player): 
		weight_sum = 0 
		for x, line in enumerate(self._board['Pieces']): 
			for y, sq in enumerate(line):
				if sq == player:
					weight_sum += weight[x][y]
		return weight_sum 
	def ValidMoves(self):
                moves = []
                for y in xrange(1,9):
                        for x in xrange(1,9):
                                move = {"Where": [x,y],
                                        "As": self.Next()}
                                if self.NextBoardPosition(move):
                                        moves.append(move)
                return moves
 
 	def __UpdateBoardDirection(self, new_board, x, y, delta_x, delta_y):
		player = self.Next()
		opponent = 3 - player
		look_x = x + delta_x
		look_y = y + delta_y
		flip_list = []
		while Pos(new_board, look_x, look_y) == opponent:
			flip_list.append([look_x, look_y])
			look_x += delta_x
			look_y += delta_y
		if Pos(new_board, look_x, look_y) == player and len(flip_list) > 0:
			SetPos(new_board, x, y, player)
			for flip_move in flip_list:
				flip_x = flip_move[0]
				flip_y = flip_move[1]
				SetPos(new_board, flip_x, flip_y, player)
                        return True
                return False
	def NextBoardPosition(self, move):
		x = move["Where"][0]
		y = move["Where"][1]
                if self.Pos(x, y) != 0:
                        # x,y is already occupied.
                        return None
		new_board = copy.deepcopy(self._board)
                pieces = new_board["Pieces"]

		if not (self.__UpdateBoardDirection(pieces, x, y, 1, 0)
                        | self.__UpdateBoardDirection(pieces, x, y, 0, 1)
		        | self.__UpdateBoardDirection(pieces, x, y, -1, 0)
		        | self.__UpdateBoardDirection(pieces, x, y, 0, -1)
		        | self.__UpdateBoardDirection(pieces, x, y, 1, 1)
		        | self.__UpdateBoardDirection(pieces, x, y, -1, 1)
		        | self.__UpdateBoardDirection(pieces, x, y, 1, -1)
		        | self.__UpdateBoardDirection(pieces, x, y, -1, -1)):
                        # Nothing was captured. Move is invalid.
                        return None
                
                # Something was captured. Move is valid.
                new_board["Next"] = 3 - self.Next()
		return Game(board=new_board)

def Pos(board, x, y):
	if 1 <= x and x <= 8 and 1 <= y and y <= 8:
		return board[y-1][x-1]
	return None

# Set piece on the board at (x,y) coordinate
def SetPos(board, x, y, piece):
	if x < 1 or 8 < x or y < 1 or 8 < y or piece not in [0,1,2]:
		return False
	board[y-1][x-1] = piece

# Debug function to pretty print the array representation of board.
def PrettyPrint(board, nl="<br>"):
	s = ""
	for row in board:
		for piece in row:
			s += str(piece)
		s += nl
	return s

def PrettyMove(move):
	m = move["Where"]
	return '%s%d' % (chr(ord('A') + m[0] - 1), m[1])

def ABnegaMax(game, depth, alpha, beta):
	if depth == 0: 
		return game.evaluate(game.Next()), None
	bestMove = None
	bestScore = -100000
	for move in game.ValidMoves(): 
		gameCopy = game.NextBoardPosition(move)
		score, amove = ABnegaMax(gameCopy, depth-1, -beta, -max(alpha, bestScore))
		score = -score 
		if score > bestScore: 
			bestScore = score
			bestMove = move
			if (bestScore >= beta):
				return bestScore, bestMove
	return bestScore, bestMove

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if not self.request.get('json'):
          self.response.write("""
							<body><form method=get>
							Paste JSON here:<p/><textarea name=json cols=80 rows=24></textarea>
							<p/><input type=submit>
							</form>
							</body>
							""")
          return
        else:
          g = Game(self.request.get('json'))
          score, move = ABnegaMax(g, depth, -10000, 10000)
          self.response.write(PrettyMove(move))

    def post(self):
    	g = Game(self.request.body)
        score, move = ABnegaMax(g, depth, -10000, 10000)
        self.response.write(PrettyMove(move))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
