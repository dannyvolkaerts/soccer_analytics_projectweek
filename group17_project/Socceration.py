import psycopg2
import dotenv
import os
import pandas as pd
import numpy as np

dotenv.load_dotenv()

PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_USER = os.getenv("PG_USER")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DB")

# Database connection
def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT,
        sslmode="require",
    )

# Fetch event data from the database (Updated query)
def get_event_data(game_id):
    query = """
    SELECT 
        e.name AS event_type,
        me.player_id, 
        me.team_id, 
        me.x, 
        me.y, 
        me.match_id AS game_id, 
        me.timestamp AS time, 
        me.result AS outcome
    FROM matchevents me
    JOIN eventtypes e ON me.eventtype_id = e.eventtype_id
    WHERE me.match_id = %s
    """
    connection = get_connection()
    df = pd.read_sql(query, connection, params=(game_id,))  # Passing game_id directly without casting
    connection.close()
    return df

# Convert event data to SPADL (Simple Player Action Data Language)
def convert_to_spadl(df):
    spadl_data = []
    for _, row in df.iterrows():
        action = {
            'player_id': row['player_id'],
            'event_type': row['event_type'],
            'x': row['x'],
            'y': row['y'],
            'outcome': row['outcome'],
            'time': row['time'],
            'team_id': row['team_id'],
            'game_id': row['game_id']
        }
        spadl_data.append(action)
    spadl_df = pd.DataFrame(spadl_data)
    return spadl_df

# Custom function to calculate xT (Expected Threat)
def calculate_xt(df):
    pitch_length = 100
    pitch_width = 100
    
    grid = np.zeros((pitch_length, pitch_width))

    for _, row in df.iterrows():
        start_x = int(row['x'])  # Start position x
        start_y = int(row['y'])  # Start position y
        
        print(f"Processing event: {row['event_type']} | x: {start_x}, y: {start_y}, outcome: {row['outcome']}")  # Debugging

        if pd.isna(row['outcome']) or row['outcome'] == 'INCOMPLETE' or row['outcome'] == 'None':
            print(f"Skipping invalid outcome: {row['outcome']}")
            continue  # Skip invalid outcome
        
        # Process Pass Events
        if row['event_type'] == 'PASS':
            try:
                end_x, end_y = int(row['outcome'][0]), int(row['outcome'][1])
                xT = 0.05 * (end_x - start_x) + 0.05 * (end_y - start_y)
                grid[start_x, start_y] += xT
                print(f"Calculated xT: {xT} for pass")  # Debugging
            except ValueError:
                continue
        
        # Process Shot Events
        elif row['event_type'] == 'SHOT':
            try:
                end_x, end_y = int(row['outcome'][0]), int(row['outcome'][1])
                xT = 0.2 * (100 - end_x) + 0.1 * (end_y - 50)
                grid[start_x, start_y] += xT
                print(f"Calculated xT: {xT} for shot")  # Debugging
            except ValueError:
                continue
        
        # Process Duel Events: Add small xT for winning duels
        elif row['event_type'] == 'DUEL' and row['outcome'] == 'WON':
            xT = 0.05  # Small xT for winning duels
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for duel (won)")  # Debugging

        # Process Take-On Events: Add xT for successful take-ons
        elif row['event_type'] == 'TAKE_ON' and row['outcome'] == 'SUCCESS':
            xT = 0.05  # Small xT for successful take-ons
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for take-on")  # Debugging
        
        # Process Recovery Events: Assign minimal xT for recoveries
        elif row['event_type'] == 'RECOVERY':
            xT = 0.02  # Minimal xT for recovery
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for recovery")  # Debugging

        # Process Interception Events: Assign minimal xT for interceptions
        elif row['event_type'] == 'INTERCEPTION':
            xT = 0.03  # Small xT for intercepting the ball
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for interception")  # Debugging
        
        # Process Ball Touch Events: Add small xT for significant touches
        elif row['event_type'] == 'GENERIC:ball touch':
            xT = 0.01  # Small xT for a ball touch
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for ball touch")  # Debugging
        
        # Other generic events can be ignored or assigned minimal xT if relevant
        elif row['event_type'] == 'GENERIC:dispossessed':
            xT = 0.01  # Minimal xT for being dispossessed
            grid[start_x, start_y] += xT
            print(f"Calculated xT: {xT} for dispossessed")  # Debugging

        # You can add more event types with similar logic

    xt_df = pd.DataFrame(grid, columns=[f"y_{i}" for i in range(pitch_width)])
    return xt_df


def main():
    game_id = "5pcyhm34h5c948yji4oryevpw"  # Example match ID (update with a valid one)
    event_data = get_event_data(game_id)
    
    # Check if event data is empty (debugging purpose)
    if event_data.empty:
        print(f"No event data found for game_id: {game_id}")
    else:
        print(event_data.head())  # Print first 5 rows to see the data structure
    
    spadl_data = convert_to_spadl(event_data)
    
    # Calculate xT values
    xt_values = calculate_xt(spadl_data)

    # Print the xT values (showing the head of the dataframe)
    print(xt_values.head())

if __name__ == '__main__':
    main()
