import numpy as np
import pandas as pd
import psycopg2
import dotenv
import os
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from mplsoccer import Pitch
import time

dotenv.load_dotenv()

PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_USER = os.getenv("PG_USER")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DB")

# Database connection parameters
import psycopg2
import os

conn = psycopg2.connect(
    host=PG_HOST,
    database=PG_DATABASE,
    user=PG_USER,
    password=PG_PASSWORD,
    port=PG_PORT,
    sslmode="require",
)

ballquery="""
SELECT pt.period_id, pt.frame_id, pt.timestamp, pt.x, pt.y, pt.player_id, p.team_id
FROM player_tracking pt
JOIN players p ON pt.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id
WHERE pt.game_id = '5uts2s7fl98clqz8uymaazehg' AND p.player_id = 'ball' AND pt.period_id = 1
ORDER BY timestamp;
"""
# Differentiating teams logic
team_query = """
SELECT DISTINCT p.team_id
FROM player_tracking pt
JOIN players p ON pt.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id AND p.player_id != 'ball'
WHERE pt.game_id = '5uts2s7fl98clqz8uymaazehg';
"""
team_ids_df = pd.read_sql_query(team_query, conn)  # Fetch the query result as a DataFrame
# Extract the team IDs as a list
team_ids = team_ids_df['team_id'].tolist()




teamqueries = """
SELECT pt.frame_id, pt.timestamp, pt.player_id, pt.x, pt.y, p.team_id
FROM player_tracking pt
JOIN players p ON pt.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id
WHERE pt.game_id = '5uts2s7fl98clqz8uymaazehg' AND p.player_id != 'ball' AND p.team_id = %s
ORDER BY timestamp;
"""



df_ball = pd.read_sql_query(ballquery,conn)
df_home = pd.read_sql_query(teamqueries, conn, params=(team_ids[0],))
df_away = pd.read_sql_query(teamqueries, conn, params=(team_ids[1],))

# First set up the figure, the axis
pitch = Pitch(pitch_type='metricasports', goal_type='line', pitch_width=68, pitch_length=105)
fig, ax = pitch.draw(figsize=(16, 10.4))

# then setup the pitch plot markers we want to animate
marker_kwargs = {'marker': 'o', 'markeredgecolor': 'black', 'linestyle': 'None'}
ball, = ax.plot([], [], ms=6, markerfacecolor='w', zorder=3, **marker_kwargs)
away, = ax.plot([], [], ms=10, markerfacecolor='#b94b75', **marker_kwargs)  # red/maroon
home, = ax.plot([], [], ms=10, markerfacecolor='#7f63b8', **marker_kwargs)  # purple

our_number = 1722798900000
# animation function
import numpy as np
import time

import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Global counter to track interpolation steps
frame_counter = 0

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import interp1d
import time

# Assuming `fig`, `ax`, and `ball`, `away`, `home` are already defined
# Example data structure placeholders:
# Assuming the database connection and ballquery are already defined
df_ball = pd.read_sql_query(ballquery, conn)

# Similarly, ensure df_away and df_home are also properly assigned
df_home = pd.read_sql_query(teamqueries, conn, params=(team_ids[0],))
df_away = pd.read_sql_query(teamqueries, conn, params=(team_ids[1],))

def update(i):
    """Updates ball/player positions with interpolation for 2 frames per second."""
    global ball, away, home
    
    # Determine if this is an interpolated frame (odd indices are interpolated)
    is_interpolated = i % 2 == 1
    
    if is_interpolated:
        # For interpolated frames, calculate position between real data points
        data_idx = i // 2
        
        # Get the frame id for the current and next frame
        frame = df_ball.loc[data_idx, 'frame_id']
        frame_next = df_ball.loc[data_idx + 1, 'frame_id'] if data_idx + 1 < len(df_ball) else frame

        # Extract ball positions for current and next frame
        ball_x_start = df_ball.loc[data_idx, 'x'] / 100
        ball_y_start = df_ball.loc[data_idx, 'y'] / 100
        
        ball_x_end = df_ball.loc[data_idx + 1, 'x'] / 100 if data_idx + 1 < len(df_ball) else ball_x_start
        ball_y_end = df_ball.loc[data_idx + 1, 'y'] / 100 if data_idx + 1 < len(df_ball) else ball_y_start
        
        # Linear interpolation (0.5 = halfway between frames)
        ball_x = ball_x_start + 0.5 * (ball_x_end - ball_x_start)
        ball_y = ball_y_start + 0.5 * (ball_y_end - ball_y_start)
        
        # Set the ball position to interpolated position
        ball.set_data([ball_x], [ball_y])
        
        # For player interpolation, we'll need player positions from both frames
        # First, get positions for current frame
        away_players_x1 = df_away.loc[df_away.frame_id == frame, 'x'] / 100
        away_players_y1 = df_away.loc[df_away.frame_id == frame, 'y'] / 100
        home_players_x1 = df_home.loc[df_home.frame_id == frame, 'x'] / 100
        home_players_y1 = df_home.loc[df_home.frame_id == frame, 'y'] / 100
        
        # Get positions for next frame
        away_players_x2 = df_away.loc[df_away.frame_id == frame_next, 'x'] / 100
        away_players_y2 = df_away.loc[df_away.frame_id == frame_next, 'y'] / 100
        home_players_x2 = df_home.loc[df_home.frame_id == frame_next, 'x'] / 100
        home_players_y2 = df_home.loc[df_home.frame_id == frame_next, 'y'] / 100
        
        # Interpolate player positions - make sure players in both frames match
        # Get player IDs from both frames
        away_ids_frame1 = df_away.loc[df_away.frame_id == frame, 'player_id'].reset_index(drop=True)
        away_ids_frame2 = df_away.loc[df_away.frame_id == frame_next, 'player_id'].reset_index(drop=True)
        
        home_ids_frame1 = df_home.loc[df_home.frame_id == frame, 'player_id'].reset_index(drop=True)
        home_ids_frame2 = df_home.loc[df_home.frame_id == frame_next, 'player_id'].reset_index(drop=True)
        
        # Initialize interpolated position arrays
        away_interp_x = []
        away_interp_y = []
        home_interp_x = []
        home_interp_y = []
        
        # Interpolate away players that appear in both frames
        common_away_players = set(away_ids_frame1).intersection(set(away_ids_frame2))
        
        for pid in common_away_players:
            # Get positions in current frame
            pos1_x = df_away.loc[(df_away.frame_id == frame) & (df_away.player_id == pid), 'x'].values[0] / 100
            pos1_y = df_away.loc[(df_away.frame_id == frame) & (df_away.player_id == pid), 'y'].values[0] / 100
            
            # Get positions in next frame
            pos2_x = df_away.loc[(df_away.frame_id == frame_next) & (df_away.player_id == pid), 'x'].values[0] / 100
            pos2_y = df_away.loc[(df_away.frame_id == frame_next) & (df_away.player_id == pid), 'y'].values[0] / 100
            
            # Interpolate
            interp_x = pos1_x + 0.5 * (pos2_x - pos1_x)
            interp_y = pos1_y + 0.5 * (pos2_y - pos1_y)
            
            away_interp_x.append(interp_x)
            away_interp_y.append(interp_y)
        
        # Interpolate home players that appear in both frames
        common_home_players = set(home_ids_frame1).intersection(set(home_ids_frame2))
        
        for pid in common_home_players:
            # Get positions in current frame
            pos1_x = df_home.loc[(df_home.frame_id == frame) & (df_home.player_id == pid), 'x'].values[0] / 100
            pos1_y = df_home.loc[(df_home.frame_id == frame) & (df_home.player_id == pid), 'y'].values[0] / 100
            
            # Get positions in next frame
            pos2_x = df_home.loc[(df_home.frame_id == frame_next) & (df_home.player_id == pid), 'x'].values[0] / 100
            pos2_y = df_home.loc[(df_home.frame_id == frame_next) & (df_home.player_id == pid), 'y'].values[0] / 100
            
            # Interpolate
            interp_x = pos1_x + 0.5 * (pos2_x - pos1_x)
            interp_y = pos1_y + 0.5 * (pos2_y - pos1_y)
            
            home_interp_x.append(interp_x)
            home_interp_y.append(interp_y)
        
        # Include players that appear only in frame 1
        for pid in set(away_ids_frame1) - common_away_players:
            pos_x = df_away.loc[(df_away.frame_id == frame) & (df_away.player_id == pid), 'x'].values[0] / 100
            pos_y = df_away.loc[(df_away.frame_id == frame) & (df_away.player_id == pid), 'y'].values[0] / 100
            away_interp_x.append(pos_x)
            away_interp_y.append(pos_y)
            
        for pid in set(home_ids_frame1) - common_home_players:
            pos_x = df_home.loc[(df_home.frame_id == frame) & (df_home.player_id == pid), 'x'].values[0] / 100
            pos_y = df_home.loc[(df_home.frame_id == frame) & (df_home.player_id == pid), 'y'].values[0] / 100
            home_interp_x.append(pos_x)
            home_interp_y.append(pos_y)
        
        # Set player positions with interpolated values
        away.set_data(away_interp_x, away_interp_y)
        home.set_data(home_interp_x, home_interp_y)
    else:
        data_idx = i // 2
        frame = df_ball.loc[data_idx, 'frame_id']
        
        # Set the ball position directly
        ball.set_data([df_ball.loc[data_idx, 'x'] / 100], [df_ball.loc[data_idx, 'y'] / 100])
        
        # Extract player positions
        away_players_x = df_away.loc[df_away.frame_id == frame, 'x'] / 100
        away_players_y = df_away.loc[df_away.frame_id == frame, 'y'] / 100
        home_players_x = df_home.loc[df_home.frame_id == frame, 'x'] / 100
        home_players_y = df_home.loc[df_home.frame_id == frame, 'y'] / 100
        
        # Set player positions
        away.set_data(away_players_x, away_players_y)
        home.set_data(home_players_x, home_players_y)
    
    return ball, away, home

# Double the number of frames (original frames + interpolated frames)
frames_to_animate = (len(df_ball) - 1) * 2  # Each original frame + one interpolated frame

# Set interval to 500ms for 2 frames per second
anim = animation.FuncAnimation(fig, update, frames=frames_to_animate, interval=500, blit=True, repeat=False)
plt.show()



# note th<at its hard to get the ffmpeg requirements right.
# I installed from conda-forge: see the environment.yml file in the docs folder
# how to save animation - commented out for example
#anim.save('example.mp4', dpi=150, fps=25,
#          extra_args=['-vcodec', 'libx264'],
#          savefig_kwargs={'pad_inches':0, 'facecolor':'#457E29'})


