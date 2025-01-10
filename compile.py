# compile bookmarklet to bookmarklet.js
# Usage: python compile.py

from rjsmin import jsmin
import sys, argparse


def compile_bookmarklet(input_file='bookmarklet-uncompiled.js', output_file='bookmarklet.js', verbose=False, silent=False):
    """
    Reads the 'bookmarklet.js' file, removes comments and unnecessary whitespace,
    and writes the cleaned content back to 'bookmarklet.js'.

    The function performs the following steps:
    1. Reads the content of 'bookmarklet.js'.
    2. Removes single-line (//) and multi-line (/* */) comments.
    3. Removes all whitespace characters (spaces, tabs, newlines).
    4. Writes the cleaned content back to 'bookmarklet.js'.

    Note:
    - The function assumes that 'bookmarklet.js' is encoded in UTF-8.
    - The function overwrites the original 'bookmarklet.js' file with the cleaned content.
    """
    def log(*args, v=False, **kwargs):
        if not silent and (verbose or not v):
            if v and verbose:
                print('\x1b[34m\x1b[1mLOG:\x1b[22m ', end='')
            print(*args, **kwargs)
            if v and verbose:
                print('\x1b[0m', end='')

    log('Reading', input_file, v=True)
    # read bookmarklet.js
    with open(input_file, 'r', encoding='utf-8') as f:
        bookmarklet = f.read()
    
    log('Cleaning bookmarklet.js', v=True)
    # find // start bookmarklet
    start = bookmarklet.find('(() => { // start bookmarklet')
    # find // end bookmarklet
    end = bookmarklet.find('// end bookmarklet')
    # extract bookmarklet
    bookmarklet = bookmarklet[start:end]

    log('Minifying bookmarklet.js', v=True)
    bookmarklet = jsmin(bookmarklet)
    # check if it spans more than one line
    if '\n' in bookmarklet:
        # warn user
        log('\x1b[33m\x1b[1mWARN:\x1b[22m bookmarklet spans multiple lines\x1b[0m', file=sys.stderr)

    bookmarklet = 'javascript:' + bookmarklet

    log('Writing', output_file, v=True)
    # write bookmarklet.js
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(bookmarklet)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile bookmarklet to bookmarklet.js')
    parser.add_argument('-i', '--input', default='bookmarklet-uncompiled.js', help='Input file (default: bookmarklet-uncompiled.js)')
    parser.add_argument('-o', '--output', default='bookmarklet.js', help='Output file (default: bookmarklet.js)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent output')
    parser.add_argument('-w', '--watch', action='store_true', help='Watch input file for changes')
    parser.add_argument('--watch-interval', type=int, default=1, help='Watch interval in seconds (default: 1)')
    args = parser.parse_args()

    compile_bookmarklet(args.input, args.output, args.verbose, args.silent)
    if args.watch:
        import time
        last = ''
        while True:
            try:
                time.sleep(args.watch_interval)
                with open(args.input, 'r', encoding='utf-8') as f:
                    if args.verbose and not args.silent:
                        print('\x1b[1mChecking\x1b[0m', args.input, end='\x1b[0m\n')
                    if f.read() != last:
                        f.seek(0)
                        last = f.read()
                        compile_bookmarklet(args.input, args.output, args.verbose, args.silent)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e, file=sys.stderr)
                time.sleep(1)
        print('\n\x1b[31mExiting...\x1b[0m')
    else:
        print('Done.')