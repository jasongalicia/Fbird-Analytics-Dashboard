from crypto import Encrypt
from analysis import Analysis
import datetime
import os

print('Beginning Testing Phases...............................................')
print('')
# Basic test first

print('Phase 1...')
text_to_encrypt = 'starwars'
crypto = Encrypt(text_to_encrypt)
salt = crypto.get_salt()

print('WORD: '+ str(text_to_encrypt))

hash_no_salt = crypto.get_hash(text_to_encrypt)
hash_with_salt = crypto.get_hashed_salt()

print('Salt: ' + str(salt))
print('Hash w/ No Salt: ' + str(hash_no_salt))
print('Hash w/ Salt: ' + str(hash_with_salt))
print('')

# Random list of words for the next part of Password/Hashing/Salt Testing
print('Phase 2...')
print('')
list_words = ['sunglasses', 'asusmax' ,'starwars', 'football', 'basketball',
'soccerball', 'dodgeball', 'kickball', 'specifications', 'sadfsadf', 'speak']

for word in list_words:
    list_word = word
    cryption = Encrypt(list_word)
    salty = cryption.get_salt()

    print('WORD: '+ str(list_word))

    hashed_no_salt = cryption.get_hash(list_word)
    hashed_with_salt = cryption.get_hashed_salt()

    print('Salt: ' + str(salty))
    print('Hash w/ No Salt: ' + str(hashed_no_salt))
    print('Hash w/ Salt: ' + str(hashed_with_salt))
    print('')

print('Ending Testing Phases..................................................')

x = str(datetime.datetime.now())
y = x.split()
date = y[0]
