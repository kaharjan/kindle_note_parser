# Kindle Highlights extractor

## What is this sorcery???
It's a small script written in Python which exports highlights, bookmarks
and notes from the given book file to the desired output format.

Every note, highlight and bookmark are saved locally to your Kindle device in a
file named *My Clippings.txt*, or something similar. That file has a specific
format which enables easy parsing of desired data. Script will take this file,
parse it, and output data the one of the supported output formats.

*My Clippings.txt* should something likes this:
```

The 5 Elements of Effective Thinking (Burger, Edward B.;Starbird, Michael)
- Your Bookmark on Location 111 | Added on Monday, August 10, 2015 7:26:42 PM


==========
The Intelligent Investor, Rev. Ed (Graham, Benjamin;Jason Zweig;Warren E. Buffett)
- Your Bookmark on Location 6152 | Added on Monday, August 10, 2015 8:06:01 PM


==========
The 5 Elements of Effective Thinking (Burger, Edward B.;Starbird, Michael)
- Your Bookmark on Location 289 | Added on Tuesday, August 11, 2015 4:49:23 PM


==========
The 5 Elements of Effective Thinking (Burger, Edward B.;Starbird, Michael)
- Your Bookmark on Location 607 | Added on Tuesday, August 11, 2015 5:19:06 PM


==========
The 5 Elements of Effective Thinking (Burger, Edward B.;Starbird, Michael)
- Your Highlight on Location 718-718 | Added on Wednesday, August 12, 2015 7:17:46 AM

perspiration, the perspiration was the process of incrementally
==========
The 5 Elements of Effective Thinking (Burger, Edward B.;Starbird, Michael)
- Your Bookmark on Location 897 | Added on Wednesday, August 12, 2015 7:33:04 AM
```

## Which export formats does it support?
1. Tex (Latex)
  * Given template .tex file, it will export data in the latex file which can be
easily converted to a PDF file.

2. Markdown
  * Given template it will fill the template with given data from the book.

3. Plain Text
  * Exports in plain .txt format.

## How to use
After you clone the repo, you will see *main.py* script in the root of the
project. Run it with:
```
python main.py [path_to_the_kindle_file]
```
After you run it, it will scan the document and interactively ask you what data
you would like to export, and in what format.

After the program has finished, exported files will be located in the
*exported_files* directory.

## Requirements
The only requirements is Python3 (this was tested on Python 3.5.0)
