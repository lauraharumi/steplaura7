#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import random

body = """
{"board":{"Pieces":[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,0,1,1,1,0],[0,0,0,0,2,1,2,0],[0,0,0,2,1,0,0,0]],"Next":2},"gamekey":"ag5zfnN0ZXAtb3RoZWxsb3IRCxIER2FtZRiAgIDAqLGWCww","history":[{"Where":[5,6],"As":1},{"Where":[6,6],"As":2},{"Where":[3,4],"As":1},{"Where":[5,7],"As":2},{"Where":[6,7],"As":1},{"Where":[7,7],"As":2},{"Where":[5,8],"As":1},{"Where":[4,8],"As":2},{"Where":[7,6],"As":1}],"valid_moves":[{"Where":[3,3],"As":2},{"Where":[5,3],"As":2},{"Where":[3,5],"As":2},{"Where":[7,5],"As":2},{"Where":[6,8],"As":2}]}
"""
body = """
 {"board":{"Pieces":[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,2,1,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],"Next":1},"gamekey":"ag5zfnN0ZXAtb3RoZWxsb3IRCxIER2FtZRiAgICA-q6cCww","history":null,"valid_moves":[{"Where":[4,3],"As":1},{"Where":[3,4],"As":1},{"Where":[6,5],"As":1},{"Where":[5,6],"As":1}]}
"""
weight = [
[5,0,4,4,4,4,0,5],
[0,0,1,1,1,1,0,0],
[4,1,3,3,3,3,1,4],
[4,1,3,2,2,3,1,4],
[4,1,3,2,2,3,1,4],
[4,1,3,3,3,3,1,4],
[0,0,1,1,1,1,0,0],
[5,0,4,4,4,4,0,5]]

class Game:
	def __init__(self, body=None, board=None):
                if body:
		        game = json.loads(body)
                        self._board = game["board"]
                else:
                        self._board = board
	def DrawBoard(self): #added for understanding
		for line in self._board["Pieces"]:
			print line
		print "\n"
	def Pos(self, x, y):
		return Pos(self._board["Pieces"], x, y)
	def Next(self):
		return self._board["Next"]
	def evaluate(self, player): 
		weight_sum = 0 
		for x, line in enumerate(g._board['Pieces']): 
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
                new_board["Next"] = 3 - self.Next()
		return Game(board=new_board)

def Pos(board, x, y):
	if 1 <= x and x <= 8 and 1 <= y and y <= 8:
		return board[y-1][x-1]
	return None

def SetPos(board, x, y, piece):
	if x < 1 or 8 < x or y < 1 or 8 < y or piece not in [0,1,2]:
		return False
	board[y-1][x-1] = piece

def PrettyMove(move): 
	m = move["Where"]
	return '%s%d' % (chr(ord('A') + m[0] - 1), m[1])

def ABnegaMax(game, depth, alpha, beta):
	if depth == 0: 
		return game.evaluate(g.Next()), None
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
	
depth =3
g = Game(body)
score, move =  ABnegaMax(g, depth, -10000, 10000)
print score, PrettyMove(move)
