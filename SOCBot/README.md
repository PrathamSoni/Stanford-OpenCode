# SOCBot
## A discord bot for monitoring this project
SOC came about through a discord conversation, so it seemed fitting to make a discord bot that can monitor this project. Right now, it can load the README, display current SOC
contributors, list foks, show the latest commit, fetch the number of open and closed issues, show the contents of subdirectories of the repository, and load code from the
repository into a discord channel. At the moment, support for branches is somehwere between poor and nonexistent, and there's room to add pull request tracking functionality.
## Usage

All commands should start with `?soc`

Commands:

`help`, `h` - brings up this text

`contributors`, `c` - list current SOC contributors

`readme`, `r` - bring up the current SOC README

`forks`, `f` - list the number of forks, and the people who have forked

`latest`, `l` - shows the latest commit to the main SOC repository

`issues`, `i` - displays the number of open issues

`list [path]`, `ls [path]` - lists the files and folders at the path within the repository.
A blank path or '/' for path will correspond to main directory of the repository. Folders are
listed in bolded font. If the path is invalid, my response will say so. Use '/' not '\\' in the path.

`view [path]`, `v [path]` - reads a file into discord. Reuqires the path to the file within the repo.
