class Grid:

    def __init__(self, scale, width, height):
        self.scale = scale
        self.width_scale = width // self.scale
        self.height_scale = height // self.scale
        self.matrix = [[1 for _ in range(self.scale)] for _ in range(self.scale)]

    @property
    def grid(self):
        return self.matrix

    def translate_screen_position(self, x: int, y: int) -> tuple:
        return (x // self.width_scale, y // self.height_scale)

    def rectangle_cords(self, x: int, y: int, width: int, height: int) -> tuple:
        rect_x = x * self.width_scale
        rect_y = y * self.height_scale

        return ((rect_x, rect_y), (self.width_scale, self.height_scale))