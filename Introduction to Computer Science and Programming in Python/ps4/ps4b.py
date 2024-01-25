# Problem Set 4B
# Name: Angel Cruz
# Collaborators: None
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = None

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        
        copy_valid_words = self.valid_words
        return copy_valid_words


    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lowercaseLetters = 2*string.ascii_lowercase
        uppercaseLetters = 2*string.ascii_uppercase
       
        dict_letters_mapped = {}
       
        for i in range(len(string.ascii_lowercase)):
            dict_letters_mapped[string.ascii_lowercase[i]] = lowercaseLetters[i+shift]
           
        for j in range(len(string.ascii_uppercase)):
            dict_letters_mapped[string.ascii_uppercase[j]] = uppercaseLetters[j+shift]       
            
        return dict_letters_mapped
       
           

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        shift_message =''
        
        for c in self.message_text:
            shift_message += (shift_dict.get(c, c))
            
        return shift_message
        
        

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        
        


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift = 1
        max_valid_words = 0
        best_shift_text =''
        for s in range(0, 26):
            shift_text = self.apply_shift(s)
            shift_text_list = shift_text.split()
            valid_words_count = 0
            for w in shift_text_list:
                if is_word(self.valid_words, w):
                    valid_words_count+=1
            
            if valid_words_count > max_valid_words:
                max_valid_words = valid_words_count
                best_shift = s
                best_shift_text = shift_text
        
        return (best_shift, best_shift_text)
            
            

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

     #Example test case (PlaintextMessage)
     message1 = 'I am so happy to be here!'
     plaintext = PlaintextMessage(message1, 1)
     print('Input: ', message1)
     print('Expected Output: J bn tp ibqqz up cf ifsf!')
     print('Actual Output:', plaintext.get_message_text_encrypted())
     print('\n')
     
     message2 = 'NEW YORK is a great... "lovely" place.'
     plaintext = PlaintextMessage(message2, 3)
     print('Input: ', message2)
     print('Expected Output: QHZ BRUN lv d juhdw... "oryhob" sodfh.')
     print('Actual Output:', plaintext.get_message_text_encrypted())
     print('\n')
    
    
    
    
     #Example test case (CiphertextMessage)
     message3 = 'J bn tp ibqqz up cf ifsf!'
     ciphertext = CiphertextMessage(message3)
     print('Input: ', message3)
     print('Expected Output:', (25, message1))
     print('Actual Output:', ciphertext.decrypt_message())
     print('\n')
     
     message4 = 'QHZ BRUN lv d juhdw... "oryhob" sodfh.'
     ciphertext = CiphertextMessage(message4)
     print('Input: ', message4)
     print('Expected Output:', (23, message2))
     print('Actual Output:', ciphertext.decrypt_message())
     print('\n____________________________________________\n')



     #TODO: best shift value and unencrypted story
     encrypted_story = get_story_string()
     decrypted_story = CiphertextMessage(encrypted_story)
     print('Input: ', encrypted_story, '\n')
     print('Output: ', decrypted_story.decrypt_message())

