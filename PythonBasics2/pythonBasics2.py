# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.


# Part A (count_threes) now needs to return the multiple of three that occurs
# the most in a string. For example, 0939639 would return 9 since it appeared
# 3 times while the other multiple of three appeared less than that. You only
# need to worry about single digit multiples of 3 (3, 6, 9). You must use a
# dictionary to accomplish this.

def count_threes(n):
    count_three = n.count('3')
    count_six = n.count('6')
    count_nine = n.count('9')

    d = {3 : count_three, 6 : count_six, 9 : count_nine}

    return max(d, key = lambda k: d[k])


# Part B (longest_consecutive_repeating_char) now needs to account for the edge
# case where two characters have the same consecutive repeat length. The return
# value should now be a list containing all characters with the longest consecutive
# repeat. For example, the longest_consecutive_repeating_char('aabbccd') would return
# ['a', 'b', 'c'] (order doesn't matter). You must use a dictionary to accomplish this.
def longest_consecutive_repeating_char(s):
    last_char = ""
    curr_count, max_count = 0
    max_char = s[0]

    for c in s:
        if c == last_char:
            curr_count += 1
            if curr_count > max_count:
                max_count = curr_count
                max_char = c
        else:
            curr_count = 1
            last_char = c

    return max_char


# Part C. is_palindrome
# Define a function is_palindrome(s) that takes a string s
# and returns whether or not that string is a palindrome.
# A palindrome is a string that reads the same backwards and
# forwards. Treat capital letters the same as lowercase ones
# and ignore spaces (i.e. case insensitive).
def is_palindrome(s):
    # remove spaces from string and make lowercase
    new_s = (s.replace(" ", "")).lower()
    for i in range(len(new_s)//2):
         if new_s[i] != new_s[-1-i]:
                 return False
    return True
