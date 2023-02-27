from collections import Counter, defaultdict
import pandas as pd
import sankey as sk
from wordcloud import WordCloud
import matplotlib.pyplot as plt




class TextBeast:

    def __init__(self):
        self.data = defaultdict(dict)
        self.stopwords = []

   
    def _default_parser(self, processed_lines):
        """
        parser 
        """
        # Initiate a word list
        word_list =[]
        # Go over the processed lines
        for line in processed_lines:
            # Split the line into words
            line = line.split(" ")
            # Loop over the words in line
            for word in line:
                word = word.lower().strip(" ,().\n?!")
                # Check if word is the empty string
                if word == "":
                    pass
                elif word in self.stopwords:
                    pass
                else:
                    # Append the stripped words to word_list
                    word_list.append(word)
        word_list

        # Get desired results for later into a dictionary
        results = {
            'wordcount': Counter(word_list),
            'numwords': len(word_list)
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

    def load_stop_words(self, stopfile):
        """
        Takes in a plain text file of stopwords
        returns : a list of stopwords
        """
        file = open(stopfile, "r")
        for w in file.readlines():
            if w.startswith("#"):
                pass
            else:
                word = w.strip()
                self.stopwords.append(word)

        return self.stopwords

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Create a Sankey Diagram showing the word count of the
        k most said words in each video or from a user_given word_list
        """

        # get wordcount dict for instance
        wc = self.data['wordcount']
        print(wc)

        # creating an empty DataFrame containing columns for left, right, and width
        df = pd.DataFrame(columns=["video", "word", "count"])

        # iterating through article, then wordcount
        for key, val in wc.items():
            for ke, v in val.items():
                # appending to df each wordcount and its value
                df.loc[len(df.index)] = [key, ke, v]

        # Separating the data by video
        df_vision = df[df['video'] == 'vision'].dropna()
        df_jet = df[df['video'] == 'jet'].dropna()
        df_prison = df[df['video'] == 'prison'].dropna()

        # Sorting each df's values in desc order
        df_vision = df_vision.sort_values(by=['count'], ascending = False)
        df_jet = df_jet.sort_values(by=['count'], ascending = False)
        df_prison = df_prison.sort_values(by=['count'], ascending = False)

        # Find the k most common words in each video
        df_jet = df_jet.head(k)
        df_vision = df_vision.head(k)
        df_prison = df_prison.head(k)

        # Combine the 3 df's into df_result (to be used for sankey)
        frames = [df_jet, df_vision, df_prison]
        df_result = pd.concat(frames)

        # If word_list is given, then use that as the target values
        # else create Sankey using df_result
        if word_list is not None:
            sk.make_sankey(df,'video', 'word_list','count')
        else:
            sk.make_sankey(df_result,'video','word','count')


    def make_wordcloud(self, vid_dict, analysis_type):
        """
        Make wordcloud
        """
        # the sub-dictionary of the stat you want to analyze
        analysis_dict = vid_dict[analysis_type]

        # Start making the plt figure
        fig = plt.figure()
        fig.set_facecolor('red')
        # loop over how many files are in the data
        for i in range(len(analysis_dict)):
            # access the counter dictionary
            counter_dict = list(analysis_dict.values())[i]
            # create wordcloud
            cloud = WordCloud(background_color="white",width=1000,height=1000, max_words=10,relative_scaling=0.5,
                            normalize_plurals=False).generate_from_frequencies(counter_dict)
            # For each file make a subplot
            ax = fig.add_subplot((len(analysis_dict) // 3), 3, i + 1)
            ax.imshow(cloud)
            ax.axis("off")
            ax.set_title(f"{list(analysis_dict.keys())[i]}")
        plt.show()

    def numwords_bar(self, vid_dict, analysis_type, title=None, ylabel=None):
        """
        Create bar chart of the number of words in each file
        """
        # get self.data
        # access the numwords sub-dictionary
        # create a bar that represents each file

        analysis_dict = vid_dict[analysis_type]

        key_list = []
        value_list = []
        for k, v in analysis_dict.items():
            key_list.append(k)
            value_list.append(v)

        if ylabel is not None:
            pass
        else:
            ylabel = analysis_type
        # Create visualization
        plt.bar(list(range(len(analysis_dict))), value_list, tick_label=key_list)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()


textbeast = TextBeast()

textbeast.load_stop_words("./stopwords.txt")

print(textbeast.stopwords)
textbeast.load_text("./Data/1000BlindPeopleSeeForTheFirstTime.txt", label="vision")
textbeast.load_text("./Data/10000EveryDayYouSurvivePrison.txt", label="prison")
textbeast.load_text("./Data/LastToTakeHandOffJetKeepsIt.txt", label="jet")

print(f"Data Dict: {textbeast.data['wordcount']['prison']}")

textbeast.wordcount_sankey()

textbeast.make_wordcloud(textbeast.data, "wordcount")

textbeast.numwords_bar(textbeast.data, "numwords", "Comparing Length of Video Transcripts", "Word Count")

