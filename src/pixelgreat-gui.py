#!/usr/bin/env python3

# ---- IMPORTS ----

import sys
import argparse
from enum import Enum

import helpers
import constants


# ---- MAIN CLASSES ----


# Main class
class Python3Template:
    def __init__(self,
                 first,
                 second=None,
                 opcode=None
                 ):
        self.first = first

        if second is None:
            self.second = constants.DEFAULTS["second"]
        else:
            self.second = second

        if opcode is None:
            self.opcode = constants.DEFAULTS["opcode"]
        else:
            if opcode not in constants.OpCode:
                raise ValueError("The operation code must is not valid!")
            if opcode == constants.OpCode.DIV and self.second == 0:
                raise ValueError("Cannot divide by zero!")
            self.opcode = opcode

    def add(self):
        return self.first + self.second

    def sub(self):
        return self.first - self.second

    def mult(self):
        return self.first * self.second

    def div(self):
        return self.first / self.second

    def operate(self):
        if self.opcode == constants.OpCode.ADD:
            eq_string = f"{self.first} + {self.second}"
            value = self.add()
        elif self.opcode == constants.OpCode.SUB:
            eq_string = f"{self.first} - {self.second}"
            value = self.sub()
        elif self.opcode == constants.OpCode.MULT:
            eq_string = f"{self.first} * {self.second}"
            value = self.mult()
        elif self.opcode == constants.OpCode.DIV:
            eq_string = f"{self.first} / {self.second}"
            value = self.div()
        else:
            raise ValueError(f"Invalid opcode: \"{self.opcode}\"")

        result = {
            "value": value,
            "equation": eq_string
        }

        return result

# ---- PROGRAM EXECUTION ----


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description=f"{constants.DESCRIPTION}\n\n"
                    f"Valid parameters are shown in {{braces}}\n"
                    f"Default parameters are shown in [brackets].",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-1", "--first", dest="first_arg", type=float, required=True,
                        help="the first argument"
                        )

    parser.add_argument("-2", "--second", dest="second_arg", type=float, required=False,
                        default=None,
                        help="the second argument [{default}]".format(
                            default=constants.DEFAULTS["second"])
                        )

    parser.add_argument("-o", "--operation", dest="opcode", type=str, required=False,
                        default=None,
                        help="the operation to perform on the arguments {{{values}}} [{default}]".format(
                            values=", ".join([x.value for x in constants.OpCode]),
                            default=constants.DEFAULTS["opcode"].value)
                        )

    parsed_args = parser.parse_args()

    # Interpret string arguments
    if parsed_args.opcode is None:
        parsed_args.opcode = constants.DEFAULTS["opcode"]
    else:
        if parsed_args.opcode in [x.value for x in constants.OpCode]:
            parsed_args.opcode = constants.OpCode(parsed_args.opcode)
        else:
            parser.error(f"\"{parsed_args.opcode}\" is not a valid opcode")

    # Set remaining defaults
    if parsed_args.second_arg is None:
        parsed_args.second_arg = constants.DEFAULTS["second"]

    return parsed_args


def main():
    args = parse_args()

    python_3_template = Python3Template(
        first=args.first_arg,
        second=args.second_arg,
        opcode=args.opcode)

    result = python_3_template.operate()

    print("{eq} = {val}".format(
        eq=result["equation"],
        val=result["value"])
    )


if __name__ == "__main__":
    main()
