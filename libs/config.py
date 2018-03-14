#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
import os

import configparser


class Config():
    def __init__(self):
        import configparser
        try:
            from SinDB.settings import BASE_DIR
        except:
            BASE_DIR = "../"
        self.conf = configparser.ConfigParser()
        self.config_path = os.path.join(BASE_DIR, "SinDB.conf")
        self.conf.read(self.config_path, encoding='utf-8')

    def set(self, section, key, value):
        self.conf.set(section, key, value)
        self.conf.write(open(self.config_path, 'w'))

    def get(self, section, key, default=None):
        try:
            value = self.conf.get(section, key)
        except  Exception as e:
            value = default
        return value

    def items(self, section):
        try:
            item_list = self.conf.items(section)
            new_list = []
            for item in item_list:
                new_value = item[1]
                new_list.append((item[0], new_value))
        except:
            new_list = []
        return new_list

    def remove_option(self, section, key):
        self.conf.remove_option(section, key)
        self.conf.write(open(self.config_path, 'w'))


def get_conf_items(section):
    conf = Config()
    return conf.items(section)





if __name__ == "__main__":
    # get_projects()
    db_type_choice = (get_conf_items('db_type'))
    print(db_type_choice)
    conf = Config()
    print(conf.items('mysql_version'))



