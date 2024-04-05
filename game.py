
"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Fruit Game!!"

CHARACTER_SCALING = .3
TILE_SCALING = 1.2
COIN_SCALING = .2
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# movement per pixels 
PLAYER_MOVEMENT_SPEED = 5
# Adding gravity
GRAVITY = 1
PLAYER_JUMP_SPEED = 20



# Starting coordinates of player
PLAYER_START_X = 64
PLAYER_START_Y = 225

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"

LAYER_NAME_COINS = "Coins"

LAYER_NAME_FOREGROUND = "Foreground"

LAYER_NAME_BACKGROUND = "Background"

LAYER_NAME_DONT_TOUCH = "Don't Touch"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.title_map = None
        
        self.scene = None
        
        self.player_sprite = None
        
        self.physics_engine = None 
        
        self.camera = None
        
        self.gui_camera = None
        
        self.score = 0

        self.reset_score = True

        self.end_of_map = 0
        
        self.level = 1
        
        self.level_completed = False  
        
        # Sounds for different actions
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.win_game = arcade.load_sound(":resources:sounds/upgrade1.wav")

    

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Map name
        map_name = "Game2.json"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        if self.reset_score:
            self.score = 0
        self.reset_score = True
        
        
        # Create sprite lists 
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        
        player_img = "images/pickle_cat.png"
        self.player_sprite = arcade.Sprite(player_img, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)
        
        # LOAD MAP FROM TILED
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        
    
        arcade.set_background_color(arcade.color.FLORAL_WHITE)
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant = GRAVITY,
            walls = self.scene[LAYER_NAME_PLATFORMS]
        )
           
        
    def on_draw(self):

        self.clear()
        
        self.camera.use()
        
        self.scene.draw()
        
        self.gui_camera.use()
    
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )
        
        
        if self.level_completed:  
            arcade.draw_text(
                f"Level Completed! Your score was: {self.score} points",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.csscolor.PINK,
                font_size=24,
                anchor_x="center",
                anchor_y="center"
            )
        
    # Functions to pick up on key movement 
    def on_key_press(self, key, modifiers):
        
        """Called whenever a key is pressed. """    
        
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            
             # Reset level completed flag if any key is pressed
        self.level_completed = False
            
    def on_key_release(self, key, modifiers):
        
        """These are used if the user releases the keys"""
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            
            
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
            
            
    def on_update(self, delta_time):
        """this causes movement with game logs"""
        self.physics_engine.update()
        
        
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 10

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)

         # Check if the player reaches the end of the level
        if self.player_sprite.center_x >= 1900:
            self.level_completed = True  # Set level completed flag
            arcade.play_sound(self.win_game)

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()
        # Position the camera
        self.center_camera_to_player()
    
        


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
    
