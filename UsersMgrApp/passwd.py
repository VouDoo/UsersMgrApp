#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All libs are part of standard distribution for python 3
from random import SystemRandom, shuffle
from passlib.hash import sha512_crypt as crypt
import string


# Important: recommanded to set size to 8 at least
def generate_secure_word(size=20):
    """
    Generate secure word by using letters, digits and special characters

    :param size:
    :return:
    """
    passwd_list = list()

    for i in range(size // 4):
        passwd_list.append(SystemRandom().choice(string.ascii_lowercase))
        passwd_list.append(SystemRandom().choice(string.ascii_uppercase))
        passwd_list.append(SystemRandom().choice(string.punctuation))
        passwd_list.append(SystemRandom().choice(string.digits))
    for i in range(size - len(passwd_list)):
        passwd_list.append(SystemRandom().choice(string.ascii_letters))

    shuffle(passwd_list)
    passwd_string = "".join(passwd_list)

    return passwd_string


def hash_word(word):
    """
    Hash word by using hashing algorithm

    :param word:
    :return:
    """
    return crypt.hash(word)


def verify_hash(plain_word, hashed_word):
    """
    Verify plain word hash with hashed word

    :param plain_word:
    :param hashed_word:
    :return:
    """
    return crypt.verify(plain_word, hashed_word)
