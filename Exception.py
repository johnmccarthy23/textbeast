class ParsingError(Exception):
    """ A user-defined exception for signalling a parsing issue """
    def __init__(self, text, msg=''):
        super().__init__("Text was not parsed")
        self.text = text
        self.msg = msg


class PreProcessingError(Exception):
    """ A user-defined exception for signalling a preprocessing issue """
    def __init__(self, text, msg=''):
        super().__init__("Text was not processed")
        self.text = text
        self.msg = msg

def check_parse(results):
    """ Checks if text was parsed into the correct dictionary format """
    try:
        assert len(results['wordcount']) > 0, 'wordcount dictionary has no items'
        assert results['numwords'] > 0, 'Number of words must be greater than 0'

    except Exception as e:
        raise ParsingError(results, str(e))


def check_preprocess(processed):
    """
    Checks if text was processed and unwanted characters were correctly filtered
    """
    try:
        assert len(processed) > 0, 'Processed list has no items'

        flag = False
        for i in range(len(processed)):
            # flag equals true if unwanted character is in string
            flag = processed[i].__contains__("[") or processed[i].__contains__("]") or \
                   processed[i].__contains__("(") or processed[i].__contains__(")") or \
                   processed[i].__contains__("-")
            # break loop if unwanted character is found
            if flag:
                break
        assert not flag, 'Text contains a bracket, parenthesis, or dash'

    except Exception as e:
        raise PreProcessingError(processed, str(e))
