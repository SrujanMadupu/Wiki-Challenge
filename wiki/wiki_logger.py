import logging

log_wiki = logging.getLogger(__name__)

f_handler = logging.FileHandler('wiki.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(f_format)

log_wiki.addHandler(f_handler)
