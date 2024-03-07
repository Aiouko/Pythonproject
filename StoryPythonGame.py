# u need pygame for this to work but u can just do pip install pygame and then pip install openai 
# sys just in case we need to do system stuff (probably won't, but hey, it's here),
# json for saving our epic game progress, and openai to sprinkle some unreal stories in ur world.
import pygame
import sys
import json
import openai

# Plug in your GPT-3 or GPT-4 API key here.
openai.api_key = ""
# Our main hero, the Player. Think of it as their personal diary.
class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.progress = 0
        self.inventory = []  # Their backpack
        self.completed_challenges = []  # Their trophy shelf
        self.choices_history = []  # Their breadcrumb trail

    def add_to_inventory(self, item):
        # New loot? Into the backpack it goes.
        self.inventory.append(item)
        print(f"Sweet! {item} is now in your inventory.")

    def complete_challenge(self, challenge_id):
        # Achievement unlocked!
        self.completed_challenges.append(challenge_id)
        print(f"Awesome! Challenge {challenge_id} is in the bag.")

    def record_choice(self, choice):
        # Remembering the paths taken.
        self.choices_history.append(choice)

# Our story's building blocks. Each choice leads to a new adventure.
class StoryNode:
    def __init__(self, story_id, text, options=None, dynamic=False):
        self.story_id = story_id
        self.text = text
        self.options = options if options else {}
        self.dynamic = dynamic  # Where the story adapts and grows.

class Story:
    # The big picture, our story's universe.
    def __init__(self):
        self.nodes = {
            "start": StoryNode("start", "At a dark cave's entrance, do you dare to enter?", {"enter": "cave_entrance"}),
            "cave_entrance": StoryNode("cave_entrance", "Inside the cave, a path beckons. Go deeper or head back?", {"continue": "deep_cave", "leave": "exit"}),
        }

    def get_node(self, node_id):
        # Finding where you are in the story.
        return self.nodes.get(node_id, None)

# The heart of the operation, our Game Engine.
class GameEngine:
    def __init__(self, player, story):
        self.player = player
        self.story = story
        self.current_node = "start"  # Every adventure starts somewhere.

    def load_dynamic_content(self, node):
        # The story evolves with your decisions. hopefully good or bad 
        if node.dynamic:
            context = f"As {self.player.name}, a level {self.player.level} adventurer, you're at a {self.current_node}."
            prompt = f"{context} What happens next?"
            dynamic_text = self.generate_ai_content(prompt)
            node.text = dynamic_text

    def generate_ai_content(self, prompt):
        # Consulting the AI for your storyline.^^
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Oops, hit a snag: {e}")
            return "An unexpected twist unfolds..."

# The grand kickoff!
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Solo Coding")

    font = pygame.font.Font(None, 36)

    # Setting up for text input
    input_active = True
    input_text = ''
    welcome_message = ''

    player = None
    story = Story()
    game_engine = None

    # Keeping time with our game clock.
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))  # The anticipation builds on a black screen.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif input_active:
                    if event.key == pygame.K_RETURN:
                        player_name = input_text
                        player = Player(player_name)
                        game_engine = GameEngine(player, story)
                        welcome_message = f"Welcome, {player_name}! Ready to embark on your solo adventure? Press any key to dive in..."
                        input_text = ''  
                        input_active = False  # And we goooooo :D
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Displaying text input
        if input_active:
            input_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(input_surface, (400 - input_surface.get_width() / 2, 300))

        # And the welcome message
        if welcome_message:
            welcome_surface = font.render(welcome_message, True, (255, 255, 255))
            screen.blit(welcome_surface, (400 - welcome_surface.get_width() / 2, 350))

        pygame.display.flip()  # i suck at drawing :c but i try
        clock.tick(60)  # 60fps if u want or 30 :)

    pygame.quit()

# Like bookmarks in our digital tale.
def save_game(player):
    try:
        with open('player_data.json', 'w') as f:
            json.dump(player.__dict__, f, indent=4)
        print("Adventure saved. Sleep tight!")
    except Exception as e:
        print(f"Oops, couldn't tuck your adventure in: {e}")

def load_game():
    try:
        with open('player_data.json', 'r') as f:
            data = json.load(f)
        player = Player(data['name'])
        player.__dict__.update(data)
        print("Back to the adventure. Let's roll!")
        return player
    except Exception as e:
        print(f"Ouch, couldn't wake your adventure up: {e}")
        return None

if __name__ == "__main__":
    main()
