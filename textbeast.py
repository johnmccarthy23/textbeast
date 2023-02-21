from collections import Counter


class TextBeast:

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

    def load_text(self, filename, label="", parser=None):
        """ Register a document with the framework """
        if parser is None:  # do default parsing of standard .txt file
            results = TextBeast._default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        self._save_results(label, results)

    # Register a text file with the library. The label is an optional label you’ll use in your
    # visualizations to identify the text

    def load_stop_words(stopfile):
        pass

    # A list of common or stop words.  These get filtered from each file automatically

    def wordcount_sankey(self, word_list=None, k=5):
        pass
    # Map each text to words using a Sankey diagram, where the thickness of the line
    # is the number of times that word occurs in the text.  Users can specify a particular
    # set of words, or the words can be the union of the k most common words across
    # each text file (excluding stop words).