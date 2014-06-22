#!/usr/bin/env python

# Name: wordsworth
# Description:  Frequency analysis tool
# Author: autonomoid
# Date: 2014-06-22
# Licence: GPLv3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# Font effects --> fancy console colours in bash
underline = "\x1b[1;4m"
black = "\x1b[1;30m"
red = "\x1b[1;31m"
green = "\x1b[1;32m"
yellow = "\x1b[1;33m"
blue = "\x1b[1;34m"
purple = "\x1b[1;35m"
turquoise = "\x1b[1;36m"
normal = "\x1b[0m"

previous_word = ''
previous_pair = ''
previous_triplet = ''
prev_punc = ''

word_stats = {
              'words': {},
              'word_pairs': {},
              'word_triplets': {},
              'word_quads': {},
              'total_chars': 0,
              'total_words': 0,
              'max_length': 0,
              'min_length': 999,
              'mean_length': -1,
              'common_words': [],
              'longest_word': '',
              'shortest_word': '',
              'char_counts': {
                              'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                              'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                              'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                              's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                              'y': 0.0, 'z': 0.0
                             },
              'char_percentages': {
                                   'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.0, 'f': 0.0,
                                   'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0, 'k': 0.0, 'l': 0.0,
                                   'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.0, 'r': 0.0,
                                   's': 0.0, 't': 0.0, 'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0,
                                   'y': 0.0, 'z': 0.0
                                  }
             }

##############################################################################

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Perform letter, word and n-tuple frequency analysis on text files.')
    parser.add_argument('--filename', '-f', dest='inputFile', required=True, help='Text file to parse.')
    args = parser.parse_args()
    
    # Read in all of the words in a file
    filename = args.inputFile
    f = open(filename, 'r')
    
    print "[+] Analysing '" + args.inputFile + "'"
    
    lines = f.readlines()
    for line in lines:
        words = line.split()
        for word in words:

            punc = ''

            #Clean the words up first
            if word.endswith('.'):
                word = word.replace('.', '')
                punc = '.'
            if word.endswith(','):
                word = word.replace(',', '')
                punc = ','
            if word.endswith(':'):
                word = word.replace(':', '')
                punc = ':'
            if word.endswith(';'):
                word = word.replace(';', '')
                punc = ';'
            if word.endswith('"'):
                word = word.replace('"', '')
                punc = '"'
            if word.endswith('?'):
                word = word.replace('?', '')
                punc = '?'
            if word.endswith('!'):
                word = word.replace('!', '')
                punc = '!'
            if word.endswith("'"):
                word = word.replace("'", '')
                punc = "'"
            if word.endswith('('):
                word = word.replace('(', '')
                punc = '('
            if word.endswith(')'):
                word = word.replace(')', '')
                punc = ')'
            word = word.replace(' ', '')
            word = word.lower()

    ##############################################################################

            length = len(word)
            if word == '': break

            # Record longest word length
            if length > word_stats['max_length']:
                word_stats['max_length'] = length
                word_stats['longest_word'] = word

            # Record shortest word length
            if length < word_stats['min_length']:
                word_stats['min_length'] = length
                word_stats['shortest_word'] = word

            # Record the word and its properties.
            if word in word_stats['words']:
                word_stats['words'][word]['count'] += 1.0
            else:
                word_stats['words'][word] = {
                                             'length': length,
                                             'count': 1
                                            }

            # Keep track of the total number of words and chars read.
            word_stats['total_chars'] += length
            word_stats['total_words'] += 1.0

            # Note the charaters in each word.
            for char in word:
                if char.lower() in word_stats['char_counts']:
                    word_stats['char_counts'][char.lower()] += 1.0

    ##############################################################################

            # Recod word-pairs
            word_pair = previous_word + prev_punc + ' ' + word + punc
            length = len(word_pair)

            if word_pair in word_stats['word_pairs']:
                word_stats['word_pairs'][word_pair]['count'] += 1.0
            else:
                if previous_word != '':
                    word_stats['word_pairs'][word_pair] = {
                                                           'length': length,
                                                           'count': 1
                                                          }

    ##############################################################################

            # Recod word-triplets
            word_triplet = previous_pair + prev_punc + ' ' + word + punc
            length = len(word_triplet)

            if word_triplet in word_stats['word_triplets']:
                word_stats['word_triplets'][word_triplet]['count'] += 1.0
            else:
                if previous_pair != '':
                    word_stats['word_triplets'][word_triplet] = {
                                                                 'length': length,
                                                                 'count': 1
                                                                }

    ##############################################################################

            # Recod word-quads
            word_quad = previous_triplet + prev_punc + ' ' + word + punc
            length = len(word_quad)

            if word_quad in word_stats['word_quads']:
                word_stats['word_quads'][word_quad]['count'] += 1.0
            else:
                if previous_triplet != '':
                    word_stats['word_quads'][word_quad] = {
                                                           'length': length,
                                                           'count': 1
                                                          }

    ##############################################################################

            previous_word = word
            previous_pair = word_pair
            previous_triplet = word_triplet
            prev_punc = punc

    ##############################################################################

    # Calculate the mean word length
    word_stats['mean_length'] = word_stats['total_chars'] / word_stats['total_words']

    # Calculate relative character frequencies
    for char in word_stats['char_counts']:
        char_count = word_stats['char_counts'][char]
        total_chars = word_stats['total_chars']
        percentage = 100.0 * (char_count / total_chars)
        word_stats['char_percentages'][char] = percentage

    ##############################################################################

    # Find the most common words
    top_words = sorted(word_stats['words'],
                       key=lambda x: (word_stats['words'][x]['count']),
                       reverse=True)

    # Find most common word pairs
    top_pairs = sorted(word_stats['word_pairs'],
                       key=lambda x: (word_stats['word_pairs'][x]['count']),
                       reverse=True)

    # Find most common word triplets
    top_triplets = sorted(word_stats['word_triplets'],
                       key=lambda x: (word_stats['word_triplets'][x]['count']),
                       reverse=True)

    # Find most common word quads
    top_quads = sorted(word_stats['word_quads'],
                       key=lambda x: (word_stats['word_quads'][x]['count']),
                       reverse=True)

    ##############################################################################

    # Print results
    out = open(filename.split('.')[0] + '-stats.txt', 'w')

    print '\n===' + blue + ' RESULTS ' + normal + '==='
    out.write('=== RESULTS ===\n')

    print 'File = ' + purple + str(filename) + normal
    out.write('File = ' + str(filename) + '\n')

    print ('Longest word = ' + purple + str(word_stats['longest_word']) + normal +
           ' (' + purple + str(word_stats['max_length']) + normal + ')')
    out.write('Longest word = ' + str(word_stats['longest_word']) +
           ' (' + str(word_stats['max_length']) + ')\n')

    print ('Shortest word = ' + purple + str(word_stats['shortest_word']) + normal +
           ' (' + purple + str(word_stats['min_length']) + normal + ')')
    out.write('Shortest word = ' + str(word_stats['shortest_word']) +
           ' (' + str(word_stats['min_length']) + ')\n')

    print ('Mean word length /chars = ' + purple + str(word_stats['mean_length']) +
            normal)
    out.write('Mean word length /chars = ' + str(word_stats['mean_length']) + '\n')

    print ('Total words parsed = ' + purple +
            str(word_stats['total_words']).split('.')[0] + normal)
    out.write('Total words parsed = ' +
            str(word_stats['total_words']).split('.')[0] + '\n')

    print ('Total chars parsed = ' + purple + str(word_stats['total_chars']) +
            normal)
    out.write('Total chars parsed = ' + str(word_stats['total_chars']) + '\n')

    ##############################################################################

    print '\n===' + blue + ' Commonest words ' + normal + '==='
    out.write('\n=== Commonest words ===\n')

    limit = 50
    if len(top_words) < 50:
        limit = len(top_words)

    for i in range(0, limit):
        word = top_words[i]
        count = word_stats['words'][word]['count']
        perc = 100.0 * (count / word_stats['total_words'])
        print (str(i + 1) + ' = ' + purple + word +
               normal + ' (' + purple + str(count).split('.')[0] + normal +
               ' = ' + purple + str(perc)[:5] + '%' + normal + ')')
        out.write(str(i + 1) + ' = ' + word + ' (' + str(count).split('.')[0] +
               ' = ' + str(perc)[:5] + '%)\n')

    ##############################################################################

    print '\n===' + blue + ' Commonest word-pairs ' + normal + '==='
    out.write('\n=== Commonest word-pairs ===\n')

    limit = 50
    if len(top_pairs) < 50:
        limit = len(top_pairs)

    for i in range(0, limit):
        word_pair = top_pairs[i]
        count = word_stats['word_pairs'][word_pair]['count']
        perc = 100.0 * (count / len(word_stats['word_pairs']))
        print (str(i + 1) + ' = ' + purple + word_pair +
               normal + ' (' + purple + str(count).split('.')[0] + normal + ' = ' +
               purple + str(perc)[:4] + '%' + normal + ')')
        out.write(str(i + 1) + ' = ' + word_pair + ' (' +
                  str(count).split('.')[0] + ' = ' + str(perc)[:4] + '%)\n')

    ##############################################################################

    print '\n===' + blue + ' Commonest word-triplets ' + normal + '==='
    out.write('\n=== Commonest word-triplets ===\n')

    limit = 50
    if len(top_triplets) < 50:
        limit = len(top_triplets)

    for i in range(0, limit):
        word_triplet = top_triplets[i]
        count = word_stats['word_triplets'][word_triplet]['count']
        perc = 100.0 * (count / len(word_stats['word_triplets']))
        print (str(i + 1) + ' = ' + purple + word_triplet +
               normal + ' (' + purple + str(count).split('.')[0] + normal + ' = ' +
               purple + str(perc)[:5] + '%' + normal + ')')
        out.write(str(i + 1) + ' = ' + word_triplet + ' (' +
                str(count).split('.')[0] + ' = ' + str(perc)[:5] + '%)\n')

    ##############################################################################

    print '\n===' + blue + ' Commonest word-quads ' + normal + '==='
    out.write('\n=== Commonest word-quads ===\n')

    limit = 50
    if len(top_quads) < 50:
        limit = len(top_quads)

    for i in range(0, limit):
        word_quad = top_quads[i]
        count = word_stats['word_quads'][word_quad]['count']
        perc = 100.0 * (count / len(word_stats['word_quads']))
        print (str(i + 1) + ' = ' + purple + word_quad +
               normal + ' (' + purple + str(count).split('.')[0] + normal + ' = ' +
               purple + str(perc)[:5] + '%' + normal + ')')
        out.write(str(i + 1) + ' = ' + word_quad + ' (' +
                str(count).split('.')[0] + ' = ' + str(perc)[:5] + '%)\n')

    ##############################################################################

    total_dev = 0.0

    print '\n===' + blue + ' FREQUENCY ANALYSIS ' + normal + '==='
    out.write('\n=== FREQUENCY ANALYSIS ===\n')
    for char in sorted(word_stats['char_percentages'].iterkeys()):
        bar = ''
        perc = word_stats['char_percentages'][char]

        # Percentage deviation from random distribution of characters.
        dev = 100.0 * (abs((100.0 / 26.0) - perc) / (100.0 / 26.0))
        total_dev += dev

        for i in range(0, int(perc)):
            bar += '#'
        print (char + ' |' + red + bar + normal + ' ' + str(perc)[:4] +
                '% (' + str(dev)[:4] + '% deviation from random)')
        out.write(char + ' |' + bar + ' ' + str(perc)[:4] + '% (' +
                str(dev)[:4] + '% deviation from random)\n')

    print ('\nTotal percentage deviation from random = ' +
            str(total_dev).split('.')[0] + '%')
    out.write('\nTotal percentage deviation from random = ' +
            str(total_dev).split('.')[0] + '%')

    average_dev = total_dev / 26.0
    print ('Average percentage deviation from random = ' +
            str(average_dev)[:4] + '%')
    out.write('\nAverage percentage deviation from random = ' +
              str(average_dev)[:4] + '%')

    ##############################################################################

    print '\nWritten results to ' + filename.split('.')[0] + '-stats.txt\n'
    out.close()
