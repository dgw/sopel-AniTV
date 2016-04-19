# sopel-AniTV
AniTV module for sopel to get showtimes and channels from the AniTV API.

## Requirements
The AniTV module relies on the following Python modules:

* `datetime` (standard Python library)
* `re` (standard Python library)
* `requests` (should be in standard Python library)

## Usage
Commands & arguments:

* `.ani <search keywords> -r -3 -ch BS11`
  * `<search keywords>`: the title (or keyword) to search on AniTV
  * `-1` to `-5`: specify how many results to retrieve (5 is the hardcoded maximum)
  * `-r`: reverse sort order (has no effect if the default of one result is returned)
  * `-ch channelname` or `-st station`: filter results by station/channel name (must not contain spaces)

Arguments can be specified in any order, with the caveat that required parameters (currently
only `-ch`/`-st` has this) may not be separated from their argument. For example, the command
`.ani imouto -ch -3 BS11` would not work as expected; it would search for the keywords "imouto
BS11" filtered by channel name "-3", and probably return no results.

