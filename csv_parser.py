#!/usr/bin/env python3
# BSD 3-Clause License
#
# Copyright (c) 2022, Iain Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import List, Iterator, Dict


class CSVException(Exception):
    pass


class CSV:
    QUOTE_CHAR = '"'
    COMMA_CHAR = ","
    NEWLINE_CHAR = "\n"
    CARRIAGE_RETURN_CHAR = "\r"

    def __init__(self, input: Iterator[str]):
        self.headers, self.rows = CSV.__parse_lines(input)
        if self.rows:
            header_count = len(self.headers)
            row_field_count = min(len(row) for row in self.rows)
            if header_count != row_field_count:
                raise CSVException(f"{row_field_count} values in row, expected {header_count}")

    def __str__(self):
        output = [",".join(self.headers)]
        output.extend(",".join(row) for row in self.rows)
        return "\n".join(output)

    def __header_index(self, header: str) -> int:
        index = 0
        for i in range(len(self.headers)):
            if self.headers[i] == header or f'"{header}"' == self.headers[i]:
                index = i
        return index

    def dict_rows(self) -> Iterator[Dict[str,str]]:
        for row in self.rows:
            dict_row = {}
            for index, header in enumerate(self.headers):
                dict_row[header] = row[index]
            yield dict_row

    def sort(self, header: str, case_sensitive: bool = False):
        index = self.__header_index(header)
        if case_sensitive:
            self.rows.sort(key=lambda row: row[index].casefold(), reverse=True)
        else:
            self.rows.sort(key=lambda row: row[index], reverse=True)

    def sorted(self, header: str, case_sensitive: bool = False):
        index = self.__header_index(header)
        if case_sensitive:
            return sorted(self.rows, key=lambda row: row[index].strip('"').casefold(), reverse=True)
        return sorted(self.rows, key=lambda row: row[index].strip('"'), reverse=True)

    @classmethod
    def __parse_line(cls, line: str) -> (List[str], bool):
        """
        Parses a line to turn it into a list of fields
        :param line: The line to be parsed
        :return: an list of field values and boolean indicating if there is an unclosed double quote
        """
        if CSV.QUOTE_CHAR in line:
            i = 0
            field_start = 0
            quoted = False
            fields = []
            line_length = len(line)
            while i < line_length:  # looking for " and ,
                if line[i] == CSV.QUOTE_CHAR:
                    if quoted:
                        try:
                            if line[i+1] == CSV.QUOTE_CHAR:
                                i = i + 1  # walk forward an extra character, we've already looked at this character
                            else:
                                quoted = False
                        except IndexError:
                            quoted = False  # End of the line closing quote
                    elif i == field_start:  # Check for quotes at the start of a field
                        quoted = True
                    else:
                        raise CSVException('" must wrap an entire field or be escaped("") inside a quoted field')
                elif not quoted:
                    if line[i] == CSV.COMMA_CHAR:
                        fields.append(line[field_start:i])
                        field_start = i + 1
                i = i + 1
            fields.append(line[field_start:i])  # cut the field out of the line
            return fields, quoted
        else:
            return line.split(CSV.COMMA_CHAR), False

    @classmethod
    def __parse_lines(cls, lines: Iterator[str]) -> (List[str], List[List[str]]):
        rows: List[List[str]] = []
        try:
            while True:
                row, dangling_quote = cls.__parse_line(next(lines).rstrip())
                while dangling_quote:
                    next_row, dangling_quote = cls.__parse_line(f'"{next(lines).rstrip()}')  # fudge a quote onto the next line and try to parse it
                    row[-1] = f"{row[-1]}\n{next_row.pop(0)[1:]}"  # stick the first field of the "next_row" onto the last field of the row, drop the leading quote
                    row.extend(next_row)
                rows.append(row)
        except StopIteration:
            # fun edge case: If there is an unclosed quote on the last line then it will not be included
            return rows.pop(0), rows  # Header is assumed to always exist


def main():
    import pathlib
    import sys
    try:
        if len(sys.argv) > 2:  # two arguments is definitely a file and a column
            csv = CSV(pathlib.Path(sys.argv[1]).open())
            column = sys.argv[2]
        else:
            csv = CSV(sys.stdin)  # 1 argument means that the CSV will come from STDIN
            column = sys.argv[1]
        if column:
            csv.sort(column)
        print(csv)
    except (BrokenPipeError, KeyboardInterrupt):  # in case we stop reading stdin
        pass


if __name__ == "__main__":
    main()
