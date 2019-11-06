book_ids = []
user_dict = {}
file = open('books.csv', 'r', encoding="mbcs")
z = open('clean_books.csv', 'w', encoding="mbcs").close()
y = open('clean_books.csv', 'a+', encoding='"mbcs"')
for index, line in enumerate(file):
    if not index:
        y.write(line)
        continue
    elif index <= 100:
        comma_index = line.find(',')
        book_ids.append(line[0:comma_index])
        y.write(line)
    else:
        break

r = open('ratings.csv', 'r', encoding="mbcs")
open('clean_ratings.csv', 'w', encoding='mbcs').close()
f = open('clean_ratings.csv', 'a+', encoding='mbcs')
f.write('user_id,book_id,rating\n')
count = 0
for index, line in enumerate(r):
    if not index:
        continue
    comma_1_index = line.find(',')
    comma_2_index = comma_1_index + 1 + line[comma_1_index + 1:].find(',')
    user_id = line[0:comma_1_index]
    # print('user id 1', user_id)

    book_id = line[comma_1_index + 1:comma_2_index]
    rating = line[comma_2_index + 1:]
    # print('index', index)
    # print('user id 2', user_id)
    if book_id in book_ids:
        if user_id in user_dict:
            user_id = user_dict[user_id]
            # print('selected from dict', user_id)
        else:
            count += 1
            user_dict[user_id] = count
            user_id = count
        the_line = str(user_id)+','+book_id+','+rating
        f.write(the_line)
