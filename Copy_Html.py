#!/sur/bin/env  python2
#-*-coding=utf-8-*-

from shutil import copytree, ignore_patterns

if __name__ == "__main__":
    print "Copy......"
    copytree("XLS_DATA", "HTML",  ignore=ignore_patterns('*.xlsx'))
    print "End!"