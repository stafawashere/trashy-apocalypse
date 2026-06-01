class Screen:
    def __init__(self, width, height, title="Trashy Apocalypse"):
        self.title = title
        self.width = width
        self.height = height
        self.top = self.height
        self.bottom = -self.height
        self.center = (self.width/2, self.height/2)
        self.top_left = (-self.width/2, self.top)
        self.top_right = (self.width/2, self.top)
        self.bottom_left = (-self.width/2, self.bottom)
        self.bottom_right = (self.width/2, self.bottom)