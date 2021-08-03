#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from shell import nmcli


DOCUMENTATION = '''
---
module: nmcli
short_description: Pythonification of nmcli wrapper
description:
    - Execute nmcli command to gather information about network manager
      devices.
'''

__all__ = ["nm", "dev", "con"]


class NMCommand(object):
    def __init__(self, cmdname, commands):
        self.cmdname = cmdname
        for command, possibleargs in commands:
            setattr(self, command, self.gen_action(command, possibleargs))

    def gen_action(self, command, possibleargs):
        def sanitize_args(args):
            def sanitize_arg(arg):
                if isinstance(arg, bool):
                    return str(arg).lower()

                if isinstance(arg, int):
                    return str(arg)

                if arg is not None:
                    return arg.lower()

                return arg

            if isinstance(args, list):
                newargs = []
                for arg in args:
                    newargs.append(sanitize_arg(arg))
                return newargs
            else:
                return sanitize_arg(args)

        usableargs = sanitize_args(possibleargs)

        def verify_arg(arg):
            arg = sanitize_args(arg)
            if arg not in usableargs:
                raise Exception(
                    "%s is not a valid argument for '%s'. Parameters: %s" % (
                        arg, command, possibleargs))
            return arg

        def verify_args(args):
            return [verify_arg(arg) for arg in args]

        def run_action(args=None, **kwargs):
            if args is None:
                args = []

            if not isinstance(args, list):
                args = [args]

            if kwargs:
                args.extend(kwargs.keys())

            args = verify_args(args)

            if not args:
                cmd = command
            else:
                opts = []
                for arg in args:
                    if arg not in kwargs:
                        opts.append(arg)
                    else:
                        opts.append("%s %s" % (
                                arg,
                                sanitize_args(kwargs[arg])))
                cmd = "%s %s" % (command,
                                 ' '.join(opts))

            return nmcli(self.cmdname,
                         command=cmd)

        return run_action


# @TODO: I'm sure there is a way to introspect all of this from
# nmcli itself.  I don't feel like doing the text parsing
# right now though.
nm = NMCommand(
        "nm",
        [("status", None),
         ("enable", [True, False]),
         ("sleep", [True, False]),
         ("wifi", ["on", "off"]),
         ("wwan", ["on", "off"])]
        )

con = NMCommand(
    "con",
    [("list", [None, "id", "uuid"]),
     ("status", [None, "id", "uuid", "path"]),
     ("up", ["id", "uuid", "iface", "ap"]),
     ("down", ["id", "uuid"]),
     ("delete", ["id", "uuid"]),
    ])


dev = NMCommand(
    "dev",
    [("status", None),
     ("list", [None, "iface"]),
     ("disconnect", ["iface"]),
     ("wifi", ["list"]),
    ])


if __name__ == '__main__':
    print nm.status()
    print nm.enable(True)

    try:
        print con.list(food=8302)
        print "BAD!"
    except:
        pass

    try:
        print nm.enable("asdasd")
        print "BAD!"
    except:
        pass
