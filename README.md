# What <a name="what"></a>

A program that gives the user a list over what comes in tv*.

*only danish tv for now

<br/>

# How to use <a name="how-to-use"></a>

Command using all flags:
```
python3 tvguide.py -c [channel] -t [time] -d [int] -a
```
An example with 'real' values:
```
python3 tvguide.py -c dr1 -c tv2 -t 20:00 -d 1 -a
```
This prints only the tv-shows that start at 8 pm the next day on the channels DR1 and TV2 and there after prints all the shows on DR1 and TV2 for the next day.

<br/>


# Available flags <a name="available-flags"></a>

- ```-c [channel]``` or ```--channel [channel]```
- ```-t [hh:mm]``` or ```--time [hh:mm]```
- ```-d [int]``` or ```--day [int]```
- ```-a``` or ```--all```
- ```--category [category]```
- ```-n``` or ```--now```
- ```-v``` or ```--verbose```
- ```-s [search-term]``` or ```--search [search-term]```
- ```--default-channels [channel]```
- ```--default-space-seperator [space-seperator]```

<br/>


## --channel <a name="--channel"></a>

By using the flag ```-c``` or ```--channel``` you specify which channels you want the program to show tv-shows from. Replace "[channel]" with wanted channel, e.g. "dr1". <br/>
You can specify multiple channels just by using the ```-c``` flag again.<br/>
If no channel(s) is chosen, the default channels is used. You can change the default channels as described [here](#--default-channels)

For example:
```
python3 tvguide.py -c [channel_1] -c [channel_2]
```
**OBS**: when specifing channels with a space such as "TV2 News", use a dash (-) instead of a space. E.g. "TV2 News" -> "TV2-News"

You can also specify "all" as the first channel to get all channels.

Examples:<br/>
```
python3 tvguide.py -c dr1 -c tv2 --all
```
This shows all the programs that run on DR1 and TV2 for today.

<br/>

```
python3 tvguide.py -c all --all
```
This shows all the programs that run on all channels for today.

<br/>


## --time <a name="--time"></a>

By using the flag ```-t``` or ```--time``` you can specify a time for the program to find a tv-show that starts or is running at the specified time.<br/>
Time must be formatted like this: "hh:mm".<br/>
You can specify multiple times.

Example: <br/>
```
python3 tvguide.py -t 19:30 -t 20:00
```
This shows the programs that start or is running at 7.30 pm and 8 pm today for the default channels.

<br/>


## --day <a name="--day"></a>

By using the flag ```-d``` or ```--day``` you specify which day you want to see programs from relative to today (default is today = 0). The range of days you can specify is from yesterday to 6 days ahead, which means the range of integer is to the flag ```--day``` is negative 1 to 6.

Example: <br/>
```
python3 tvguide.py -t 19:30 --day 1
```
This shows the programs that either starts or is running at 7.30 pm tomorrow on the default channels.

<br/>


## --all <a name="--all"></a>

By using the flag ```-a``` or ```--all``` you want to see all the programs running today at the specified channels.

Example: <br/>
```
python3 tvguide.py --all
```
This shows all programs for today that runs on the default channels.

<br/>


## --category <a name="--category"></a>

By using the flag ```--category``` you search after programs that have the specified categories.

Examples: <br/>
```
python3 tvguide.py --category film
```
This shows all the programs that have the category "film" on the default channels for today.

<br/>

```
python3 tvguide.py --category film --category drama
```
This shows all the programs that have either the category "film" or "drama" on the default channels for today.

<br/>


## --now <a name="--now"></a>


Example:
```
python3 tvguide.py --now
```
This shows what programs are currently running on the default channels.

<br/>


## --verbose <a name="--verbose"></a>


Example:
```
python3 tvguide.py --all --verbose
```
This shows all the programs with categories for the default channels for today.

<br/>


## --search <a name="--search"></a>


Examples:
```
python3 tvguide.py --search avis
```
This shows all the programs on the default channels for today that have the word "avis" in the title.

<br/>

```
python3 tvguide.py --search avis --search vejr
```
This shows all the programs on the default channels for today that have either the words "avis" or "vejr" in the title.

<br/>


## --default-channels <a name="--default-channels"></a>


Example:
```
python3 tvguide.py --default-channels dr1 tv2 canal-9
```
This changes the default channels to "DR1", "TV2" and "CANAL 9".

<br/>


## --default-space-seperator <a name="--default-space-seperator"></a>


Example:
```
python3 tvguide.py --default-space-seperator -
```
This changes the default space seperator to the sign "-".

<br/>


# Supported channels <a name="supported-channels"></a>

Right now all the channels on [tvtid.tv2.dk](https://tvtid.tv2.dk/) is supported:
- dr1
- tv2
- tv3
- dr2
- tv2-charlie
- tv2-news
- kanal-5
- tv3-plus
- tv2-zulu
- dr-ramasjang
- kanal-4
- tv2-sport
- tv2-sport-x
- tv3-sport
- tv3-puls
- 6eren
- disney-channel
- tv2-fri
- canal-9
- discovery-channel
- tlc
- nickelodeon
- national-geographic-channel
- tv3-max
- cartoon
- disney-junior
- dk4
- mtv
- animal-planet
- investigation-discovery
- vh1
- eurosport-2
- boomerang
- viasat-film
- viasat-film-action,
- viasat-film-hits,
- viasat-film-family,
- viasat-explorer,
- viasat-nature,
- c-more-first,
- c-more-hits,
- viasat-history,
- disney-xd,
- tv4-sverige
- discovery-world
- nrk2
- nrk1
- svt1
- sv2
- tv2-norge
- discovery-hd-showcase
- rtl
- ard
- zdf
- 3sat
- viasat-golf
- eurosport-1
- cnn
- ndr
- bbc-world
- c-more-series
- travel-channel
- vox
- rtl-2
- super-rtl
- paramount-network
- xee
- viasat-ultra
- bbc-earth
- viasat-series
- arte
- sf-kanalen
- history
- kanal-hovedstaden
- folketinget
- tnt
- nickelodeon-junior
- sat1
- prosieben
- sport1
- national-geographic-wild
- tv2-nord-salto
- tv-midt-vest
- tv2-østjylland
- tv2-øst
- tv-syd
- tv-fyn
- lorry
- tv2-bornholm
- tv3-sport-2-hd
- bbc-brit
- tv5-monde-europe
- national-geographic-people
- comedy-central
- cs-go
- zulu-comedy
- oiii
- discovery-science

<br/>


## TODO

- Add documentation to all flags
- Change section "How to use" to "Examples" or something similar
- Add docstrings to functions
