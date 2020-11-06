from itertools import combinations

""" Class/Origins
AS - Assassin
BL - Blademaster
BR - Brawler
EL - Elementalist
GA - Guardian
GS - Gunslinger
KN - Knight
RA - Ranger
SH - Shapeshifter
SO - Sorcerer
DE - Demon
DR - Dragon
EX - Exile
GL - Glacial
IM - Imperial
NI - Ninja
NO - Noble
PH - Phantom
PI - Pirate
RO - Robot
VO - Void
WI - Wild
YO - Yordle
"""
bonuses = {
"AS": [[3,6], 2],
"BL": [[3,6], 2],
"BR": [[2,4], 2],
"EL": [[3], 1],
"GA": [[2], 4],
"GS": [[2,4], 1],
"KN": [[2,4,6], 4],
"RA": [[2,4], 2],
"SH": [[3], 3],
"SO": [[3,6], 1],
"DE": [[2,4,6], 1],
"DR": [[2], 2],
"EX": [[1], 4],
"GL": [[2,4,6], 1],
"IM": [[2,4], 3],
"NI": [[1,4], 2],
"NO": [[3,6], 1],
"PH": [[2], 3],
"PI": [[3], 4],
"RO": [[1], 5],
"VO": [[3], 5],
"WI": [[2,4], 2],
"YO": [[3,6], 2]
}
#Name,Cost,[Class/Origin],Tier(lower = better)
champs = {
"Aatrox": [3,["DE","BL"],2],
"Ahri": [2,["SO","WI"],5],
"Akali": [4,["NI","AS"],2],
"Anivia": [5,["GL","EL"],2],
"Ashe": [3,["RA","GL"],3],
"Aurelion Sol": [4,["SO","DR"],3],
"Blitzcrank": [2,["RO","BR"],4],
"Brand": [4,["DE","EL"],2],
"Braum": [2,["GA","GL"],3],
"Cho'Gath": [4,["BR","VO"],2],
"Darius": [1,["KN","IM"],4],
"Draven": [4,["IM","BL"],2],
"Elise": [1,["SH","DE"],4],
"Evelynn": [3,["DE","AS"],3],
"Fiora": [1,["BL","NO"],4],
"Gangplank": [3,["GS","BL","PI"],4],
"Garen": [1,["KN","NO"],3],
"Gnar": [4,["SH","YO","WI"],1],
"Graves": [1,["GS","PI"],4],
"Karthus": [5,["SO","PH"],3],
"Kassadin": [1,["VO","SO"],4],
"Katarina": [3,["AS","IM"],2],
"Kayle": [5,["KN","NO"],1],
"Kennen": [3,["YO","NI","EL"],2],
"Kha'Zix": [1,["VO","AS"],3],
"Kindred": [4,["RA","PH"],3],
"Leona": [4,["KN","GA"],2],
"Lissandra": [2,["EL","GL"],3],
"Lucian": [2,["GS","NO"],3],
"Lulu": [2,["SO","YO"],3],
"Miss Fortune": [5,["GS","PI"],2],
"Mordekaiser": [1,["KN","PH"],5],
"Morgana": [3,["SO","DE"],3],
"Nidalee": [1,["SH","WI"],2],
"Poppy": [3,["KN","YO"],3],
"Pyke": [2,["AS","PI"],2],
"Rek'Sai": [2,["BR","VO"],5],
"Rengar": [3,["AS","WI"],4],
"Sejuani": [4,["KN","GL"],2],
"Shen": [2,["BL","NI"],3],
"Shyvana": [3,["SH","DR"],3],
"Swain": [5,["SH","DE","IM"],1],
"Tristana": [1,["GS","YO"],3],
"Twisted Fate": [2,["SO","PI"],5],
"Varus": [2,["DE","RA"],2],
"Vayne": [1,["NO","RA"],4],
"Veigar": [3,["SO","YO"],4],
"Volibear": [3,["BR","GL"],2],
"Warwick": [1,["BR","WI"],4],
"Yasuo": [5,["BL","EX"],1],
"Zed": [2,["AS","NI"],2]
}

drops = [
["Level 2",1,0,0,0,0],
["Level 3",.65,.3,.05,0,0],
["Level 4",.5,.35,.15,0,0],
["Level 5",.37,.35,.25,.03,0],
["Level 6",.245,.35,.3,.1,.005],
["Level 7",.2,.3,.33,.15,.02],
["Level 8",.15,.25,.35,.2,.05],
["Level 9",.1,.15,.35,.3,.1],
]
#Get list of names/classes
names = list(champs.keys())
classes = list(bonuses.keys())

#Create cIDs to reduce memory usage
cIDs = []
cid = 0
for name in names:
    cIDs.append(cid)
    cid += 1

def getBonus(comb):
    bonus = 1
    # List all class traits on team
    clist = []
    for id in comb:
        champ = names[id]
        traits = champs[champ][1]
        for trait in traits:
            clist.append(trait)

    # Get class counts
    for id in classes:
        b = 0
        count = clist.count(id)
        if count > 0:
            vals = bonuses[id][0]
            for val in vals:
                if count >= val:
                    b +=1
                else: break
            bm = 6 - bonuses[id][1]
            bonus += (b*bm)
    return bonus

def getChance(comb,level):
    tChance = 1.0
    for id in comb:
        champ = names[id]
        cost = champs[champ][0]
        sum = 0
        count = 0
        avg = 0
        for x in range(0,level - 1):
            sum += drops[x][cost]
            count +=1
        avg = sum/count
        #chance = drops[level - 2][cost]
        chance = avg
        if chance == 0: return 0
        tChance = tChance * chance
    return tChance

def getPower(comb):
    power = 0
    for id in comb:
        champ = names[id]
        tier = 6 - champs[champ][2]
        power += tier
    return power

def getValue(comb):
    value = 0
    for id in comb:
        champ = names[id]
        cost = 6 - champs[champ][0] #lower is better, similar to tier
        value += cost
    return value

#Score factors: bonus * chance * power * value
def getScore(comb,level):
    chance = getChance(comb, level)
    if chance == 0: return 0
    bonus = getBonus(comb)
    power = getPower(comb)
    value = getValue(comb)
    score = bonus * power #* chance #*value
    return score

def getString(comb):
    str = []
    for c in comb:
        str.append(names[c])
    string = ",".join(str)
    return string

def writeFile(combs,x):
    counter = 0
    f = open("Level_{}_Comps.txt".format(x), "w+")
    for comb in combs:
        counter += 1
        f.write("{}\n".format(comb))
        print("Writing {}".format(counter))
    f.close()


def readFile():
    with open('Test.txt') as f:
        for line in f:
            print(line)

#Find all possible teams at each level

#for x in range (2,10):
#readFile()
x = 6
counter = 0

combs = combinations(cIDs, x)
#total = len(combs)
#writeFile(combs,x)


scores = []
max = 0
for comb in combs:
    counter += 1
    #print("{} of {}".format(counter,total))
    #score = getBonus(comb)
    score = getScore(comb,x)
    scores.append([score,comb])
    if score > max:
        max = score
        comb_str = getString(comb)
        print("{} - {}  : {}".format(comb_str,score,counter))
scores.sort(key=lambda x: x[0], reverse = True)
top_score = scores[0][0]
#top = scores[0]
#top_comb = ",".join(top[1])
for y in range(0,300):
    comb = scores[y][1]
    comb_str = getString(comb)
    print("#{} : {} - {}".format(y,comb_str,scores[y][0]))
#print("Level {}: {} - {})".format(x,top_comb,top[0]))


#print(one)

#TODO: Find best chance max overlap using drop rates
