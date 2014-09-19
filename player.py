class Player:
 
	def __init__(self, board, position):
 
		self.board 		= board
		self.position 	= position
 
		# Set low_limit, high_limit, fixed_limit, depending on position
		if position == "top":
			self.low_limit 		= self.board.TOP_BAND.x
			self.high_limit 	= self.board.TOP_BAND.x + self.board.BAND_LENGTH
			self.fixed_limit 	= self.board.TOP_BAND.y
 
		elif position == "bottom":
			self.low_limit 		= self.board.BOTTOM_BAND.x
			self.high_limit 	= self.board.BOTTOM_BAND.x + self.board.BAND_LENGTH
			self.fixed_limit 	= self.board.BOTTOM_BAND.y
 
		elif position == "left":
			self.low_limit 		= self.board.LEFT_BAND.y
			self.high_limit 	= self.board.LEFT_BAND.y + self.board.BAND_LENGTH
			self.fixed_limit 	= self.board.LEFT_BAND.x
 
		elif position == "right":
			self.low_limit 		= self.board.RIGHT_BAND.y
			self.high_limit 	= self.board.RIGHT_BAND.y + self.board.BAND_LENGTH
			self.fixed_limit 	= self.board.RIGHT_BAND.x
 
		self.score 		= 0
