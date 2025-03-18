import sqlite3
import zlib


class DbManager:

    def __init__(self):
        try:
            self.conn = sqlite3.connect("stats.db")
            self.cursor = self.conn.cursor()
            print("DB Init")

        except sqlite3.Error as error:
            print("Error occurred on initialisation - ", error)

    def setup_db(self):
        create_stats_table = '''CREATE TABLE game_stats(
                            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            score INTEGER,
                            time_alive INTEGER,
                            starting_position BLOB,
                            food_positions BLOB,
                            num_food_positions INTEGER,
                            step_data BLOB,
                            num_steps INTEGER)'''
        self.cursor.execute(create_stats_table)

    def save_game(self, score, time_alive, inputs, steps):
        """
        Insert the stats from a game into the DB.
        :param score: Number of apples the snake ate
        :param time_alive: Time in millisec. the snake was alive
        :param inputs: Numpy array with the inputs
        :param steps:
        :return:
        """

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("SQL Connection closed")