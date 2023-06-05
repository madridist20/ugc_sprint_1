import time
import datetime
import random
import multiprocessing
from clickhouse_driver import Client
from tqdm import tqdm

# Connect to ClickHouse server
client = Client('localhost')

# Create the test table if it doesn't exist
# create_table_query = '''
    # CREATE TABLE IF NOT EXISTS user_progress (
        # user_id Int32,
        # movie_id Int32,
        # progress Float64,
        # timestamp DateTime
    # ) ENGINE = MergeTree()
    # PARTITION BY toYYYYMMDD(timestamp)
    # ORDER BY (user_id, movie_id, timestamp)
# '''
# client.execute(create_table_query)

# Function to insert random data into the table
def insert_data(total_rows):
    insert_query = 'INSERT INTO user_progress (user_id, movie_id, progress, timestamp) VALUES'
    data = [(random.randint(1, 100), random.randint(1, 100), random.random(), datetime.datetime.now()) for _ in range(total_rows)]
    client.execute(insert_query, data)

# Function to simulate background load with concurrent write operations
def background_load(total_rows, interval, event):
    while not event.is_set():
        insert_data(total_rows)
        time.sleep(interval)

# Function to read all data from the table
def read_data():
    select_query = 'SELECT user_id, movie_id, progress FROM user_progress WHERE user_id = 1'
    result = client.execute(select_query)
    return result

if __name__ == '__main__':
    # Start the background load process with concurrent write operations
    total_rows = 1000  # Number of rows to insert in each background load operation
    interval = 1  # Interval between consecutive background load operations in seconds
    write_iterations = 10  # Number of write iterations
    write_intervals = write_iterations - 1  # Number of intervals (sleep time) between write iterations
    write_event = multiprocessing.Event()
    background_process = multiprocessing.Process(target=background_load, args=(total_rows, interval, write_event))
    background_process.start()

    # Measure the write velocity
    start_time = time.time()
    for i in tqdm(range(write_iterations), desc='Write Iterations', unit='iteration'):
        insert_data(total_rows)
        if i < write_intervals:
            time.sleep(interval)  # Wait for interval seconds between write iterations
    end_time = time.time()

    # Stop the background load process
    write_event.set()
    background_process.join()

    total_rows_inserted = total_rows * write_iterations
    write_time = (end_time - start_time) - (interval * write_intervals)  # Exclude interval time from total time
    write_velocity = total_rows_inserted / write_time
    print(f'Write Velocity: {write_velocity:.2f} rows/s')

    # Measure the read velocity
    start_time = time.time()
    read_iterations = 10  # Number of read iterations
    read_intervals = read_iterations - 1  # Number of intervals (sleep time) between read iterations
    for i in tqdm(range(read_iterations), desc='Read Iterations', unit='iteration'):
        result = read_data()
        if i < read_intervals:
            time.sleep(interval)  # Wait for interval seconds between read iterations
    end_time = time.time()

    total_rows_read = len(result) * read_iterations
    read_time = (end_time - start_time) - (interval * read_intervals)  # Exclude interval time from total time
    read_velocity = total_rows_read / read_time
    print(f'Read Velocity: {read_velocity:.2f} rows/s')

    #

