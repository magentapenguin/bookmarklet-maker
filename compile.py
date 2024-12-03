# compile bookmarklet to bookmarklet.js
# Usage: python compile.py

from rjsmin import jsmin

def compile_bookmarklet():
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
    # read bookmarklet.js
    with open('bookmarklet-uncompiled.js', 'r', encoding='utf-8') as f:
        bookmarklet = f.read()
    # find // start bookmarklet
    start = bookmarklet.find('(() => { // start bookmarklet')
    # find // end bookmarklet
    end = bookmarklet.find('// end bookmarklet')
    # extract bookmarklet
    bookmarklet = bookmarklet[start:end]

    bookmarklet = jsmin(bookmarklet)

    bookmarklet = 'javascript:' + bookmarklet

    # write bookmarklet.js
    with open('bookmarklet.js', 'w', encoding='utf-8') as f:
        f.write(bookmarklet)

if __name__ == '__main__':
    compile_bookmarklet()
    print('Compiled bookmarklet.js')