# #src/book.py
import os
import sys
from json import dump, load
from pprint import pprint

from dotenv import load_dotenv
from mongoengine import Document, connect
from mongoengine.fields import IntField, ListField, StringField, UUIDField
from pymongo import MongoClient
from tqdm.auto import tqdm


from src.atlas import max_title, sg
from src.log import BASE, console, log

# . ##########################################. #
# .                                           . #
# .                                           . #
# .                                           . #
# .  888                          888         . #
# .  888 88e   e88 88e   e88 88e  888 ee      . #
# .  888 888b d888 888b d888 888b 888 P       . #
# .  888 888P Y888 888P Y888 888P 888 b       . #
# .  888 88"   "88 88"   "88 88"  888 8b      . #
# .                                           . #
# .                                           . #
# .                                           . #
# . ##########################################. #


class Book (Document):
    title = StringField(required=True, max_length=500)
    output = StringField()
    cover = StringField()
    cover_path = StringField()
    uuid = UUIDField(binary=False)
    default = StringField()
    start = IntField(min_value=1)
    end = IntField(max_value=3463)
    book = IntField()
    book_word = StringField(required=True)


# > Declaring Static Variables
written: str = "Written by Twelve Winged Burning Seraphim"
edited: str = "Complied and Edited by Max Ludden"
TEXT = f'<p class="title">{written}</p>\n<p class="title">{edited}</p>'

def generate_output_file(book: int):
    book_result = books.find_one({'book':book}) # type: ignore
    pprint(book_result)
    output = book_result['output']
    return output


def get_output_file(book: int):
    sg()
    for doc in Book.objects(book=book): # type: ignore
        print(doc.output)
        return doc.output
