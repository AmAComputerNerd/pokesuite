# PokeSuite
A collection of neat Pokemon-info utilities for me to practise my Python programming on.

---------

As of now, I currently have four planned modules for this project, alongside a main file to simplify usage.
These files are:

  - **PokeType:** A tool enabling best-case scenario type matchups, to put it simply, to calculate type effiencies against a Pokemon opponent so that you, as the player, may figure out the most efficient and least efficient moves to make. This idea has been expanded on since V1 to take into account STAB moves and, when working in Advanced mode, move power and special conditions, to most effectively predict moves to be used against you, and the best returning move to use back.
  - **PokeFind:** An API-based utility designed mainly for integration purposes, but also acts as an external PokeDex for any Pokemon, ability, move, and more. As it relies entirely upon the PokeAPI online service to receive the valid information, an internet connection is required. The main purposes of PokeFind serve to it's moduable state, as other modules can use the PokeAPI and convenience methods within the file to retrieve information without unavoidable hard-coding (that be, the act of programming every single Pokemon, ability, move, status... into the script natively).
  - **PokeBuild/PokeTeam:** A combination of a team builder and completely customisable creation tool, this module provides the framework to create custom teams to test within the PokeBattle module, and furthered since V1, methods for creating custom abilities, moves, and of course, Pokemon! The module is best explored through the PokeSuite program, as it benefits greatly from connections to all of the other modules. A lot of abilities (such as type suggestions, accurate statistics, and battle functionality) are locked out when ran standalone, though, remains functional in a simpler interface.
  - **PokeBattle:** A fully-working battle simulator for Pokemon, this module allows complete control over battles and the teams that fight within them. Similar to Pokemon Showdown, the program can simulate battles between two humans, or when ran through PokeSuite, a human and AI, to test the strength of unique teams without any repercussion, and with complete support for custom Pokemon, moves, and abilities created within the PokeBuild/PokeTeam module. This module relies upon PokeBuild/PokeTeam to function, and benefits greatly through connections to other modules for it's AI capabilities and other misc features.

I hope to achieve completion of all of these modules soon, though various factors in my life currently such as exams, moving and so fourth will probably limit me to an end-of-year deadline. That being said, I do believe I will actually complete this project (unlike others), just due to the very low expectactions I hold myself to re: Python - I shouldn't feel a need to rush, so burnout should take a lot longer to hit than in some of my old plugins, such as my Hypixel SkyBlock Recreation (*V2 soon?*).

----------

## Q&A
**Nothing lol**