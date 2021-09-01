# DROP TABLES

songplay_table_drop = "DROP table songplay"
user_table_drop = "DROP table user"
song_table_drop = "DROP table song"
artist_table_drop = "DROP table artist"
time_table_drop = "DROP table time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (songplay_id int, start_time timestamp, user_id int, \
level varchar, song_id int, artist_id int, session_id int, location varchar, user_agent varchar)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user (user_id int, first_name varchar, last_name varchar, last_name varchar, \
    gender varchar, level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id int, title varchar, artist_id int, year int, duration numeric)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id int, name varchar, location varchar, latitude numeric, longitude numeric)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp, hour int, day int, week int, month int, year int, weekday varchar)
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]