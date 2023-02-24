from collections import Counter, defaultdict
import sankey as sk


class TextBeast:

    def __init(self):
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        results = {
            'wordcount': Counter(filename.split()),
            'numwords': len(filename.split())
        }

        return results

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label: unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute-->raw data
        """
        for k, v in results.items():
            self.data[k][label] = v

    def load_text(self, filename, label="", parser=None, **kwargs):
        """ Register a document with the framework """
        if parser is None:  # do default parsing of standard .txt file
            results = TextBeast._default_parser(filename)
        else:
            results = parser(filename, kwargs)

        if label is None:
            label = filename

        self._save_results(label, results)

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


