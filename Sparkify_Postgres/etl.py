import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import config

def process_song_file(cur, filepath):
    """[This function reads JSON file and insert record into Postgres Database]

    Args:
        cur ([object]): [Cursor for Postgres]
        filepath ([string]): [Path to json file]
    """    
    # open song file
    df = pd.read_json(filepath, lines=True)
    # Select columns
    song_features = ['song_id', 'title', 'artist_id', 'year', 'duration']
    # insert song record
    song_data = df[song_features].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_features = ['artist_id', 'artist_name', 'artist_location',\
        'artist_latitude', 'artist_longitude']
    
    # insert artist record
    artist_data = df[artist_features].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """[This function reads JSON file and insert record into Postgres Database]

    Args:
        cur ([object]): [Cursor for Postgres]
        filepath ([string]): [Path to json file]
    """    
    # open log file
    df = pd.read_json(filepath, lines=True)
    df.ts = pd.to_datetime(df.ts,unit='ms')
    df.rename(columns={'userId': 'user_id', 'firstName':'first_name', 'lastName': 'last_name', \
        'sessionId': 'session_id', 'userAgent' : 'user_agent', 'ts': 'timestamp'}, inplace=True)
    # filter by NextSong action
    df = df[df.page == 'NextSong']
    # convert timestamp column to datetime
    t = df.timestamp
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day,\
             t.dt.week, t.dt.month, \
            t.dt.year, t.dt.dayofweek]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['user_id', 'first_name', 'last_name', 'gender', 'level']]
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.artist, row.song, row.length))
        results = cur.fetchone()
        
        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None
        # insert songplay record
        songplay_data = [row.timestamp, row.user_id, row.level, song_id, \
            artist_id, row.session_id, row.location, row.user_agent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """[Function to process the data files]

    Args:
        cur ([object]): [database cursor]
        conn ([object]): [database connection]
        filepath ([string]): [filepath location]
        func ([func]): [function call to be made]
    """    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(f"host=127.0.0.1 dbname=sparkifydb user={config.user} password={config.password}")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()