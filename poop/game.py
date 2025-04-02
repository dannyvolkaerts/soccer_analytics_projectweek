import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from mplsoccer import Pitch
import matplotlib.backends.backend_agg as agg
from queries import load_data
from functions import interpolate_ball_data, prepare_player_data, get_interpolated_positions

# Load data
df_ball, df_home, df_away = load_data()

# Interpolate data
frames_between = 12
df_ball_interp = interpolate_ball_data(df_ball, frames_between)
home_frames, home_positions = prepare_player_data(df_home, "home")
away_frames, away_positions = prepare_player_data(df_away, "away")

# Initialize Pygame
pygame.init()
window_width, window_height = 1920, 1080
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Soccer Match Animation")

# Create the matplotlib figure
pitch = Pitch(pitch_type='metricasports', goal_type='line', pitch_width=68, pitch_length=105)
fig, ax = pitch.draw(figsize=(16, 10.4))
marker_kwargs = {'marker': 'o', 'markeredgecolor': 'black', 'linestyle': 'None'}
ball, = ax.plot([], [], ms=6, markerfacecolor='w', zorder=3, **marker_kwargs)
away, = ax.plot([], [], ms=10, markerfacecolor='#b94b75', **marker_kwargs)
home, = ax.plot([], [], ms=10, markerfacecolor='#7f63b8', **marker_kwargs)

# Animation function
def animate(i):
    ball_x = df_ball_interp.iloc[i]['x'] / 100
    ball_y = df_ball_interp.iloc[i]['y'] / 100
    ball.set_data([ball_x], [ball_y])

    frame = df_ball_interp.iloc[i]['frame_id']
    home_pos = get_interpolated_positions(frame, home_frames, home_positions)
    away_pos = get_interpolated_positions(frame, away_frames, away_positions)

    home_x = [pos[0] / 100 for pos in home_pos.values()]
    home_y = [pos[1] / 100 for pos in home_pos.values()]
    away_x = [pos[0] / 100 for pos in away_pos.values()]
    away_y = [pos[1] / 100 for pos in away_pos.values()]

    home.set_data(home_x, home_y)
    away.set_data(away_x, away_y)

# Draw frame
def draw_frame(frame_idx):
    animate(frame_idx)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    canvas_width, canvas_height = canvas.get_width_height()
    return pygame.image.fromstring(raw_data, (canvas_width, canvas_height), "RGB")

# Main game loop
def main():
    clock = pygame.time.Clock()
    fps = 24
    frame_delay = 1000 // fps
    current_frame = 0
    total_frames = len(df_ball_interp)
    playing = False  # Start in a paused state

    # Button dimensions
    button_width = 100
    button_height = 40
    button_margin = 10
    controls_y = window_height - button_height - button_margin

    # Define buttons
    start_button = pygame.Rect(button_margin, controls_y, button_width, button_height)
    stop_button = pygame.Rect(button_margin + 110, controls_y, button_width, button_height)
    restart_button = pygame.Rect(button_margin + 220, controls_y, button_width, button_height)

    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    playing = True
                elif stop_button.collidepoint(event.pos):
                    playing = False
                elif restart_button.collidepoint(event.pos):
                    current_frame = 0
                    playing = False

        # Update frame if playing
        if playing:
            current_frame = (current_frame + 1) % total_frames

        # Draw the current frame
        frame_surface = draw_frame(current_frame)
        screen.blit(frame_surface, (0, 0))

        # Draw buttons
        pygame.draw.rect(screen, (0, 200, 0), start_button)  # Green for Start
        pygame.draw.rect(screen, (200, 0, 0), stop_button)   # Red for Stop
        pygame.draw.rect(screen, (0, 0, 200), restart_button)  # Blue for Restart

        # Add button labels
        start_text = font.render("Start", True, (255, 255, 255))
        stop_text = font.render("Stop", True, (255, 255, 255))
        restart_text = font.render("Restart", True, (255, 255, 255))

        screen.blit(start_text, (start_button.x + 20, start_button.y + 5))
        screen.blit(stop_text, (stop_button.x + 20, stop_button.y + 5))
        screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 5))

        # Update the display
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()