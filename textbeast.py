from collections import Counter, defaultdict
import sankey as sk


class TextBeast:

    def __init__(self):
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(processed_lines):
        """

        """
        # Initiate a word list
        word_list =[]
        # Go over the processed lines
        for line in processed_lines:
            # Split the line into words
            line = line.split(" ")
            # Loop over the words in line
            for word in line:
                word = word.lower().strip(" .\n?!")
                # Check if word is the empy string
                if word == "":
                    pass
                else:
                    # Append the stripped words to word_list
                    word_list.append(word)

        # Get desired results for later into a dictionary
        results = {
            'wordcount': Counter(word_list),
            'numwords': len(Counter(word_list))
        }

        return results

    @staticmethod
    def _preprocessor(filename):
        """
        Preprocess the data file, get rid of any characters that aren't words or actually spoken
        filename : the file we have just loaded
        returns : processed file
        """
        # Must exclude any non dialogue terms included in the existing word list
        file = open(filename, "r")
        lines = file.readlines()
        processed = []
        for line in lines:

            # If a line contains parentheses remove parentheses and what's inside
            if "(" in line:
                # Find indices of parentheses
                start_pos = line.find("(")
                stop_pos = line.find(")")
                # Index string for characters not inside ()
                line = f"{line[:start_pos]}{line[stop_pos+1:]}"
            # If a line contains a bracket remove the bracket and what's inside
            if "[" in line:
                # Find indices of brackets
                start_pos = line.find("[")
                stop_pos = line.find("]")
                # Index string for characters not inside []
                line = f"{line[:start_pos]}{line[stop_pos+1:]}"
            # Remove all dashes from each line in the file
            line = line.strip("-")
            processed.append(line)
        print(f"Processed: {processed}")

        return processed

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label: unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute-->raw data
        """
        for k, v in results.items():
            self.data[k][label] = v

    def load_text(self, filename, label="", parser=None):
        """ Register a document with the framework """
        # Preprocess the file

        processed_file = self._preprocessor(filename)
        if parser is None:  # do default parsing of standard .txt file
            results = self._default_parser(processed_file)
        else:
            results = parser(processed_file)

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


textbeast = TextBeast()

textbeast.load_text("1000BlindPeopleSeeForTheFirstTime.txt", label="vision")

print(f"Data Dict: {textbeast.data}")
