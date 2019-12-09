#Hi hi im just using this file to store a bunch of stuff i was tryna 
#use for the actual notebook dw bout this guy

def read_csv(fn="eggs.csv.gz"):
    """read the GZipped CSV data and split it into headers and newlines.
    
    kwargs:
        fn : str -- .csv.gz file to read
    
    returns: Tuple[headers, body] where
      headers : Tuple[str] -- the CSV headers
      body : List[Tuple[str,...]] -- the CSV body
    """
    with gzip.open(fn, 'rt', newline="", encoding='utf-8') as f:
        csvobj = csv.reader(f)
        headers = next(csvobj)
        return headers, [tuple(row) for row in csvobj]


def load_twitter_data_sqlite3(conn, users_filepath, edges_filepath, tweets_filepath) :
    """ Load twitter data in the three files as tables into an in-memory SQLite database
    Input:
        conn (sqlite3.Connection) : Connection object corresponding to the database; used to perform SQL commands.
        users_filepath (str) : absolute/relative path to users.csv file
        edges_filepath (str) : absolute/relative path to edges.csv file
        tweets_filepath (str) : absolute/relative path to tweets.csv file
    Output:
        None
    """
    #Creating the user Table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE users
    (
    name TEXT,
    screen_name TEXT,
    location TEXT,
    created_at TEXT,
    friends_count INTEGER,
    followers_count INTEGER,
    statuses_count INTEGER,
    favourites_count INTEGER
    );""")
    
    #Creating the tweets Table
    cursor.execute("""
    CREATE TABLE tweets (
    screen_name TEXT,
    created_at TEXT,
    retweet_count INTEGER,
    favorite_count INTEGER,
    text TEXT
    );""")
        
    # Creating the edges Table
    cursor.execute("""
    CREATE TABLE edges (
    screen_name TEXT,
    friend TEXT
    );""")
    
    conn.commit()
    
    
    with gzip.open(users_filepath,'rt',encoding ='utf-8') as f:
        unzip = csv.reader(f)
        output = []
        c = 1
        for r in unzip:
            if (c > 1):    
                output.append(tuple(r))
            c += 1
        #print(type(row))
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', output)


    with gzip.open(tweets_filepath,'rt',encoding ='utf-8') as f:
        unzip = csv.reader(f)
        output = []
        c = 1
        for r in unzip:
            if (c > 1):    
                output.append(tuple(r))
            c += 1
        cursor.executemany('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)',output)
        
    with gzip.open(edges_filepath,'rt',encoding ='utf-8') as f:
        unzip = csv.reader(f)
        output = []
        c = 1
        for r in unzip:
            if (c > 1):    
                output.append(tuple(r))
            c += 1
        cursor.executemany('INSERT INTO edges VALUES (?, ?)',output)
    


