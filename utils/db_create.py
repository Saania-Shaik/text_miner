import sqlite3
con = sqlite3.connect("tutorial.db")
cur=con.cursor()
cur.execute("CREATE TABLE sentences(sentence TEXT,score INTEGER,sentiment TEXT)")
cur.execute("CREATE TABLE words(word TEXT,score INT,is_available_in_dict BOOLEAN)")
cur.execute("""
    CREATE TABLE analysis(
        total_sentences INT,
        total_paragraphs INT,
        total_score INT,
        total_words INT,
        total_negative_words INT,
        total_positive_words INT,
        total_dict_hits INT,
        total_dict_miss INT,
        total_negative_sentences INT,
        total_positive_sentences INT
        )
        """
    )

con.commit()
con.close()