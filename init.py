from datetime import timedelta
import time
from Encounter import Encounter
from Encounter import writeResult
import sys

def main():
    print("Welcome to the raid parser. Please ensure /combatlog is enabled before continuing.")
    input("Press enter to continue.\n")
    print("\n")

    if len(sys.argv) < 2:
        print("Please include argument for log file location.")
        exit()

    fname = sys.argv[1]
    # Eternal Palace raid tracking. Mostly done for testing, as Parser was created in 8.3 (pre Nya'lotha)
    #RAID = {"Abyssal Commander Sivara":[["SPELL_AURA_APPLIED","Unstable Mixture","hit"]],"Blackwater Behemoth":["1","2","3"],"Radiance of Azshara":["1","2","3"],"Lady Ashvane":["1","2","3"],"Orgozoa":["1","2","3"],"The Queen"s Court":["1","2","3"],"Za"qul":["1","2","3"],"Queen Azshara":["1","2","3"], }
    # Nya'lotha raid tracking.
    RAID = {"Wrathion":[["SPELL_DAMAGE","Creeping Madness","hit"],["SPELL_DAMAGE","Gale Blast","sum"]], "Maut":[["SPELL_DAMAGE", "Stygian Annihilation", "hit"], ["SPELL_DAMAGE", "Obsidian Skin", "sum"],["SPELL_DAMAGE", "Black Wings", "hit"]], "Prophet Skitra":[["SPELL_DAMAGE","Surging Images","hit"]], "Dark Inquisitor Xanesh":[["SPELL_DAMAGE","Revile","hit"],["SPELL_AURA_APPLIED","Voidwoken","hit"],["SPELL_DAMAGE","Ritual Field","sum"],["SPELL_DAMAGE","Torment","hit"]],"The Hivemind":[["SPELL_AURA_APPLIED","Corrosion","hit"],["SPELL_DAMAGE","Void Echo","hit"],["SPELL_CAST_SUCCESS","Mind-Numbling Nova","nil"],["SPELL_DAMAGE","Entropic Echo","hit"], ["SPELL_AURA_APPLIED", "Nullification", "hit"]],"Shad'har the Insatiable":[["SPELL_AURA_APPLIED", "Tasty Morsel", "hit"],["SPELL_AURA_APPLIED","Slimy Residue","hit"],["SPELL_DAMAGE","Umbral Breath","hit"],["SPELL_DAMAGE","Umbral Eruption","hit"],["SPELL_DAMAGE","Entropic Breath","hit"],["SPELL_DAMAGE","Bubbling Breath","hit"],["SPELL_DAMAGE","Slurry Outburst","avg"]], "Drest'agath":[["SPELL_DAMAGE","Volatile Detonation","hit"],["SPELL_AURA_APPLIED","Void Infused Ichor","hit"],["SPELL_DAMAGE","Void Glare","sum"]], "Vexiona":[["SPELL_AURA_APPLIED","Encroaching Shadows","hit"],["SPELL_AURA_APPLIED","Gift of the Void","hit"],["SPELL_DAMAGE","Brutal Smash","sum"],["SPELL_AURA_APPLIED","Heart of Darkness","hit"]],"Il'gynoth":[["SPELL_DAMAGE","Eye of N'Zoth","hit"],["SPELL_DAMAGE","Cursebreak","avg"]],"Ra-den the Despoiled":[["SPELL_DAMAGE","Unstable Vita","hit"],["SPELL_DAMAGE","Unstable Void","hit"],["SPELL_DAMAGE","Unstable Nightmare","hit"]], "Carapace of N'Zoth":[["SPELL_AURA_APPLIED","Boon of the Black Prince","hit"],["SPELL_AURA_APPLIED", "Servant of N'Zoth","hit"]], "N'Zoth the Corruptor":[["SPELL_CAST_SUCCESS","Mindwrack","nil"],["SPELL_CAST_SUCCESS","Corrupted Mind", "nil"],["SPELL_AURA_APPLIED","Paranoia","hit"],["SPELL_AURA_APPLIED","Servant of N'Zoth","hit"],["SPELL_AURA_APPLIED","Azeroth's Radiance","hit"],["SPELL_CAST_SUCCESS","Severed Consciousness","hit"]]}

    ifile = open(fname, "r", encoding="utf-8")
    sumPulls = {}

    for b in RAID:
        sumPulls[b] = 0

    while True:
        line = ifile.readline()
        try:
            if not line:
                time.sleep(0.1) # Sleep briefly
                continue
            if "ENCOUNTER_START" in line:
                line = line.replace("\"","").replace("\n","").replace("Il'gynoth, Corruption Reborn","Il'gynoth").split(",")
                info = line[0].split(" ")
                boss = line[2]
                sumPulls[boss] = sumPulls[boss]+1
                print("Boss Encounter Start " + boss + " at " + info[1] +"\n")
                # Encounter recording
                Encounter(RAID, line, info, boss, sumPulls[boss], ifile)
                continue
        except:
             print("Quitting program.")
             exit()
    return #The excape that should never occur but its here anyways

main()
exit()
