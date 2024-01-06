<!--
This file is auto-generated and any changes made to it will be overwritten
-->
# tests

## tests._test


### _class_ tests._test.TestExit()
Bases: `object`

Test correct exit status returned from main.


#### test_bad(write_file: Callable[[Path, str], None], name: str, template: str, _: str)
Test non-zero when constants are detected.


### Dequote

Test removing quotes from str.


### File args

Test passing individual file names to the `path` argument.


### File ignore str

Test results when one file exists.


### File non rel

Test header and result when passing relative files to `path`.

Ensure path is resolved properly when path is not in CWD.


### Ignore files

Test results when multiple files exist.


### Ignore from

Test file/strings passed to `ignore_from` only ignores file.


### Ignore from no value given

Test program continues if value not given to key.

No need to run any assertions, testing no error raised.


### Len and count

Test using `-c/--count` and `-l/--len`


### Multiple files multiple packages

Test results when multiple files exist.


### Multiple files single packages

Test results when multiple files exist.


### No ansi

Test output with color and output when using `-n/--no-color`.


### Parse str

Test results when one file exists.


### Print version

Test printing of version on commandline.


### Single file

Test results when one file exists.


