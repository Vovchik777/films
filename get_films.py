import sqlite3
import colorama
import datetime
import tkinter as tk
#import collections
#genresdict = collections.defaultdict(int)
#from pprint import pprint
conn = sqlite3.connect('films.db')
cursor = conn.cursor()
# genres = 'sci-fi'
# years, minutes = [], []
# isAdult = 0
# result = ''
# # cursor.execute("DELETE from ru_films WHERE id NOT IN (SELECT id FROM films)")
# # print(f'{cursor.rowcount} rows deleted')
# # genre = 'comedy'
# # #filmes = cursor.execute('''SELECT name,year, isAdult FROM films WHERE genres LIKE ? AND minutes > 45 AND minutes < 150 AND year > 2020 AND isAdult = 0 ''', (f"%{genre}%"))
# def get_films_by_genre(genre: str, minutes: list, years: list, isAdult: int):
#   global result
#   if years == []: years = [-1,-1]
#   if minutes == []: minutes = [-1,-1]
#   genre_str = '(1=1'
#   if genre != '':
#       for g in genre.split(','):
#           genre_str += " AND UPPER(genres) LIKE UPPER('%"+g+"%')"
#   else: genre_str += ' AND UPPER(genres) LIKE UPPER("%COMEDY%")'
#   genre_str += ')'
#   query = '''
#   SELECT COALESCE(ru_films.name, films.name) as name, year,genres, minutes
#   FROM films 
#   LEFT JOIN ru_films ON ru_films.id = films.id 
#   WHERE ''' + genre_str + ''' 
#     AND minutes >= ? 
#     AND minutes <= ? 
#     AND year >= ? 
#     AND year <= ?
#     AND isAdult = ?
#   ORDER BY year
#   LIMIT 100
#   '''
#   print(query)
#   result = cursor.execute(query, (f'{minutes[0]}' if minutes[0] != -1 else 0,
#                                 f'{minutes[1]}' if minutes[1] != -1 else 999,
#                                 f'{years[0]}' if years[0]  != -1 else 0,
#                                 f'{years[1]}' if years[1] != -1 else 9999, 
#                                 f'{isAdult}')
#                         ).fetchall()
#   #for i  in result:print(i)
# root = tk.Tk()
# root.title("films")
# root.geometry("1000x800+100+100")
# root.colormapwindows()
# search = tk.Button(root, text="Search", command=get_films_by_genre(genre=genres, minutes=minutes, years=years, isAdult=isAdult))
# search.pack(padx=[700,0], pady=50, fill="x")

# counter = 0
# for i in result:
#   resulttext = tk.Label(root, text=i)
#   resulttext.pack(expand=True,padx=[100,0], fill="x",pady=0+2*counter)
#   counter+=1
# root.mainloop()
#films = 0
# for i in get_films_by_genre(genre='Action,Adventure,Animation,', minutes=[], years=[], isAdult=0):
#     if i[1] <= datetime.datetime.now().year:
#         print(i)
#         films +=1
#     else: print(colorama.Fore.CYAN + colorama.Back.BLACK + i[0] + colorama.Back.RESET + colorama.Fore.RED + " will be released in "
#                 + colorama.Fore.YELLOW + str({i[1]}) + colorama.Fore.RESET+ "😢")
# print(colorama.Fore.LIGHTBLACK_EX+ f'''
# ████████████████████████████████████████████████████████
# ████████████████████████████████████████████████████████ {colorama.Fore.RESET}
#                     films: {films}''')
# max_year = cursor.execute('''SELECT year,count(*) FROM films GROUP BY year ORDER BY year''')
# #print(get_films_by_genre('drama,horror', [45,120], 2020, 0))
# films = cursor.execute('''SELECT *
# res = collections.defaultdict(int)
# harry_potter = cursor.execute('''SELECT genres,count(*) FROM films WHERE name LIKE '%Harry Potter%' GROUP BY genres''')
# for i in harry_potter.fetchall():
#     for j in i[0].split(','):
#         #res[i[0]] += i[1]
#         res[j] += i[1]
# for i in res:
#     print(i,res[i])
#print(harry_potter.fetchall())
#cursor.execute('''DROP TABLE films_rating''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS films_rating (
        id TEXT PRIMARY KEY,
        rating FLOAT
    )
''')

cursor.execute("VACUUM")
import csv
with open('title.ratings.tsv','r',encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)
    headers = next(reader)  # пропускаем заголовок
    #ids = cursor.execute('SELECT id FROM films').fetchall()
    for row in reader:
        cursor.execute("""
            INSERT INTO films_rating (id, rating)
            SELECT ?, ?
            WHERE EXISTS (SELECT 1 FROM films WHERE id = ?)
            """, (row[0], row[1], row[0])
            )
        print(row[0])
        # if row[3] == 'RU' and row[5] not in ['alternative', '\\N']: #and row[0] in ids:
        #     try:
        #         cursor.execute("INSERT INTO ru_films (id, name) VALUES (?, ?)",
        #                     (row[0], row[2]))
        #     except:
        #         continue
        #     print(row)
        # cursor.execute("INSERT INTO films (id, name, isAdult,year,minutes,genres) VALUES (?, ?, ?, ?, ?, ?)",
        #                (row[0], row[2], int(row[4]) if row[4].isdigit() else 0,int(row[5]) if row[5].isdigit() else 0,int(row[7]) if row[7].isdigit() else 0,row[8]))

conn.commit()
conn.close()