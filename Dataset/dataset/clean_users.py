file = open('clean_ratings.csv', 'r', encoding='"mbcs"')
user_dict = {}
first_line = None
for index, line in enumerate(file):
    if not index:
        first_line = line
        continue
    comma_1_index = line.find(',')
    comma_2_index = comma_1_index + 1 + line[comma_1_index + 1:].find(',')
    user_id = line[0:comma_1_index]
    # print('user id 1', user_id)

    book_id = line[comma_1_index + 1:comma_2_index]
    rating = line[comma_2_index + 1:]
    # print('index', index)
    # print('user id 2', user_id)
    int_user = int(user_id)
    user_id = int_user // 8

    if user_id in user_dict:
        tuple_list = user_dict[user_id]
        if len(tuple_list) >= 5:
            continue
        book_was_in = False
        for tuple in tuple_list:
            if tuple[0] == book_id:
                book_was_in = True
        if not book_was_in:
            user_dict[user_id].append((book_id, rating))
    else:
        user_dict[user_id] = [(book_id, rating)]

y = open('cleaner_ratings.csv', 'a+', encoding='"mbcs"')
y.write(first_line)
print(user_dict)
for user_id in user_dict:
    for book_id, rating in user_dict[user_id]:
        the_line = str(user_id) + ',' + str(book_id) + ',' + str(rating)
        y.write(the_line)