# musicdl

Download .mp3 files from Youtube Music, with minimal effort!

Example:

musicdl (url_here) (opt)

---

## Overview
 - Downloads from Youtube Music URL
 - Cleans filenames
 - Fixes .mp3 file metadata

When musicdl runs, you will be prompted to enter a download location (default = CWD),
an Artist Name(*), and Album Name.

(*) - This option can be skipped. If (opt) is not empty, the directory name of the download
      location will be used. Note: directory names will have underscores formatted to spaces.
      I.e. All_Time_Low -> All Time Low

---

## Installation

### Windows: Scoop (Recommended)
If you use [Scoop](https://scoop.sh), you can install it by doing:

```powershell
scoop bucket add ds_musicdl https://github.com/drspliff17/scoop-ds_musicdl
scoop install musicdl
```

### Manual
Download the latest [release here](https://github.com/drspliff17/ds_musicdl/releases/latest)
Extract ds_musicdl.zip
Move your respective executable to a directory in your PATH

# Note
This is an early build, and has been cobbled together, based from my bash scripts that do the
same thing.

Currently, non-English characters will likely be wiped during cleanse. This will be changed soon

Also, I intend to replace the current (opt) with proper argument parsing, that will change soon too.

When the above mentioned changes are pushed, a help message will be included with the command
