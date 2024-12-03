class PathFormatter:

    @staticmethod
    def format(path, skip_capitalization = False):
        split_path = path.split("/")
        split_path_length = len(split_path) - 1
        formatted_path = ""

        for index, word in enumerate(split_path):
            string_format = "{}" if split_path_length == index else "{}."

            if "-" in word:
                split_words = word.split("-")
                split_words_length = len(split_words) -1

                for index, split_word in enumerate(split_words):
                    word_format = "{}" if split_words_length == index else "{}"
                    
                    if not skip_capitalization:
                        split_word = str(split_word.capitalize())

                    formatted_path += word_format.format(split_word)
            else:
                if not skip_capitalization:
                    word = str(word).capitalize()

                formatted_path += string_format.format(word)

        return formatted_path