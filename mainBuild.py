# Zachary
# Imports
import json
import sys
import operator
import os
from collections import Counter
import re
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QTreeWidget, \
    QTreeWidgetItem, QTextEdit, QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

# Global defines
PUNCTUATION = '''!()-[]{};:'"\,<>./?@#$%^&*_~—”’'''
NUMBERS = '1234567890'
sample_text = "Hello this is sample text."
sample_oe = "& æfter geearnunge his geleafan þæt heo heora feond oferswiðdon & sige ahton. In þære gebedstowe æfter " \
            "þon monig mægen & hælo tacen gefremed wæron to tacnunge & to gemynde þæs cyninges geleafan. Ond monige " \
            "gen to dæge of þæm treo þæs halgan Cristes mæles sponas & scefþon neomað & þa in wæter sendað & þæt " \
            "wæþer on adlige men oððe on neat stregdað oðþe drincan syllað & heo sona hælo onfoð. Is seo stow on " \
            "Englisc genemned Heofenfeld. Wæs geo geara swa nemned fore-tacnunge ðæra toweardan wundra, forðon þe þær " \
            "þæt heofonlice sigebeacen aræred beon scolde, & þær heofonlic sige þam cinge seald wæs & þær gen to dæge " \
            "heofonlic wundor mærsode beoð. "
sample_oe2 = "þær þa halgan martyras licgað in heora lichaman, nis nænig tweo þæt hi magon manige fortacnu æteowian & " \
             "hi eac swa doð & hi cyðað unarimedlice wundru þam þe hie secað mid clænum mode. Ac forþon hit mag beon " \
             "tweod fram tyddrum & unstrangum modum, hwæþer hi syn þe ne syn þær andwearde us is to gehyrenne, " \
             "þær hit cuþ is þæt hi ne beoð na self on heora lichaman ac þær is nydþearf þæt hi æteowian maran " \
             "wundru, þær þæt tydre mod tweoð be heora andweardnesse; "
sample_oe3 = "Se wisa wer timbrode his hus ofer stan. Þa com þær micel flod, and þær bleowon windas, and ahruron on " \
             "þæt hus, and hit ne feoll: soþlice, hit wæs ofer stan getimbrod. Þa timbrode se dysiga wer his hus ofer " \
             "sandceosol. Þa rinde hit, and þær com flod, and bleowon windas, and ahruron on þæt hus, and þæt hus " \
             "feoll; and his hryre wæs micel. "
sample_oe4 = "God cwæþ to Abrahame: 'Nim þinne sunu Isaac, and far to þæm dunum, and geoffra hine þær uppan dune.'Þa " \
             "aras Abraham on Þære nihte, and ferde mid twæm cnapum to þæm dunum, and Isaac samod.  Hie ridon on " \
             "assum.  Þa on þone þriddan dæg, þa hie þa dune gesawon, þa cwæþ Abraham to þæm twæm cnapum þus: " \
             "'Andbidiaþ eow her mid þæm assum!' Isaac bær þone wudu to þære stowe, and Abraham bær his sweord and " \
             "fyr.  Isaac þa ascode Abraham his fæder: 'Fæder min, hwær is seo offrung?  Her is wudu.'  Se fæder " \
             "cwæþ: 'God foresceawaþ, min sunu, him self þa offrunge.' Þ a comon hie to þære stowe; and he þær weofod " \
             "arærde on þa ealdan wisan. Þa band he his sunu, and his sweord ateah. þa he wolde þæt weorc beginnan, " \
             "þa clipode Godes engel arodlice of heofonum: 'Abraham!'  He andswarode sona.  Se engel him cwæþ to: 'Ne " \
             "acwele þu þæt cild!' Þa geseah Abraham ramm betwix þæm bremlum; and he ahof þone ramm to þære offrunge. "


# Classes
# GUI Class
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle('Old English Analyzer')
        self.setFixedSize(self.size())
        cwd_gui = os.getcwd()
        cwd_gui = cwd_gui + "\AuthorProfiles"

        # For auto complete help
        # input = QPlainTextEdit()
        # input.
        # tree = QTreeWidget()
        # output = QTextEdit()
        # spinbox = QSpinBox()
        # freqspinbox = QDoubleSpinBox()
        tree_list = get_tree_dict(cwd_gui)
        for key, value in tree_list.items():
            root = QTreeWidgetItem(self.tree, [key])
            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)
        self.tree.expandAll()
        self.tree.show()

        self.pushButtonInput.clicked.connect(self.output_answer_input)
        self.pushButtonFolder.clicked.connect(self.output_answer_folder)

    def output_answer_input(self):
        ngram_length = self.spinBox.value()
        min_freq = self.doubleSpinBox.value()
        # print(min_freq)
        # print(ngram_length)
        input_text = self.input.toPlainText()
        input_text = input_text.strip()
        input_text = input_text.replace('\n', '')
        input_text = text_clean(input_text)
        #print(input_text)
        profile_dict = get_profiles_dict(cwd)
        output = compare_string_to_profiles(input_text, profile_dict, ngram_length, min_freq)
        self.output.setText('Sorted List: \n {0}'.format(json.dumps(output, indent=4)))

    def output_answer_folder(self):
        self.output.setText('')
        ngram_length = self.spinBox.value()
        min_freq = self.doubleSpinBox.value()
        cwd_tmp = os.getcwd()
        cwd_tmp = cwd_tmp + "\TestFolder"
        for filename in os.listdir(cwd_tmp):
            # print(filename)
            file = os.path.join(cwd_tmp, filename)
            input_text = read_file_to_string(file)
            input_text = input_text.strip()
            input_text = input_text.replace('\n', '')
            input_text = text_clean(input_text)
            #print(input_text)
            profile_dict = get_profiles_dict(cwd)
            output = compare_string_to_profiles(input_text, profile_dict, ngram_length, min_freq)
            self.output.append('List for: ' + filename)
            self.output.append('Sorted List: \n {0}'.format(json.dumps(output, indent=4)))


# Helper functions
def add_values_in_dict(sample_dict, key, list_of_values):
    # Append multiple values to a key in the given dictionary
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict


def get_tree_dict(path):
    tree_profile_dict = {}
    for filename in os.listdir(path):
        # print(filename)
        file = os.path.join(path, filename)
        # checking if it is a dir
        if os.path.isdir(file):
            # print(file)
            for filename2 in os.listdir(file):
                # print(filename2)
                add_values_in_dict(tree_profile_dict, filename, [filename2])
                # file2 = os.path.join(file, filename2)
                # print(file2)
    # print(profile_dict)
    return tree_profile_dict


# Frequency of a word
def find_frequency_of_word_in_text(target_word, text):
    text = re.split('\s+', text)
    c = Counter(text)
    total_count = sum(c.values())
    relative = {}
    for key in c:
        relative[key] = c[key] / total_count
    # print(relative)
    return relative


# Read text file to string
def read_file_to_string(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        string = file.read().replace('\n', '')
        string = string.strip()
        # string = string.replace('Ã°', 'ð')
        # string = string.replace('Ã†', 'Æ')
        # string = string.replace('Ã¦', 'æ')
    return string


# Splits text on the nth character
def split_text_by_nth_chars(text, n):
    output = [text[i:i + n] for i in range(0, len(text), n)]
    return output


# Helper function to clean text
def text_clean(text, ignore_spaces=True, ignore_punctuation=True, ignore_numbers=True):
    # Check for is spaces are being ignored
    if ignore_spaces:
        text = text.replace(" ", "")
    # Removing punctuations in string
    # Using loop + punctuation string
    if ignore_punctuation:
        for char in text:
            if char in PUNCTUATION:
                text = text.replace(char, "")
    if ignore_numbers:
        for char in text:
            if char in NUMBERS:
                text = text.replace(char, "")
    return text


# Helper function for n gram
def analyze_freq(text, number_of_chars, ignore_spaces=True, ignore_punctuation=True, find_frequency=True,
                 ignore_numbers=True, word_profile_analysis=False):
    text = text_clean(text, ignore_spaces, ignore_punctuation, ignore_numbers)
    if word_profile_analysis:
        text = text.split()
    else:
        text = split_text_by_nth_chars(text, number_of_chars)
    # Dictionary to store results
    dictionary = {}
    for chars in text:
        if chars not in dictionary.keys():
            dictionary[chars] = 0
        dictionary[chars] += 1
    # Sort by value in descending order
    sorted_dictionary = dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True))
    # print(sorted_dictionary)
    if find_frequency:
        total_count = 0
        for key, value in sorted_dictionary.items():
            total_count += value
        for key, value in sorted_dictionary.items():
            sorted_dictionary[key] = value / total_count
    return sorted_dictionary


# Main helper function for n gram analysis
def ngram_analyzer(text, text2, ngram_length, ignore_spaces=True, ignore_punctuation=True, ignore_numbers=True,
                   min_frequency=0.000000, word_profile_analysis=False):
    dict1 = analyze_freq(text, ngram_length, ignore_spaces, ignore_punctuation, True, ignore_numbers,
                         word_profile_analysis)
    total = 0
    for key, value in dict1.items():
        total += value
    # print(dict1)
    # print(total)
    dict2 = analyze_freq(text2, ngram_length, ignore_spaces, ignore_punctuation)
    total = 0
    for key, value in dict2.items():
        total += value
    # print(dict2)
    # print(total)
    list_dicts = [dict1, dict2]
    combined = dict.fromkeys(set().union(*list_dicts), 0)
    combined = ([dict(combined, **d) for d in list_dicts])
    list_dicts = [combined[0], combined[1]]
    to_be_popped = []
    # MIN freq REMOVAL
    for ngram, frequency in list_dicts[0].items():
        f1 = frequency  # ngram frequency from first profile
        if f1 < min_frequency:
            to_be_popped.append(ngram)
        else:
            f2 = list_dicts[1].get(ngram, 0)  # ngram frequency from second profile
            if f2 < min_frequency:
                to_be_popped.append(ngram)
    ###
    for ngram in to_be_popped:
        list_dicts[0].pop(ngram)
        list_dicts[1].pop(ngram)
    ####################
    # print(list_dicts)
    dis_sim_sum = 0.0
    for ngram, frequency in list_dicts[0].items():
        f1 = frequency  # ngram frequency from first profile
        f2 = list_dicts[1].get(ngram, 0)  # ngram frequency from second profile
        # print(f2)
        dis_sim_sum = dis_sim_sum + pow((2.0 * (f1 - f2) / (f1 + f2)), 2)
    # print(dis_sim_sum)
    return dis_sim_sum


# Main helper function to walk through directory and build profiles
def get_profiles_dict(path):
    # for subdir, dirs, files in os.walk(cwd):
    #     for file in files:
    #         #print(os.path.join(subdir, file))
    #         print(subdir)
    #         print(files)
    profile_dict = {}
    # profile_dict["Test"] = "Hello there"
    for filename in os.listdir(path):
        temp_str = ""
        # print(filename)
        file = os.path.join(path, filename)
        # checking if it is a dir
        if os.path.isdir(file):
            # print(file)
            for filename2 in os.listdir(file):
                file2 = os.path.join(file, filename2)
                # print(file2)
                if os.path.isfile(file2):
                    temp_str = temp_str + " " + read_file_to_string(file2)
                    # print(temp_str)
        profile_dict[filename] = temp_str
    # print(profile_dict)
    return profile_dict


def compare_string_to_profiles(string, profiles, ngram_length=2, min_frequency=0.00000):
    result_dict = {}
    for profile in profiles:
        result_dict[profile] = ngram_analyzer(string, profiles.get(profile), ngram_length, True, True, True,
                                              min_frequency)
    # sort_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=False)
    sorted_dict = {}
    sorted_keys = sorted(result_dict, key=result_dict.get)
    for item in sorted_keys:
        sorted_dict[item] = result_dict[item]
    # print(sorted_dict)
    return sorted_dict


# TODO
# Create common n-gram list based being in at least a certain number of texts. (new function probably, ran before
# | maybe unnecessary)
# Minimum cutoff value for ngrams (Think its basically done)
# Look at certain number of top frequent ngrams
# More tests - look at grieves and kessel - (Positional word frequency) | 1st word in sentence
# Some GUI (Mainly done)
# Fix capitalization --
if __name__ == '__main__':
    cwd = os.getcwd()
    # print("Current Directory:", cwd)
    cwd = cwd + "\AuthorProfiles"
    # print("Current Directory:", cwd)

    # Main Program

    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
