import pygame
import random
import sys
from enum import Enum
import time

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GRID_SIZE = 12
ROOM_SIZE = 64
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)

# Directions
DIRECTIONS = {
    'north': (0, -1),
    'south': (0, 1),
    'east': (1, 0),
    'west': (-1, 0)
}
REVERSE_DIRECTIONS = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}

class GameState(Enum):
    PLAYING = 0
    PAUSED = 1
    GAME_OVER = 2
    VICTORY = 3

class DialogueManager:
    def __init__(self):
        self.conversations = {}

    def add_conversation(self, spirit, conversation):
        self.conversations[spirit] = conversation

class AudioManager:
    def __init__(self):
        self.ambient_sounds = {
            'normal': pygame.mixer.Sound('ambient_normal.wav'),
            'low_sanity': pygame.mixer.Sound('ambient_low_sanity.wav'),
            'entity_near': pygame.mixer.Sound('entity_near.wav')
        }
        self.event_sounds = {
            'door_shift': pygame.mixer.Sound('door_shift.wav'),
            'item_pickup': pygame.mixer.Sound('item_pickup.wav'),
            'entity_spawn': pygame.mixer.Sound('entity_spawn.wav'),
            'flashlight_toggle': pygame.mixer.Sound('flashlight_toggle.wav')
        }
        self.current_ambient = self.ambient_sounds['normal']
        self.current_ambient.play(-1)

    def update_ambient(self, player_sanity, entities_near):
        if player_sanity < SANITY_THRESHOLD_LOW or entities_near:
            if self.current_ambient != self.ambient_sounds['entity_near']:
                self.current_ambient.stop()
                self.current_ambient = self.ambient_sounds['entity_near']
                self.current_ambient.play(-1)
        elif player_sanity < SANITY_THRESHOLD_MED:
            if self.current_ambient != self.ambient_sounds['low_sanity']:
                self.current_ambient.stop()
                self.current_ambient = self.ambient_sounds['low_sanity']
                self.current_ambient.play(-1)
        else:
            if self.current_ambient != self.ambient_sounds['normal']:
                self.current_ambient.stop()
                self.current_ambient = self.ambient_sounds['normal']
                self.current_ambient.play(-1)

    def play_event(self, event_name):
        self.event_sounds[event_name].play()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Echoes of the Forgotten")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.state = GameState.PLAYING
        self.player = Player()
        self.house = House(GRID_SIZE)
        self.story = StoryManager(self.house, self.player)
        self.audio = AudioManager()
        self.message = ""
        self.message_timer = 0
        self.distortion_alpha = 0
        self.entities_near = False
        self.minimap_surface = pygame.Surface((200, 200), pygame.SRCALPHA)

    def run(self):
        while self.state != GameState.GAME_OVER and self.state != GameState.VICTORY:
            self.handle_events()
            if self.state == GameState.PLAYING:
                self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.GAME_OVER
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.PLAYING:
                if self.state == GameState.PLAYING:
                if self.state == GameState.PLAYING:
                if self.state == GameState.PLAYING:
                if self.state == GameState.PLAYING:

                if event.key == pygame.K_p:
                    self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING

    def update(self):
        self.player.update()
        self.house.update()
        self.story.update()
        
        elif self.story.all_spirits_helped():
            self.message = "All spirits are at peace. The house releases its grip. You escape."
            self.state = GameState.VICTORY

        if self.message:
            self.message_timer += 1
            if self.message_timer > 180:
                self.message = ""
                self.message_timer = 0

        self.distortion_alpha = max(0, 255 - int(self.player.sanity * 2.55))
        if self.player.sanity < SANITY_THRESHOLD_LOW:
            self.distortion_alpha = min(255, self.distortion_alpha + random.randint(-20, 20))

    def draw(self):
        self.screen.fill(BLACK)
        current_room = self.house.get_room(self.player.x, self.player.y)

        # Draw room
        room_surface = pygame.Surface((SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100), pygame.SRCALPHA)
        room_surface.fill((20, 20, 20))
        pygame.draw.rect(room_surface, GRAY, (50, 50, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 200), 5)

        # Draw doors with dynamic lighting
        for dir_name, open_door in current_room.doors.items():
            if open_door:
                dx, dy = DIRECTIONS[dir_name]
                door_x = (SCREEN_WIDTH - 300) // 2 + dx * 150
                door_y = (SCREEN_HEIGHT - 100) // 2 + dy * 150
                door_color = YELLOW if self.player.flashlight_on else GRAY
                pygame.draw.rect(room_surface, door_color, (door_x - 25, door_y - 25, 50, 50))

        # Draw items
        for item in current_room.items:
            item_x = random.randint(100, SCREEN_WIDTH - 400)
            item_y = random.randint(100, SCREEN_HEIGHT - 200)
            pygame.draw.circle(room_surface, BLUE, (item_x, item_y), 10)

        # Draw entities
        for entity in current_room.entities:
            entity_x = random.randint(100, SCREEN_WIDTH - 400)
            entity_y = random.randint(100, SCREEN_HEIGHT - 200)
            pygame.draw.circle(room_surface, RED, (entity_x, entity_y), 15)
            if self.player.flashlight_on:
                pygame.draw.circle(room_surface, (255, 255, 255, 100), (entity_x, entity_y), 20, 2)

        self.screen.blit(room_surface, (50, 50))

        # Draw minimap
        self.minimap_surface.fill((0, 0, 0, 0))
        for x in range(max(0, self.player.x - 2), min(GRID_SIZE, self.player.x + 3)):
            for y in range(max(0, self.player.y - 2), min(GRID_SIZE, self.player.y + 3)):
                room = self.house.get_room(x, y)
                map_x = (x - (self.player.x - 2)) * 40 + 10
                map_y = (y - (self.player.y - 2)) * 40 + 10
                color = GRAY if self.house.stabilized_regions[room.region] else DARK_GRAY
                pygame.draw.rect(self.minimap_surface, color, (map_x, map_y, 35, 35))
                for dir_name, open_door in room.doors.items():
                    if open_door:
                        dx, dy = DIRECTIONS[dir_name]
                        door_x = map_x + 17 + dx * 17
                        door_y = map_y + 17 + dy * 17
                        pygame.draw.rect(self.minimap_surface, WHITE, (door_x - 5, door_y - 5, 10, 10))
        pygame.draw.rect(self.minimap_surface, RED, (90, 90, 35, 35), 2)
        self.screen.blit(self.minimap_surface, (SCREEN_WIDTH - 250, 50))

        # Draw HUD
        sanity_text = self.font.render(f"Sanity: {int(self.player.sanity)}", True, WHITE)
        self.screen.blit(sanity_text, (50, SCREEN_HEIGHT - 80))
        battery_text = self.font.render(f"Battery: {int(self.player.flashlight_battery)}%", True, WHITE)
        self.screen.blit(battery_text, (250, SCREEN_HEIGHT - 80))
        inventory_text = self.small_font.render("Inventory: " + ", ".join([item.name for item in self.player.inventory]), True, WHITE)
        self.screen.blit(inventory_text, (50, SCREEN_HEIGHT - 50))

        # Draw distortion effects
        if self.player.sanity < SANITY_THRESHOLD_MED:
            distortion_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            distortion_surface.fill((100, 0, 0, self.distortion_alpha))
            self.screen.blit(distortion_surface, (0, 0))

        # Draw messages and state
        if self.message:
            msg_surface = pygame.Surface((SCREEN_WIDTH - 100, 100), pygame.SRCALPHA)
            msg_surface.fill((0, 0, 0, 200))
            msg_render = self.font.render(self.message, True, DARK_RED)
            msg_surface.blit(msg_render, (10, 10))
            self.screen.blit(msg_surface, (50, SCREEN_HEIGHT // 2 - 50))
        if self.state == GameState.PAUSED:
            pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 150))
            pause_text = self.font.render("PAUSED - Press P to resume", True, WHITE)
            pause_surface.blit(pause_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_surface, (0, 0))

        pygame.display.flip()

class Player:
    def __init__(self):
        self.x = random.randint(0, GRID_SIZE - 1)
        self.y = random.randint(0, GRID_SIZE - 1)
        self.sanity = 100
        self.inventory = []
        self.hiding = False
        self.flashlight_on = False
        self.flashlight_battery = FLASHLIGHT_BATTERY_MAX
        self.last_battery_recharge = time.time()

    def move(self, direction):
        if self.hiding:
            game.message = "You cannot move while hiding."
            return
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = self.x + dx, self.y + dy
        current_room = game.house.get_room(self.x, self.y)
        if current_room.doors[direction]:
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                self.x, self.y = new_x, new_y
                game.message = f"You move {direction} into {game.house.get_room(self.x, self.y).description}."
                if game.house.get_room(self.x, self.y).entities and not self.flashlight_on:
                    game.message += " A shadow watches you!"
            else:
                game.message = "An unseen force blocks your path."
        else:
            game.message = "The passage is sealed."

    def interact(self):
        current_room = game.house.get_room(self.x, self.y)
        if self.hiding:
            self.hiding = False
            game.message = "You emerge from hiding."
            return
        if current_room.items:
            item = current_room.items.pop(0)
            self.inventory.append(item)
            game.message = f"You picked up {item.name}."
            game.audio.play_event('item_pickup')
        elif current_room.entities and not self.hiding:
            self.hiding = True
            game.message = "You hide in the shadows, holding your breath."
        elif not current_room.items and not current_room.entities:
            game.message = "There's nothing to interact with here."

    def toggle_flashlight(self):
        if self.hiding:
            game.message = "You cannot use the flashlight while hiding."
            return
        if self.flashlight_battery <= 0:
            game.message = "Your flashlight battery is drained."
            return
        self.flashlight_on = not self.flashlight_on
        game.message = f"Flashlight {'on' if self.flashlight_on else 'off'}."
        game.audio.play_event('flashlight_toggle')

    def toggle_hiding(self):
        if not self.hiding and game.house.get_room(self.x, self.y).entities:
            self.hiding = True
            game.message = "You hide from the lurking shadow."
        elif self.hiding:
            self.hiding = False
            game.message = "You stop hiding."

    def update(self):
        if not self.hiding:
            self.sanity -= SANITY_DRAIN_RATE
            current_room = game.house.get_room(self.x, self.y)
            if current_room.entities:
                if self.flashlight_on:
                    current_room.entities = []
                    game.message = "The flashlight repels the shadow!"
                else:
                    self.sanity -= 1.5
            if self.flashlight_on:
                self.flashlight_battery -= FLASHLIGHT_DRAIN_RATE
                if self.flashlight_battery <= 0:
                    self.flashlight_on = False
                    game.message = "Your flashlight battery has died."
        else:
            self.sanity -= 0.8

        if time.time() - self.last_battery_recharge > 1:
            self.flashlight_battery = min(FLASHLIGHT_BATTERY_MAX, self.flashlight_battery + FLASHLIGHT_RECHARGE_RATE)
            self.last_battery_recharge = time.time()

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.doors = {'north': False, 'south': False, 'east': False, 'west': False}
        self.items = []
        self.entities = []
        self.description = self.generate_description()
        self.region = self.assign_region()
        self.clue = None

    def generate_description(self):
        descriptions = [
            "A forsaken bedroom, its furniture draped in shadows.",
            "A narrow hallway, echoing with distant whispers.",
            "A desolate study, books scattered like forgotten memories.",
            "A dining room, where the table is set for no one.",
            "A shadowy attic, filled with cobwebs and secrets.",
            "A cold basement, the air thick with dampness."
        ]
        return random.choice(descriptions)

    def assign_region(self):
        if self.x < GRID_SIZE // 3 and self.y < GRID_SIZE // 2:
            return 0
        elif self.x >= GRID_SIZE // 3 and self.x < 2 * GRID_SIZE // 3 and self.y < GRID_SIZE // 2:
            return 1
        elif self.x >= 2 * GRID_SIZE // 3 and self.y < GRID_SIZE // 2:
            return 2
        elif self.x < GRID_SIZE // 2 and self.y >= GRID_SIZE // 2:
            return 3
        else:
            return 4

class House:
    def __init__(self, size):
        self.size = size
        self.grid = [[Room(x, y) for y in range(size)] for x in range(size)]
        self.spanning_tree = self.generate_spanning_tree()
        self.set_doors()
        self.stabilized_regions = [False] * 5
        self.last_shift = time.time()

    def generate_spanning_tree(self):
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]
        spanning_tree = set()
        start_x, start_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.dfs(start_x, start_y, visited, spanning_tree)
        return spanning_tree

    def dfs(self, x, y, visited, spanning_tree):
        visited[x][y] = True
        directions = list(DIRECTIONS.items())
        random.shuffle(directions)
        for dir_name, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and not visited[nx][ny]:
                spanning_tree.add(((x, y), (nx, ny)))
                spanning_tree.add(((nx, ny), (x, y)))
                self.dfs(nx, ny, visited, spanning_tree)

    def set_doors(self):
        for x in range(self.size):
            for y in range(self.size):
                room = self.grid[x][y]
                for dir_name, (dx, dy) in DIRECTIONS.items():
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        edge = ((x, y), (nx, ny))
                        if edge in self.spanning_tree:
                            room.doors[dir_name] = True
                            self.grid[nx][ny].doors[REVERSE_DIRECTIONS[dir_name]] = True
                        elif random.random() < 0.25:
                            room.doors[dir_name] = True
                            self.grid[nx][ny].doors[REVERSE_DIRECTIONS[dir_name]] = True

    def update(self):
        if time.time() - self.last_shift > 5:
            for x in range(self.size):
                for y in range(self.size):
                    room = self.grid[x][y]
                    if not self.stabilized_regions[room.region]:
                        for dir_name, (dx, dy) in DIRECTIONS.items():
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.size and 0 <= ny < self.size:
                                edge = ((x, y), (nx, ny))
                                if edge not in self.spanning_tree:
                                    open_door = random.random() < 0.2
                                    room.doors[dir_name] = open_door
                                    self.grid[nx][ny].doors[REVERSE_DIRECTIONS[dir_name]] = open_door
            game.audio.play_event('door_shift')
            self.last_shift = time.time()

        for x in range(self.size):
            for y in range(self.size):
                room = self.grid[x][y]
                if not self.stabilized_regions[room.region] and random.random() < ENTITY_SPAWN_CHANCE:
                    if not room.entities and (abs(x - game.player.x) > 1 or abs(y - game.player.y) > 1):
                        room.entities.append("Shadow")
                        game.audio.play_event('entity_spawn')

    def get_room(self, x, y):
        return self.grid[x][y]

class Item:
    def __init__(self, name, clue_text):
        self.name = name
        self.clue_text = clue_text

class StoryManager:
    def __init__(self, house, player):
        self.house = house
        self.player = player
        self.spirits_helped = [False] * 5
        self.story_items = [
            Item("Broken Mirror", "Reflections show more than reality. Find where I shattered my image."),
            Item("Faded Photograph", "A family torn apart. Seek the room where memories burned."),
            Item("Locked Diary", "Secrets locked away. The key lies in the shadow of betrayal."),
            Item("Torn Letter", "Words unsent, promises broken. Mend me in the place of silence."),
            Item("Ancient Pendant", "A bond eternal, now cursed. Return me to the heart of despair.")
        ]
        self.clues = [
            "The mirror broke in the attic, where the eldest took her life.",
            "The fire consumed the study, destroying the family's legacy.",
            "The diary's key is hidden in the basement, where trust was broken.",
            "The letter was torn in the silent dining room, where arguments echoed.",
            "The pendant was lost in the master bedroom, where love turned to hate."
        ]
        self.spirit_locations = [None] * 5
        self.place_items_and_spirits()

    def place_items_and_spirits(self):
        for i, item in enumerate(self.story_items):
            region = i
            rooms = [room for row in self.house.grid for room in row if room.region == region]
            item_room = random.choice(rooms)
            item_room.items.append(item)
            spirit_room = random.choice([r for r in rooms if r != item_room])
            spirit_room.clue = self.clues[i]
            self.spirit_locations[i] = (spirit_room.x, spirit_room.y)

    def update(self):
        for i in range(5):
            if not self.spirits_helped[i]:
                spirit_x, spirit_y = self.spirit_locations[i]
                spirit_room = self.house.get_room(spirit_x, spirit_y)
                if self.player.x == spirit_x and self.player.y == spirit_y:
                    if self.story_items[i].name in [item.name for item in self.player.inventory]:
                        self.spirits_helped[i] = True
                        self.house.stabilized_regions[i] = True
                        self.player.inventory = [item for item in self.player.inventory if item.name != self.story_items[i].name]
                        game.message = f"You've resolved the spirit's unrest in region {i}. The area stabilizes."
                        game.audio.play_event('item_pickup')
                elif spirit_room.clue and not self.player.hiding:
                    game.message = spirit_room.clue

    def all_spirits_helped(self):
        return all(self.spirits_helped)

if __name__ == "__main__":
    game = Game()
    game.run()