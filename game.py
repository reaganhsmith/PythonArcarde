"""
Platformer Game
"""
import arcade

# Constants
CHARACTER_SCALING = .3
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Pickle Game!!"
TILE_SCALING = 0.5
# movement per pixels 
PLAYER_MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.scene = None
        
        self.player_sprite = None
        
        self.physics_engine = None 

        arcade.set_background_color(arcade.color.JORDY_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        """Create a list to hold all the player info"""
        self.scene = arcade.Scene()
        
        
        # Create sprite lists 
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        
        # Set up the player 
        img = "images/pickle_cat.png"
        self.player_sprite = arcade.Sprite(img,  CHARACTER_SCALING)
        self.player_sprite.center_x = 40
        self.player_sprite.center_y = 105
        
        self.scene.add_sprite("Player", self.player_sprite)
        
        for x in range(0, 400, 64):
            wall = arcade.Sprite(":resources:images/tiles/sandMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 28
            self.scene.add_sprite("Walls", wall)
            
        for x in range(0, 300, 64):
            wall = arcade.Sprite("images/water.png", .21)
            wall.center_x = x + 400
            wall.center_y = 28
            self.scene.add_sprite("Walls", wall)
            
        for x in range(0, 400, 64):
            wall = arcade.Sprite(":resources:images/tiles/sandMid.png", TILE_SCALING)
            wall.center_x = x + 700
            wall.center_y = 28
            self.scene.add_sprite("Walls", wall)
    
        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        
        for coordinate in coordinate_list: 
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            
        # Create physics to move character
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
        
        
    # Function to draw the sceneray 
    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        
        self.scene.draw()  
        
    # Functions to pick up on key movement 
    def on_key_press(self, key, modifiers):
        
        """Called whenever a key is pressed. """    
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            
    def on_key_release(self, key, modifiers):
        
        """These are used if the user releases the keys"""
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
    def on_update(self, delta_time):
        """this causes movement with game logs"""
        self.physics_engine.update()

    
        


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()