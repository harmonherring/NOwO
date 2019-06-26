def check_space_exception(spaced_text, banned_word):
    """
    Replace inner parts of the word with a space and check if that exists in the text
    :param text:
    :param banned_word:
    :return:
    """
    print("checking space extension")
    for i in range(1, len(banned_word)):
        new_phrase = banned_word[:i] + " " + banned_word[i:]
        print(new_phrase)
        if new_phrase in spaced_text:
            start_index = spaced_text.index(new_phrase)
            end_index = start_index + len(new_phrase)
            print("START: " + spaced_text[start_index-1])
            print("END: " + spaced_text[end_index])
            if spaced_text[start_index-1] != ' ' and spaced_text[start_index-1] != '' \
                and spaced_text[end_index] != ' ' and spaced_text[end_index] != '':
                return False
    return True

print(check_space_exception("to work", "owo"))
