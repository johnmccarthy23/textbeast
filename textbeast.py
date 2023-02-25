from collections import Counter, defaultdict
import sankey as sk


class TextBeast:

    def __init__(self):
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        """
        ...
        returns : list of words in the file not preprocessed yet
        """
        # Read the file
        file = open(filename, "r")
        lines = file.readlines()
        word_list =[]
        for line in lines:
            line = line.split(" ")
            for word in line:
                word_list.append(word.strip(" .\n"))

        return word_list

    @staticmethod
    def _preprocessor(words):
        """
        Preprocess the data file, get rid of any characters that aren't words or actually spoken
        filename : the file we have just loaded
        returns : results
        """
        # Must exclude any non dialogue terms included in the existing word list

        # loop through all the words
        for word in words:
            # get rid of all non dialogue words
            if word == "-":
                words.remove(word)
            elif word.startswith("["):
                words.remove(word)
            elif word.endswith("]"):
                words.remove(word)
            elif word.startswith("("):
                words.remove(word)
            elif word.endswith(")"):
                words.remove(word)

        results = {
            'wordcount': Counter(words),
            'numwords': len(Counter(words))
        }

        return results

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label: unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute-->raw data
        """
        for k, v in results.items():
            self.data[k][label] = v

    def load_text(self, filename, label="", parser=None):
        """ Register a document with the framework """
        if parser is None:  # do default parsing of standard .txt file
            word_list = self._default_parser(filename)
        else:
            word_list = parser(filename)

        # Preprocess the file
        p_results = self._preprocessor(word_list)

        if label is None:
            label = filename

        self._save_results(label, p_results)


    # Register a text file with the library. The label is an optional label you’ll use in your
    # visualizations to identify the text

    @staticmethod
    def load_stop_words(stopfile):
        # A list of common or stop words.  These get filtered from each file automatically
        stop_words = ["a", "the", "is", "are", "an"]
        for word in stop_words:
            del stopfile[word]

        return stopfile

    def wordcount_sankey(self, word_list=None, k=5):
        # Map each text to words using a Sankey diagram, where the thickness of the line
        # is the number of times that word occurs in the text.  Users can specify a particular
        # set of words, or the words can be the union of the k most common words across
        # each text file (excluding stop words).

        # get wordcount dict for instance
        wc = self.data['wordcount']
        # sort the wordcount by most times said
        sorted_wc = sorted(wc.items(), key=lambda x: x[1], reverse=True)
        # get the first k words
        first_k = sorted_wc.iloc[:, :k]

        # We need to find a way to support multiple videos

        # Create dataframe from wordcount dictionary

        # build sankey functionality
        sk.make_sankey()

    def vis2(self):
        """
        Need to use subplots
        """
        pass

    def vis3(self):
        """
        Need to be comparative on one vis
        """
        pass


textbeast = TextBeast()

textbeast.load_text("1000BlindPeopleSeeForTheFirstTime.txt", label="vision")

print(textbeast.data)
