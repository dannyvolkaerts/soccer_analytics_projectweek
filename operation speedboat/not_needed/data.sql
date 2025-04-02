CREATE TABLE eventtypes (
    eventtype_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    match_date TEXT,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER
);

CREATE TABLE matchevents (
    match_id INTEGER,
    event_id INTEGER,
    eventtype_id INTEGER,
    result TEXT,
    success INTEGER,
    period_id INTEGER,
    timestamp TEXT,
    end_timestamp TEXT,
    ball_state TEXT,
    ball_owning_team INTEGER,
    team_id INTEGER,
    player_id INTEGER,
    x INTEGER,
    y INTEGER,
    end_coordinates_x INTEGER,
    end_coordinates_y INTEGER,
    receiver_player_id INTEGER
);

CREATE TABLE player_tracking (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    frame_id INTEGER,
    timestamp TEXT,
    period_id INTEGER,
    player_id INTEGER,
    x INTEGER,
    y INTEGER
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT,
    team_id INTEGER,
    jersey_number INTEGER
);

CREATE TABLE qualifiers (
    match_id INTEGER,
    event_id INTEGER,
    qualifier_type_id INTEGER,
    qualifier_value TEXT
);

CREATE TABLE qualifiertypes (
    qualifier_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE spadl_actions (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    period_id INTEGER,
    seconds INTEGER,
    player_id INTEGER,
    team_id INTEGER,
    start_x INTEGER,
    start_y INTEGER,
    end_x INTEGER,
    end_y INTEGER,
    action_type TEXT,
    result TEXT,
    bodypart TEXT
);

CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT
);

-- eventtypes
INSERT INTO eventtypes (eventtype_id, name, description) VALUES
(1001, 'Squirrel Interference', 'A squirrel disrupts the match.'),
(1002, 'Referees Interpretive Dance', 'The referee pauses the game for an impromptu dance routine.'),
(1003, 'Sudden Onset of Yodeling', 'A player spontaneously bursts into yodeling.'),
(1004, 'Alien Abduction', 'A player is temporarily abducted by aliens.'),
(1005, 'Massive Confetti Eruption', 'A sudden and overwhelming eruption of confetti halts the game.'),
(1006, 'Synchronized Seagull Formation', 'Seagulls perform a complex aerial formation over the field.'),
(1007, 'Unexpected Opera Performance', 'An opera singer spontaneously appears and performs an aria.'),
(1008, 'Sudden Shift to Zero Gravity', 'The field experiences a brief period of zero gravity.');

-- matches
INSERT INTO matches (match_id, match_date, home_team_id, away_team_id, home_score, away_score) VALUES
(9001, '2024-04-01', 1, 2, 42, 42),
(9002, '2024-04-02', 3, 4, 0, 0),
(9003, '2024-04-03', 5, 6, 1, 100),
(9004, '2024-04-04', 1, 3, 7, 7),
(9005, '2024-04-05', 2, 5, 10, 11),
(9006, '2024-04-06', 4, 6, 999, 0); -- A massive score difference

-- matchevents
INSERT INTO matchevents (match_id, event_id, eventtype_id, result, success, period_id, timestamp, end_timestamp, ball_state, ball_owning_team, team_id, player_id, x, y, end_coordinates_x, end_coordinates_y, receiver_player_id) VALUES
(9001, 1001, 1001, 'Interrupted', 0, 1, '00:15:00', '00:15:05', 'InPlay', 1, 1, 101, 50, 50, 50, 50, NULL),
(9002, 1002, 1002, 'Successful', 1, 2, '00:30:00', '00:30:30', 'OutOfPlay', 0, NULL, NULL, 50, 50, 50, 50, NULL),
(9003, 1003, 1003, 'Successful', 1, 3, '00:45:00', '00:45:10', 'InPlay', 2, 2, 105, 75, 25, 75, 25, NULL),
(9001, 1004, 1004, 'Abducted', 0, 4, '00:60:00', '00:60:05', 'InPlay', 1, 1, 102, 25, 75, 25, 75, NULL),
(9004, 1005, 1005, 'Interrupted', 1, 1, '00:10:00', '00:10:15', 'OutOfPlay', 1, 1, 103, 30, 60, 30, 60, NULL),
(9005, 1006, 1006, 'Successful', 1, 2, '00:25:00', '00:25:20', 'InPlay', 2, 2, 104, 70, 40, 70, 40, NULL),
(9006, 1007, 1007, 'Interrupted', 1, 3, '00:40:00', '00:41:00', 'OutOfPlay', 1, 4, 106, 10, 90, 10, 90, NULL),
(9006, 1008, 1008, 'Interrupted', 1, 4, '00:55:00', '00:55:10', 'InPlay', 2, 6, 107, 90, 10, 90, 10, NULL);

-- player_tracking
INSERT INTO player_tracking (game_id, frame_id, timestamp, period_id, player_id, x, y) VALUES
(9001, 1, '00:00:01', 1, 101, 50, 50),
(9001, 2, '00:00:02', 1, 101, 51, 52),
(9001, 3, '00:00:03', 1, 101, 53, 55),
(9001, 1000, '00:15:00', 1, 101, 50, 50),
(9001, 1001, '00:15:01', 1, 101, 50, 50),
(9001, 1002, '00:15:02', 1, 5000, 50, 50),
(9001, 1003, '00:15:03', 1, 5000, 50, 50),
(9001, 1004, '00:15:04', 1, 5000, 50, 50),
(9006, 2000, '00:55:01', 4, 107, 90, 10),
(9006, 2001, '00:55:02', 4, 107, 90, 10),
(9006, 2002, '00:55:03', 4, 107, 90, 10),
(9006, 2003, '00:55:04', 4, 107, 90, 10);

-- players
INSERT INTO players (player_id, player_name, team_id, jersey_number) VALUES
(101, 'Sir Reginald Dunkalot', 1, 1),
(102, 'Speedy McShooty', 1, 2),
(103, 'Professor Foulplay', 2, 3),
(104, 'Captain Kickypants', 2, 4),
(105, 'Yodeling Yeti', 3, 5),
(106, 'Opera Octavius', 4, 6),
(107, 'Zero Gravity Zane', 6, 7),
(5000, 'Invisible Man', 1, 99);

-- qualifiers
INSERT INTO qualifiers (match_id, event_id, qualifier_type_id, qualifier_value) VALUES
(9001, 1001, 1, 'Very Large Squirrel'),
(9002, 1002, 2, 'Tango'),
(9003, 1003, 3, 'Alpine Style'),
(9001, 1004, 4, 'Tractor Beam'),
(9004, 1005, 5, 'Rainbow Confetti'),
(9005, 1006, 6, 'V-Formation'),
(9006, 1007, 7, 'Dramatic Soprano'),
(9006, 1008, 8, 'Anti-Gravity Boots');

-- qualifiertypes
INSERT INTO qualifiertypes (qualifier_id, name, description) VALUES
(1, 'Squirrel Size', 'The size of the interfering squirrel.'),
(2, 'Dance Style', 'The style of the referee''s dance.'),
(3, 'Yodeling Style', 'The style of the player''s yodeling.'),
(4, 'Abduction Method', 'The method used for alien abduction.'),
(5, 'Confetti Type', 'Type of confetti used in the eruption.'),
(6, 'Seagull Formation', 'The aerial formation performed by the seagulls.'),
(7, 'Opera Style', 'The style of the opera performance.'),
(8, 'Gravity Alteration', 'The method used to alter gravity.');

-- spadl_actions
INSERT INTO spadl_actions (game_id, period_id, seconds, player_id, team_id, start_x, start_y, end_x, end_y, action_type, result, bodypart) VALUES
(9001, 1, 15, 101, 1, 50, 50, 50, 50, 'interception', 'fail', 'head'),
(9002, 2, 30, NULL, NULL, 50, 50, 50, 50, 'referee_action', 'success', 'legs'),
(9003, 3, 45, 105, 3, 75, 25, 75, 25, 'shot', 'success', 'voice'),
(9001, 4, 60, 102, 1, 25, 75, 25, 75, 'out', 'fail', 'whole_body'),
(9004, 1, 10, 103, 2, 30, 60, 30, 60, 'foul', 'fail', 'confetti_cannon'),
(9005, 2, 25, 104, 2, 70, 40, 70, 40, 'pass', 'success', 'wings'),
(9006, 3, 40, 106, 4, 10, 90, 10, 90, 'shot', 'fail', 'vocal_cords'),
(9006, 4, 55, 107, 6, 90, 10, 90, 10, 'dribble', 'success', 'boots');

-- teams
INSERT INTO teams (team_id, team_name) VALUES
(1, 'The Flying Squirrels'),
(2, 'The Dancing Referees'),
(3, 'The Yodeling Yetis'),
(4, 'The Opera Performers'),
(5, 'The Seagull Squadron'),
(6, 'The Zero Gravity Zephyrs');
