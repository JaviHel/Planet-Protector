class Font:
    """ Creates a font from an image """
    char_ord = ["0","1","2","3","4","5","6","7","8","9"]
    def __init__(self, pg, img_path, fg_color=None, bg_color="black" , character_order=char_ord):
        self.pg = pg
        self.img = pg.image.load(img_path).convert()
        self.character_order = character_order
        self.characters = {}

        self.sprite_width = self.img.get_rect().width//len(character_order)
        self.sprite_height = self.img.get_rect().height
        
        self.spacing_x = 1
        self.spacing_y = 1

        if fg_color != None: self.change_color(self.img, fg_color, bg_color)
        self.map_chars()
        

    def map_chars(self):
        for x in range(len(self.character_order)):
            cropped_character = self.crop_frame(self.img, x, 0, self.sprite_width, self.sprite_height)
            self.characters[self.character_order[x]] = cropped_character

    def render(self, surf, text, pos):
        x_offset, y_offset = 0, 0
        for char in text:
            if char != ' ' and char != '.':
                surf.blit(self.characters[char], (pos[0]+x_offset, pos[1]+y_offset))
                x_offset += self.characters[char].get_width() + self.spacing_x
            elif char == '.':
                x_offset = -self.sprite_width - self.spacing_x
                y_offset += self.sprite_height + self.spacing_y
            else:
                x_offset += self.sprite_width + self.spacing_x

        
    @staticmethod
    def crop_frame(surf, x, y, w, h):
        handle_surf = surf.copy()
        handle_surf.set_clip(x*w, y*h, w, h)
        surf_img = handle_surf.subsurface(handle_surf.get_clip())
        return surf_img


    @staticmethod
    def change_color(surf, fg_color="white", bg_color="black",rgb=[250, 250, 250, 250]):
        """ Changes the color of the pixels based on its color """       
        for x in range(surf.get_width()):
            for y in range(surf.get_height()):
                if (surf.get_at((x, y))[0] >= rgb[0] and
                    surf.get_at((x, y))[1] >= rgb[1] and
                    surf.get_at((x, y))[2] >= rgb[2] and
                    surf.get_at((x, y))[1] >= rgb[3]):
                    surf.set_at((x, y), fg_color)
                else:
                    surf.set_at((x, y), bg_color)
        return surf
