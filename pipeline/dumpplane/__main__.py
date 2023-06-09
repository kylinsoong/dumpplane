#!/usr/bin/python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from traceback import format_exception

from . import __version__
from .split import split as split_exec
from .dump import dump as dump_exec


def split(filename, out):
    split_exec(filename, out, True)

def dump(filename, input, out, db, table):
    dump_exec(filename, input, out, db, table)


class _SubparserHelpFormatter(RawDescriptionHelpFormatter):
    def _format_action(self, action):
        line = super(RawDescriptionHelpFormatter, self)._format_action(action)

        if action.nargs == 'A...':
            line = line.split('\n', 1)[-1]

        if line.startswith('    ') and line[4] != ' ':
            parts = filter(len, line.lstrip().partition(' '))
            line = '  ' + ' '.join(parts)

        return line

def parse_args(args=None):
    parser = ArgumentParser(
        formatter_class=_SubparserHelpFormatter,
        description='various operations for nginx config files',
        usage='%(prog)s <command> [options]'
    )
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title='commands')

    def create_subparser(function, help):
        name = function.__name__
        prog = 'dumpplane ' + name
        p = subparsers.add_parser(name, prog=prog, help=help, description=help)
        p.set_defaults(_subcommand=function)
        return p

    p = create_subparser(split, 'split a nginx dump(nginx -T) .conf to raw files')
    p.add_argument('filename', help='the nginx dump(nginx -T) folder')
    p.add_argument('-o', '--out', type=str, help='write output to a folder, default ~/.dumpplane/data')

    p = create_subparser(dump, 'dump crossplane parsed .json to data storage')
    p.add_argument('filename', help='the nginx dump(nginx -T) folder')
    p.add_argument('-i', '--input', type=str, help='read input from folder which contains crossplane parsed json, default ~/.dumpplane/data')
    p.add_argument('-o', '--out', type=str, help='dump crossplane parsed .json to data storage, supported output: [mongodb://127.0.0.1:27017, http://localhost:9200, file://output], default output from current path')
    p.add_argument('--db', type=str, help='db used to hold configurations, default nginx')
    p.add_argument('--table', type=str, help='table used to hold configurations, default configurations')
    
    def help(command):
        if command not in parser._actions[-1].choices:
            parser.error('unknown command %r' % command)
        else:
            parser._actions[-1].choices[command].print_help()

    p = create_subparser(help, 'show help for commands')
    p.add_argument('command', help='command to show help for')

    parsed = parser.parse_args(args=args)

    if not parsed.__dict__:
        parser.error('too few arguments')

    return parsed

def main():
    kwargs = parse_args().__dict__
    func = kwargs.pop('_subcommand')
    func(**kwargs)

if __name__ == '__main__':
    main()
