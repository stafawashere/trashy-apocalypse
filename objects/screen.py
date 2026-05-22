class Screen():
    def __init__(self, width, height, title="DeepClean"):
        self.title = title
        self.width = width
        self.height = height
        self.top = self.height/2
        self.bottom = -self.height/2
        self.center = (self.bottom/2, self.top/2)
        self.top_left = (-self.width/2, self.top)
        self.top_right = (self.width/2, self.top)
        self.bottom_left = (-self.width/2, self.bottom)
        self.bottom_right = (self.width/2, self.bottom)