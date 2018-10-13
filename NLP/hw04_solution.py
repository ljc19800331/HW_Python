def finish_sentence(initial_str,number,corpus):
    current_str = initial_str[-number:]
    corpus_list = [corpus[m:m+number] for m in range(0,len(corpus)-number)]
    print("The current is ", current_str)
    print("The corpus list is ", corpus_list)
    count = 1
    while 1:
        # print(count)
        indices = [i for i, x in enumerate(corpus_list) if x == current_str]
        n_dict = dict()
        for ind in indices:
            next_word = corpus_list[ind+1][-1]
            if next_word in n_dict.keys():
                n_dict[next_word] += 1
            else:
                n_dict[next_word] = 1

        max_word = max(n_dict, key = n_dict.get)
        initial_str.append(max_word)
        current_str = initial_str[-number:]

        count += 1
        if max_word in ['.','?','!']:
            break

    return initial_str


