#!/usr/bin/env python3

#
# Copyright (c) 2023 Marc POULHIÈS
#

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse

from opensmtpd import FilterServer

target_tag = '+'
other_tags = '-'


def start():
    parser = argparse.ArgumentParser(
        description='Rewrite RCPT TO using extra tag to use a single tag')
    parser.add_argument('target_tag', help='TAG character to use')
    parser.add_argument('other_tags', help='String of TAG characters')
    args = parser.parse_args()

    global target_tag
    global other_tags

    target_tag = args.target_tag
    other_tags = args.other_tags

    server = FilterServer()
    server.register_handler('filter', 'rcpt-to', convert_tag)
    server.serve_forever()


def convert_tag(session, s):
    f = list(filter(lambda x: x != -1,
                    map(lambda x: s.find(x),
                        list(other_tags + target_tag))))
    if f:
        m = min(f)
        c = list(s)
        c[m] = target_tag
        return "rewrite|<{}>".format("".join(c))
    else:
        return "proceed"


if __name__ == '__main__':
    start()
