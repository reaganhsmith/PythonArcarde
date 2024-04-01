"""
Platformer Game
"""
import arcade

# Constants
CHARACTER_SCALING = 0.7
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Fun Game!!"
TILE_SCALING = 0.5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.player_list = None
        self.wall_list = None
        
        self.player_sprite = None

        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        """Create a list to hold all the player info"""
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        
        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img,  CHARACTER_SCALING)
        self.player_sprite.center_x = 40
        self.player_sprite.center_y = 105
        
        self.player_list.append(self.player_sprite)
        
        for x in range(0, 400, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 28
            self.wall_list.append(wall)
            
        for x in range(0, 300, 65):
            wall = arcade.Sprite(":resources:images/tiles/water.png", TILE_SCALING)
            wall.center_x = x + 400
            wall.center_y = 28
            self.wall_list.append(wall)
            
        for x in range(0, 400, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x + 700
            wall.center_y = 28
            self.wall_list.append(wall)
    
        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        
        for coordinate in coordinate_list: 
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)
        

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        
        self.wall_list.draw()
        self.player_list.draw()
        


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()