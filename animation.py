import numpy as np
import pandas as pd
import psycopg2
import dotenv
import os
from matplotlib import animation
from matplotlib import pyplot as plt

from mplsoccer import Pitch



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
SELECT pt.frame_id, pt.timestamp, pt.player_id, pt.x, pt.y, p.team_id
FROM player_tracking pt
JOIN players p ON pt.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id
WHERE pt.game_id = '5uts2s7fl98clqz8uymaazehg' AND p.player_id = 'ball'
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

our_number = 1722026700000
# animation function
def animate(i):
    """ Function to animate the data. Each frame it sets the data for the players and the ball."""
    # set the ball data with the x and y positions for the ith frame
    ball.set_data(df_ball.iloc[i, [3]], df_ball.iloc[i, [4]])
    # get the frame id for the ith frame
    print(i)
    frame = df_ball.iloc[i, 1]

    # set the player data using the frame id
    away.set_data(df_away.loc[df_away.frame_id - our_number == frame, 'x'],
                  df_away.loc[df_away.frame_id - our_number == frame, 'y'])
    home.set_data(df_home.loc[df_home.frame_id - our_number == frame, 'x'],
                  df_home.loc[df_home.frame_id - our_number == frame, 'y'])
    return ball, away, home


# call the animator, animate so 25 frames per second
anim = animation.FuncAnimation(fig, animate, frames=len(df_ball), interval=1, blit=True)
plt.show()

# note th<at its hard to get the ffmpeg requirements right.
# I installed from conda-forge: see the environment.yml file in the docs folder
# how to save animation - commented out for example
# anim.save('example.mp4', dpi=150, fps=25,
#          extra_args=['-vcodec', 'libx264'],
#          savefig_kwargs={'pad_inches':0, 'facecolor':'#457E29'})


