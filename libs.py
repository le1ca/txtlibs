import re

class lib:
    """ Madlibs-like story parser and formatter
    """

    # regular expression for parsing substitution definitions
    _pat = re.compile("\$\{(?:([^\}]+):)?([^\}]*?)\}")
        
    def __init__(self, inputFile):
        """ Constructor:
            Loads the story from the given inputFile
        """
        
        fh = open(inputFile, 'r')
        self._parse(fh)
        fh.close()
        
    def _parse(self, fh):
        """ Internal helper routine:
            Parses substitutions from the input file behind fh and stores the
            definitions of the substitutions which have to be made.
        """
        self._subs = []
        lines = []
        for line in fh:
            end = 0
            proc = []
            for m in lib._pat.finditer(line):
                m_beg, m_end = m.span()
                self._subs.append((m.group(1), m.group(2)))
                proc.append(line[end:m_beg])
                proc.append("%s")
                end = m_end
            proc.append(line[end:])
            lines.append("".join(proc))
        self._text = "".join(lines)
    
    def getWordsNeeded(self):
        """ Returns a list of the types of words requested by the story. Each
            entry in the list represents a unique substitution that has to be
            made.
        """
        visited = {}
        types = []
        for ref, value in self._subs:
            if ref == None or not ref in visited:
                visited[ref] = True
                types.append(value)
        return types
    
    def getStory(self, wordList):
        """ Returns the story after making the substitutions defined in the
            provided wordList.
        """
        solutions = []
        mapped = {}
        for ref, value in self._subs:
            if ref == None:
                solutions.append(wordList[0])
                wordList = wordList[1:]
            elif ref in mapped:
                solutions.append(mapped[ref])
            else:
                mapped[ref] = wordList[0]
                solutions.append(mapped[ref])
                wordList = wordList[1:]
        return self._text % tuple(solutions)

if __name__ == "__main__":
    import sys
    l = lib(sys.argv[1])
    needed = l.getWordsNeeded()
    answers = []
    for word in needed:
        answers.append(raw_input("%s: " % word))
    sys.stdout.write("\n%s" % l.getStory(answers))
    sys.exit(0)
