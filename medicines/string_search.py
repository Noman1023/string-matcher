from difflib import SequenceMatcher as sm


class StringFinder:
    """StringFinder is a class for comparing two strings and checking for the similarity for those strings.
    """
    def __init__(self, *args, **kwargs):
        self.key = kwargs.get('key')
        self.values = kwargs.get('values')
        self.matching_criteria = kwargs.get('matching_criteria')

    def get_results(self):
        matched_results = []
        # searching key through all they values

        for val in self.values:
            # implemented our custom search
            matched, perc = self.custom_search(self.key, val)
            if matched:
                matched_results.append({'value': val, 'percentage': perc})
        return matched_results

    # helper function
    @staticmethod
    def find_all(string, word):
        return [i for i in range(len(string)) if string.startswith(word, i)]

    def check_match_criteria(self, key, found_result):
        # checks by finding out number of matched words in the key,
        # if matched then it returns True and matching percentage
        perc = int(len(found_result) / len(list(key)) * 100)
        return (True, f'{perc}%') if perc > self.matching_criteria else (False, 0)

    def custom_search(self, key, val):
        """Compares the key with value by converting both the key and value into list.
           And then looking for each word in a key. If a word is found, the word is
           removed from the key list and added to found list. Once all the values are
           iterated, the number of occurrences is compared with the total words inside
           the key and the ratio is calculated.
        """

        found_results = []

        # converting the key into a list
        key_list = [el for el in key.split(' ') if el]
        key_list_copy = key_list.copy()

        # converting the value into a list too for comparison
        for idx, ch in enumerate([el for el in val.split(' ') if el]):
            if ch in key_list:
                found_results.append((ch, idx))
                # if the value is found, then update the list by removing the matched value
                key_list.pop(key_list.index(ch))

        # check for the matching criteria
        matched, perc = self.check_match_criteria(key_list_copy, found_results)
        return matched, perc

    def next_search(self, str1, str2):
        # string comparison with difflib library
        perc = int(sm(isjunk=None, a=str1, b=str2).ratio() * 100)
        return (True, f'{perc}%') if perc > self.matching_criteria else (False, 0)
