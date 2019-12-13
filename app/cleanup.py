import logging
import os


class Cleaner(object):
    def __init__(self):
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def cleanup(self):
        removed_files = []
        for file in self.files:
            try:
                os.remove(file)
                removed_files.append(file)
            except Exception as e:
                logging.error(e)

        for file in removed_files:
            self.files.remove(file)

        return removed_files
