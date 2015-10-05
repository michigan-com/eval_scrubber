Eval/Base64 File Scrubber
=========================

This script will walk through all files in a directory, find, and remove
any content that is suspected to be malicious.

This scan uses a regular expression to seek out any potentially malicious content

```
infected_pattern = re.compile(r"<\?php\s*eval\((.+\()*base64_decode\(.+\)\).+\s*?>")
```

What it is matching is `<?php eval(base64_decode()) ?>` or `<?php eval(gzinflate(base64_decode())) ?>`

It is strongly advized to check that this regular expression will match your needs.

We have not covered all of the edge cases for this script so be warned running this
script could have negative consequences.

The script accepts two arguments: action and directory

Actions:

* Find - Scans directory recursively and lists all potentially infected files
* Remove - Scans directory recursively and removes the regular express match
from all potentially infected files

```
python scrubber.py find <dir>
python scrubber.py remove <dir>
```

Set the log level
```
DEBUG=1 python scrubber.py find <dir>
```
