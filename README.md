# WoWLogParser
Parser of World of Warcraft Advanced Combat Logs.

## Warcraft Log Definitions 

https://wow.gamepedia.com/COMBAT_LOG_EVENT

## Input Prerequisites
1. /combatlog must be enabled (With Advanced Combat Logging enabled in System > Network)
2. Supports python3 (built for Windows 10)
3. Supports WoW patch 8.3 (01/30/2020)

## Output
- Creates file for every mechanic tracked for each boss while logging.
- csv formatted output (See Glossary below for specifics).

## Parser Glossary:
- Tracking Types:
  - dam - Track Individual damage done for each occurance.
    - output : pull#,deltatime,player,damage
  -	aura - Application of buff/debuff
    - output : pull#,deltatime,player
  - cast - each successful cast of said spell
    - output : pull#,deltatime,player
-	MODIFIERS of tracking types :
	-	avg - avg # over entire fight (used by dam). ex. (dam, avg) 
		- output [pull#,player,number]
	-	sum - total # over entire fight (used by dam,aura,cast)
		- ex. (hit, sum) - total # of times player got hit by ability
			- output [pull#,player,number]
	-	hit - records the hit, but not the damage done (used by dam, cast/aura use this by default)
		- output of dam : same, minus damage column
		
## Known Issues:
- General:
  - results files are not separated by difficulty.
    - e.g: Guild Method pulls Wrathion(Heroic) 3 times, and then later comes back to pull Wrathion(Mythic) 2 times. Each Wration results file records 5 pulls worth of data.
- Tracking Healing: 
  - Avenging Wrath is being tracked without considering Paladin specialization because they share the same spellID.
  
