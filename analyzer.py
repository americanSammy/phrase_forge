# analyzer.py
import sqlite3
from collections import Counter
from utils import extract_words_from_text

class Analyzer:
    @staticmethod
    def analyze_chat_db(chat_db_path):
        try:
            connection = sqlite3.connect(chat_db_path)
            cursor = connection.cursor()
            query = "SELECT text FROM message"
            cursor.execute(query)
            messages = cursor.fetchall()

            all_words = [word for message in messages if message[0] for word in extract_words_from_text(message[0])]
            common_words = Counter(all_words).most_common(300)

            return common_words

        except Exception as e:
            raise RuntimeError(f"An error occurred during analysis: {e}")

        finally:
            connection.close()
