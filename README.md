# What

A program that gives the user a list over what comes in tv*.

*only danish tv for now

<br/>

# How to use

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

# Available flags

- ```-c [channel]``` or ```--channel [channel]```
- ```-t [hh:mm]``` or ```--time [hh:mm]```
- ```-a``` or ```--all```
- ```-d [int]``` or ```--day [int]```

<br/>

By using the flag "-c" or "--channel" you specify which channels you want the program to show tv-shows from. Replace "[channel]" with wanted channel, e.g. "dr1". <br/>
You can specify multiple channels just by using the "-c" flag again.<br/>
For example:
```
python3 tvguide.py -c [channel_1] -c [channel_2]
```
**OBS**: when specifing channels with a space such as "TV2 News", use a dash (-) instead of a space. E.g. "TV2 News" -> "TV2-News"

You can also specify "all" as the first channel to get all channels.

<br/>

By using the flag "-t" or "--time" you can specify a time for the program to find a tv-show that starts at the specified time.<br/>
Time must be formatted like this: "hh:mm". You can specify multiple times.

<br/>

By using the flag "-a" or "--all" you want to see all the programs running today at the specified channels.

<br/>

By using the flag "-d" or "--day" you specify which day you want to see programs from relative to today (default is today = 0). The range of days you can specify is from yesterday to 6 days ahead, which means the range of integer is to the flag "--day" is negative 1 to 6.

<br/>

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

- Add a file with default values (such as channels) that the user can change by defining them with commands
- Add an argument to search for a specific program, such as "TV-avisen" and then show all the programs (with time)
- When searching for a specific program or time, then also show the category for the program, perchaps when only using the flag "--verbose" or similar flag name
- Add an argument to search for a specific category, and then show all the programs with that category
