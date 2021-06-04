import sys
import random
import shutil
import copy
from math import ceil, floor
from os import path, remove, mkdir
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# the same folder where this program is stored
if getattr(sys, 'frozen', False):
	mainFolder = path.dirname(sys.executable) # EXE (executable) file
else:
	mainFolder = path.dirname(path.realpath(__file__)) # PY (source) file
sys.path.append(mainFolder)
outputFolder = path.join(mainFolder, "output")

import AMR_support

"""
Ability Values:

00 - Nothing
01 - Fire
02 - Ice
03 - Burning
04 - Wheel
05 - Parasol
06 - Cutter
07 - Beam
08 - Stone
09 - Bomb
0A - Throw
0B - Sleep
0C - Cook
0D - Laser
0E - UFO
0F - Spark
10 - Tornado
11 - Hammer
12 - Sword
13 - Cupid
14 - Fighter
15 - Magic
16 - Smash
17 - Mini
18 - Crash
19 - Missile
1A - Master

The remaining values are either some sort of bug/crash, mix (like when you inhale two abilities at one), or duplicate.
"""

abilities = [
	"Nothing",
	"Fire",
	"Ice",
	"Burning",
	"Wheel",
	"Parasol",
	"Cutter",
	"Beam",
	"Stone",
	"Bomb",
	"Throw",
	"Sleep",
	"Cook",
	"Laser",
	"UFO",
	"Spark",
	"Tornado",
	"Hammer",
	"Sword",
	"Cupid",
	"Fighter",
	"Magic",
	"Smash",
	"Mini",
	"Crash",
	"Missile",
	"Master"
]

normalEnemies = {
	"Bang-Bang"				:	[[0x351AB6], 0x19],
	"Batty"					:	[[0x351A86], 0x00],
	"Big Waddle Dee"		:	[[0x3517E6], 0x00],
	"Blipper"				:	[[0x35167E], 0x00],
	"Bomber"				:	[[0x351A0E], 0x18],
	"Boxin"					:	[[0x3519C6], 0x14],
	"Bronto Burt"			:	[[0x351666], 0x00],
	"Chip"					:	[[0x35170E], 0x00],
	"Cookin"				:	[[0x3519DE], 0x0C],
	"Cupie"					:	[[0x35176E], 0x13],
	"Droppy"				:	[[0x351AFE, 0x3527D6], 0x00], # the second address is the one spawned by Wiz
	"Flamer"				:	[[0x351816], 0x03],
	"Foley"					:	[[0x35197E], 0x09],
	"Giant Rocky"			:	[[0x351A3E], 0x08],
	"Glunk"					:	[[0x351696], 0x00],
	# "Golem"					:	[[0x351966], 0x08], # mostly-unknown; this only covers the Golems spawned by King Golem; address search showed the same thing for all types of Golems
	"Haley"					:	[[0x35173E], 0x00],
	"Heavy Knight"			:	[[0x351A26], 0x12],
	"Hot Head"				:	[[0x35182E], 0x01],
	"Jack"					:	[[0x3517CE], 0x00],
	"Laser Ball"			:	[[0x351846], 0x0D],
	"Leap"					:	[[0x3517B6], 0x00],
	"Metal Guardian"		:	[[0x351A56], 0x0D],
	"Minny"					:	[[0x3519F6], 0x17],
	"Noddy"					:	[[0x35191E], 0x0B],
	# "Parasol Waddle Dee"	:	[[0x??????], 0x05], # unknown; address search showed it as Parasol object
	"Pengy"					:	[[0x35185E], 0x02],
	"Prank"					:	[[0x351B16], 0x00],
	"Rocky"					:	[[0x351876], 0x08],
	"Roly-Poly"				:	[[0x351756], 0x00],
	# "Shadow Kirby"			:	[[0x??????], 0x00], # unknown
	"Shooty"				:	[[0x351996], 0x00],
	"Sir Kibble"			:	[[0x35188E], 0x06],
	"Snapper"				:	[[0x352536], 0x12],
	"Snooter"				:	[[0x3516F6], 0x00],
	"Soarar"				:	[[0x351726], 0x00],
	"Sparky"				:	[[0x3518A6], 0x0F],
	"Squishy"				:	[[0x3516AE], 0x00], # Did you know there's only one of these in the entire game? And it's really well-hidden
	"Sword Knight"			:	[[0x3518BE], 0x12],
	"Twister"				:	[[0x3518EE], 0x10],
	"UFO"					:	[[0x3518D6], 0x0E],
	"Waddle Dee"			:	[[0x35164E, 0x351B76], 0x00], # the second address is the mini-boss version
	"Waddle Doo"			:	[[0x3517FE], 0x07],
	"Wheelie"				:	[[0x351906], 0x04]
}

miniBosses = {
	"Batafire"		:	[[0x351BD6], 0x03],
	"Bombar"		:	[[0x351C36], 0x19],
	"Bonkers"		:	[[0x351BA6], 0x11],
	"Box Boxer"		:	[[0x351BEE], 0x14],
	"Boxy"			:	[[0x351C06], 0x15],
	"Master Hand"	:	[[0x351C1E], 0x16],
	"Mr. Frosty"	:	[[0x351B8E], 0x02],
	"Phan Phan"		:	[[0x351BBE], 0x0A]
}

objects = {
	"Batafire (Fireball)"			:	[[0x352566], 0x00],
	"Bombar (Bomb)"					:	[[0x3526FE], 0x09],
	"Bombar (Missile)"				:	[[0x352716], 0x19],
	"Bonkers (Large Rock)"			:	[[0x352626], 0x00],
	"Bonkers (Small Rock)"			:	[[0x35260E], 0x00],
	"Box Boxer (Energy Blast)"		:	[[0x35272E], 0x00],
	# "Boxy (Bomb)"					:	[[0x??????], 0x09], # unknown
	"Boxy (Present)"				:	[[0x3626CE], 0x00],
	"Dark Mind (Blue Star)"			:	[[0x35296E], 0x02],
	"Dark Mind (Bomb)"				:	[[0x351ACE], 0x18],
	"Dark Mind (Purple Star)"		:	[[0x352986], 0x0F],
	"Dark Mind (Red Star)"			:	[[0x352956], 0x01],
	"Enemy Star"					:	[[0x3525C6], 0x00], # the thing that's spawned by basically every boss/mini-boss
	"King Golem (Rock)"				:	[[0x3524D6], 0x00],
	"Master/Crazy Hand (Bullet)"	:	[[0x35290E], 0x03],
	# "Master/Crazy Hand (Star)"		:	[[0x??????], 0x08], # unknown; address search showed it as normal enemy star
	"Moley (Bomb)"					:	[[0x3528AE], 0x09],
	"Moley (Large Rock)"			:	[[0x3528C6], 0x08],
	"Moley (Oil Drum)"				:	[[0x3528DE], 0x03],
	"Moley (Screw)"					:	[[0x35287E], 0x00],
	"Moley (Small Rock)"			:	[[0x352866], 0x00],
	"Moley (Spiny)"					:	[[0x3528F6], 0x06],
	"Moley (Tire)"					:	[[0x352896], 0x04],
	"Mr. Frosty (Large Ice)"		:	[[0x3525F6], 0x00],
	"Mr. Frosty (Small Ice)"		:	[[0x3525DE], 0x00],
	"Parasol"						:	[[0x35257E], 0x05],
	"Phan Phan (Apple)"				:	[[0x35263E], 0x00],
	"Prank (Bomb)"					:	[[0x352686], 0x09],
	"Prank (Fireball)"				:	[[0x352656], 0x01],
	"Prank (Ice)"					:	[[0x35266E], 0x02],
	"Titan Head (Missile)"			:	[[0x35284E], 0x00],
	"Wiz (Balloon)"					:	[[0x352776], 0x00],
	"Wiz (Bomb)"					:	[[0x35278E], 0x09],
	"Wiz (Car)"						:	[[0x35275E], 0x04],
	"Wiz (Cloud)"					:	[[0x3527A6], 0x0F],
	"Wiz (Football)"				:	[[0x352746], 0x00],
	"Wiz (Poison Apple)"			:	[[0x3527BE], 0x0B]
}

def main():
	# open the GUI
	vp_start_gui()

def randomize():
	global sourceRom
	global numSeedsFinished
	global currSeed
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global includeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject
	global generateAbilityLog

	sourceRom = AMR_support.sourceRom.get()
	try:
		assert path.isfile(sourceRom)
	except:
		return [False, "Invalid ROM input."]
	generateAbilityLog = int(AMR_support.generateAbilityLog.get())
	numSeedsFinished = 0
	if int(AMR_support.useSeed.get()) == 1:
		try:
			assert(len(AMR_support.seedInput.get()) == 10)
			currSeed = int(AMR_support.seedInput.get(), 36)
			abilityDistributionType, basicEnemyBehaviorType, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses, includeMinnyAndWheelie, objectRandomizationType, noneAbilityChanceObject = decodeSeed(AMR_support.seedInput.get()[:5], [2,2,60,60,1,1,2,30], 36)
			abilityDistributionType += 1
			basicEnemyBehaviorType += 1
			includeMiniBosses += 1
			includeMinnyAndWheelie += 1
			objectRandomizationType += 1
			assert 1 <= abilityDistributionType <= 3
			assert 1 <= basicEnemyBehaviorType <= 3
			assert 0 <= noneAbilityChanceBasicEnemy <= 60
			assert 0 <= noneAbilityChanceNonBasicEnemy <= 60
			assert 1 <= includeMiniBosses <= 2
			assert 1 <= includeMinnyAndWheelie <= 2
			assert 1 <= objectRandomizationType <= 3
			assert 0 <= noneAbilityChanceObject <= 30
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
		except:
			return [False, "Invalid Seed."]
		numSeeds = 0
		if not generateSeed(currSeed):
			return [False, "Failed to generate the given seed."]
		return [True, "Successfully generated the given seed."]
	else:
		adtDict = {"Pure Random":1, "By Enemy Grouping":2, "By Ability Frequency":3}
		abilityDistributionType = adtDict.get(AMR_support.abilityDistributionType.get())
		if abilityDistributionType == 1:
			bebDict = {"All Random":1, "Basic Enemies Random":2, "No Random (Unchanged)":3}
			basicEnemyBehaviorType = bebDict.get(AMR_support.basicEnemyBehaviorType.get())
		else:
			basicEnemyBehaviorType = 3
		if basicEnemyBehaviorType != 3:
			noneAbilityChanceEnemy = int(AMR_support.noneAbilityChanceEnemy.get())
			noneAbilityChanceEnemy = min(ceil(noneAbilityChanceEnemy/1.67), 60) # this value rounds to increments of 1.67%; this is to reduce the length of the seed
			noneAbilityChanceBasicEnemy = noneAbilityChanceEnemy
			noneAbilityChanceNonBasicEnemy = noneAbilityChanceEnemy if basicEnemyBehaviorType == 1 else 30
		else:
			noneAbilityChanceBasicEnemy = 0
			noneAbilityChanceNonBasicEnemy = 60
		includeMiniBosses = int(AMR_support.includeMiniBosses.get())
		includeMinnyAndWheelie = int(AMR_support.includeMinnyAndWheelie.get())
		ortDict = {"Yes":1, "Basic Objects Only":2, "No":3}
		objectRandomizationType = ortDict.get(AMR_support.objectRandomizationType.get())
		if objectRandomizationType != 1:
			noneAbilityChanceObject = 30 # unused but needed for seed calculation
			noneAbilityChanceBasicObject = 0
			noneAbilityChanceNonBasicObject = 30
		else:
			noneAbilityChanceObject = int(AMR_support.noneAbilityChanceObject.get())
			noneAbilityChanceObject = min(ceil(noneAbilityChanceObject/3.34), 30) # this value rounds to increments of 3.34%; this is to reduce the length of the seed
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
		try:
			assert 1 <= abilityDistributionType <= 3
			assert 1 <= basicEnemyBehaviorType <= 3
			assert 0 <= noneAbilityChanceBasicEnemy <= 60
			assert 0 <= noneAbilityChanceNonBasicEnemy <= 60
			assert 1 <= includeMiniBosses <= 2
			assert 1 <= includeMinnyAndWheelie <= 2
			assert 1 <= objectRandomizationType <= 3
			assert 0 <= noneAbilityChanceObject <= 30
			settingsSeed = encodeSeed([abilityDistributionType-1, basicEnemyBehaviorType-1, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses-1, includeMinnyAndWheelie-1, objectRandomizationType-1, noneAbilityChanceObject], [2,2,60,60,1,1,2,30])[0]
			seedPluralString = " seed"
		except:
			return [False, "Invalid settings."]
		try:
			numSeeds = int(AMR_support.numSeeds.get())
			1 <= numSeeds <= 20
		except:
			return [False, "Please select a value between 1 and 20 for # of seeds."]
		for i in range(numSeeds):
			maxVal = int("ZZZZZ", 36)
			genSeed = random.randint(0, maxVal)
			currSeed = (settingsSeed*(maxVal+1)) + genSeed
			if not generateSeed(currSeed):
				if numSeedsFinished > 1:
					seedPluralString = " seeds"
				if numSeeds > 0:
					return [False, "Successfully generated "+str(numSeedsFinished)+seedPluralString+", but then something went wrong."]
				else:
					return [False, "Failed to generate"+seedPluralString+"."]
		if numSeedsFinished > 1:
			seedPluralString = " seeds"
		return [True, "Successfully generated "+str(numSeeds)+seedPluralString+"."]

# unused
def main_cmd_line():
	global sourceRom
	global numSeedsFinished
	global currSeed
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global includeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject
	global generateAbilityLog

	print("\n")
	print("---------------------------------------------")
	print("| Welcome to the Amazing Mirror Randomizer! |")
	print("---------------------------------------------")
	sourceRom = ""
	while sourceRom == "":
		Tk().withdraw()
		sourceRom = askopenfilename(filetypes=[("GBA ROM files", "*.gba")])
	useSeed = makeChoice("Do you already have a seed?", ["Yes", "No"])
	seedInput = ""
	numSeedsFinished = 1
	if useSeed == 1:
		currSeed = verifySeed()
		generateAbilityLog = makeChoice("Generate a spoiler text file containing ability distribution?", [
			"Yes",
			"No"])
		numSeeds = 1
		generateSeed(currSeed)
	else:
		print("\nAnswer the following questions to generate a ROM.\n[R] means \"Recommended\".")
		sleep(1)
		abilityDistributionType = makeChoice("[1/6] How should abilities be distributed?", [
			"[R] Pure random (anything goes)",
			"By enemy grouping (enemies that gave matching abilities in the original game (like Sword Knight and Heavy Knight) will still give matching abilities)",
			"By ability frequency (for example, two enemies gave Ice in the original game, so two random enemies will give Ice here)"])
		if abilityDistributionType == 1:
			basicEnemyBehaviorType = makeChoice("[1a/6] How should enemies that do not give an ability be handled?", [
				"[R] All enemies may or may not give an ability",
				"Basic enemies that did not originally give an ability (like Waddle Dee) may or may not give an ability; other enemies are still guaranteed to give an ability",
				"Unchanged (basic enemies will still not give an ability, and other enemies will)"])
		else:
			basicEnemyBehaviorType = 3
		if basicEnemyBehaviorType != 3:
			noneAbilityChanceEnemy = makeChoiceNumInput("[1b/6] For these enemies that may or may not give an ability, how likely is it that they do give an ability? (0\%-100\%) ([R] = 90)", 0, 100)
			noneAbilityChanceEnemy = min(ceil(noneAbilityChanceEnemy/1.67), 60) # this value rounds to increments of 1.67%; this is to reduce the length of the seed
			noneAbilityChanceBasicEnemy = noneAbilityChanceEnemy
			noneAbilityChanceNonBasicEnemy = noneAbilityChanceEnemy if basicEnemyBehaviorType == 1 else 30
		else:
			noneAbilityChanceBasicEnemy = 0
			noneAbilityChanceNonBasicEnemy = 60
		includeMiniBosses = makeChoice("[2/6] Include mini-bosses?", [
			"[R] Yes (randomize mini-boss abilities)",
			"No (do not change mini-bosses)"])
		includeMinnyAndWheelie = makeChoice("[3/6] Include Minny and Wheelie? (Not recommended; you need Mini and Wheel at certain parts of the game)", [
			"Yes (randomize Minny and Wheelie's abilities)",
			"[R] No (do not change their abilities)"])
		objectRandomizationType = makeChoice("[4/6] How would you like to randomize other objects (like inhalable enemy projectiles; basically everything except star blocks)?", [
			"[R] Randomize all objects"
			"Only randomize objects that already give abilities",
			"Do not randomize objects"])
		if objectRandomizationType != 1:
			noneAbilityChanceObject = 30 # unused but needed for seed calculation
			noneAbilityChanceBasicObject = 0
			noneAbilityChanceNonBasicObject = 30
		else:
			noneAbilityChanceObject = makeChoiceNumInput("[4a/6] For objects that may or may not give an ability, how likely is it that they do give an ability? (0\%-100\%) ([R] = 90)", 0, 100)
			noneAbilityChanceObject = min(ceil(noneAbilityChanceObject/3.34), 30) # this value rounds to increments of 3.34%; this is to reduce the length of the seed
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
		generateAbilityLog = makeChoice("[5/6] Generate a spoiler text file containing ability distribution?", [
			"Yes",
			"No"])
		numSeeds = int(makeChoiceNumInput("[6/6] How many seeds do you want to generate with these settings? (up to 20)", 0, 100))

		settingsSeed = encodeSeed([abilityDistributionType-1, basicEnemyBehaviorType-1, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses-1, includeMinnyAndWheelie-1, objectRandomizationType-1, noneAbilityChanceObject], [2,2,60,60,1,1,2,30])[0]
		for i in range(numSeeds):
			maxVal = int("ZZZZZ", 36)
			genSeed = random.randint(0, maxVal)
			currSeed = (settingsSeed*(maxVal+1)) + genSeed
			generateSeed(currSeed)
	input("\nPress Enter to exit.")

def generateSeed(seed):
	global normalEnemies
	global miniBosses
	global objects
	global myEnemies
	global myObjects
	global currSeed
	global numSeedsFinished
	global seedString
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global includeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject
	global generateAbilityLog

	seedString = str(dec_to_base(currSeed, 36)).upper().zfill(10)
	print("\nGenerating ROM #"+str(numSeedsFinished+1)+" with seed "+seedString+".")
	random.seed(currSeed)

	myEnemies = copy.deepcopy(normalEnemies)
	if includeMiniBosses:
		myEnemies.update(copy.deepcopy(miniBosses))
	myEnemies = shuffleDict(myEnemies)
	if not includeMinnyAndWheelie:
		del myEnemies["Minny"]
		del myEnemies["Wheelie"]
	if abilityDistributionType != 3:
		abilityArray = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]
	else:
		abilityArray = []
		for key in myEnemies:
			currVal = myEnemies[key][1]
			abilityArray.append(currVal)
	if abilityDistributionType == 2:
		myEnemies = randomizeGroupByAbility(myEnemies, abilityArray)
	else:
		myEnemies = randomizeGroup(myEnemies, abilityArray, abilityDistributionType != 3, True)

	myObjects = shuffleDict(objects)
	if objectRandomizationType != 3:
		abilityArray = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]
		myObjects = randomizeGroup(myObjects, abilityArray, True, False)

	if not path.isdir(outputFolder):
		mkdir(outputFolder)
	if not generateRom():
		return False
	if generateAbilityLog:
		generateLog()
	numSeedsFinished += 1
	return True

def shuffleDict(oldDict):
	newKeys = list(oldDict.keys())
	random.shuffle(newKeys)
	newDict = dict()
	for key in newKeys:
		newDict.update(copy.deepcopy({key:oldDict[key]}))
	return newDict

def randomizeGroup(group, arr, allowDuplicates=True, isEnemy=True):
	for key in group:
		group[key] = randomizeAbilityWithArray(group[key], arr, isEnemy)
		if not allowDuplicates:
			# for i in range(len(arr)):
			# 	if arr[i] == group[key]:
			# 		del arr[i]
			# 		break
			arr.remove(group[key])
	return group

def randomizeGroupByAbility(group, arr):
	shuffledArray = arr[:]
	random.shuffle(shuffledArray)
	for key in group:
		group[key][1] = shuffledArray[group[key][1]-1]
	return group

def randomizeAbilityWithArray(entity, possibleAbilities, isEnemy=True):
	global abilityDistributionType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject

	if isEnemy:
		if abilityDistributionType == 1 and ((entity[1] == 0x00 and random.randint(1,60) > noneAbilityChanceBasicEnemy) or (entity[1] != 0x00 and random.randint(1,60) > noneAbilityChanceNonBasicEnemy)):
			entity[1] = 0x00
			return entity
	else:
		# objectRandomizationType checks are added so only one noneAbilityChanceObject variable has to be stored in the seed
		if (entity[1] == 0x00 and (objectRandomizationType == 2 or random.randint(1,30) > noneAbilityChanceBasicObject)) or (entity[1] != 0x00 and objectRandomizationType != 2 and random.randint(1,30) > noneAbilityChanceNonBasicObject):
			entity[1] = 0x00
			return entity
	originalAbility = entity[1]
	count = 0
	while entity[1] == originalAbility and count < 2: # unchanged abilites are possible but uncommon
		entity[1] = random.choice(possibleAbilities)
		count += 1
	return entity

def generateRom():
	global sourceRom
	global currSeed
	global seedString

	newRom = path.join(outputFolder, path.splitext(path.basename(sourceRom))[0]+"-"+seedString+".gba")
	shutil.copyfile(sourceRom, newRom)
	try:
		file = open(newRom, "r+b")
		for key in myEnemies:
			for address in myEnemies[key][0]:
				file.seek(address)
				file.write(bytes([myEnemies[key][1]]))
		for key in myObjects:
			for address in myObjects[key][0]:
				file.seek(address)
				file.write(bytes([myObjects[key][1]]))
		file.close()
		print("Succesfully generated ROM with seed "+seedString)
		return True
	except:
		print("Something went wrong. Deleting generated ROM.")
		file.close()
		remove(newRom)
		return False

def generateLog():
	global sourceRom
	global myEnemies
	global myMiniBosses
	global myObjects
	global abilities

	newLog = path.join(outputFolder, path.splitext(path.basename(sourceRom))[0]+"-"+seedString+".txt")
	file = open(newLog, "w")
	file.writelines("NORMAL ENEMIES:\n")
	for key in normalEnemies:
		if key in myEnemies:
			unchangedStr = " [unchanged]" if myEnemies[key][1] == normalEnemies[key][1] else ""
			file.writelines(key+" - "+abilities[myEnemies[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[normalEnemies[key][1]]+" [unchanged]"+"\n")
	file.writelines("\nMINI-BOSSES:\n")
	for key in miniBosses:
		if key in myEnemies:
			unchangedStr = " [unchanged]" if myEnemies[key][1] == miniBosses[key][1] else ""
			file.writelines(key+" - "+abilities[myEnemies[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[miniBosses[key][1]]+" [unchanged]"+"\n")
	file.writelines("\nOBJECTS:\n")
	for key in objects:
		if key in myObjects:
			unchangedStr = " [unchanged]" if myObjects[key][1] == objects[key][1] else ""
			file.writelines(key+" - "+abilities[myObjects[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[objects[key][1]]+" [unchanged]"+"\n")
	file.close()

def makeChoice(question, choices, allowMultiple=False):
	numChoices = len(choices)
	if numChoices == 0:
		print("Warning: A question was asked with no valid answers. Returning None.")
		return None
	if numChoices == 1:
		print("A question was asked with only one valid answer. Returning this answer.")
		return choices[0]
	print("\n"+question)
	for i in range(numChoices):
		print(str(i+1)+": "+choices[i])
	cInput = input().split(" ")
	if not allowMultiple:
		try:
			assert len(cInput) == 1
			choice = int(cInput[0])
			assert choice > 0 and choice <= numChoices
			return choice
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)
	else:
		try:
			choices = [int(c) for c in cInput]
			for choice in choices:
				assert choice > 0 and choice <= numChoices
			return choices
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)

def makeChoiceNumInput(question, minVal, maxVal):
	while True:
		print("\n"+question)
		try:
			var = float(input())
			assert minVal <= var <= maxVal
			return var
		except:
			print("Invalid input.")

# taken from https://www.codespeedy.com/inter-convert-decimal-and-any-base-using-python/
def dec_to_base(num,base):  #Maximum base - 36
	base_num = ""
	while num>0:
		dig = int(num%base)
		if dig<10:
			base_num += str(dig)
		else:
			base_num += chr(ord('A')+dig-10)  #Using uppercase letters
		num //= base
	base_num = base_num[::-1]  #To reverse the string
	return base_num

def encodeSeed(varArray, maxValueArray, base=10):
	seed = 0
	baseShift = 0
	for i in range(len(varArray)):
		seed += varArray[i]<<baseShift
		baseShift += maxValueArray[i].bit_length()
	return seed, dec_to_base(seed, base)

def decodeSeed(seed, maxValueArray, seedBase=10):
	if type(seed) is str:
		seed = int(seed, seedBase)
	baseShift = 0
	varArray = []
	for i in range(len(maxValueArray)):
		bitLength = maxValueArray[i].bit_length()
		varArray.append((seed>>baseShift) & ((2**bitLength)-1))
		baseShift += bitLength
	return varArray

# only used in main_cmd_line (which is unused)
def verifySeed():
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global includeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject

	while True:
		print("\nPlease type the seed and press Enter.")
		seedInput = input().upper().strip()
		try:
			assert(len(seedInput) == 10)
			abilityDistributionType, basicEnemyBehaviorType, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses, includeMinnyAndWheelie, objectRandomizationType, noneAbilityChanceObject = decodeSeed(seedInput[:5], [2,2,60,60,1,1,2,30], 36)
			abilityDistributionType += 1
			basicEnemyBehaviorType += 1
			includeMiniBosses += 1
			includeMinnyAndWheelie += 1
			objectRandomizationType += 1
			assert 1 <= abilityDistributionType <= 3
			assert 1 <= basicEnemyBehaviorType <= 3
			assert 0 <= noneAbilityChanceBasicEnemy <= 60
			assert 0 <= noneAbilityChanceNonBasicEnemy <= 60
			assert 1 <= includeMiniBosses <= 2
			assert 1 <= includeMinnyAndWheelie <= 2
			assert 1 <= objectRandomizationType <= 3
			assert 0 <= noneAbilityChanceObject <= 30
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
			return int(seedInput, 36)
		except:
			print("Invalid seed.")



#######
# GUI #
#######

#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module initially created by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#	platform: Windows NT

import AMR_support

try:
	import Tkinter as tk
	from Tkinter.filedialog import askopenfilename
	from Tkinter import font as tkFont
	from Tkinter.messagebox import showinfo, showerror
except ImportError:
	import tkinter as tk
	from tkinter.filedialog import askopenfilename
	from tkinter import font as tkFont
	from tkinter.messagebox import showinfo, showerror
try:
	import ttk
	py3 = False
except ImportError:
	import tkinter.ttk as ttk
	py3 = True

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root
	root = tk.Tk()
	# 1.7 seems to be default scaling
	# size = root.winfo_screenheight()
	# sizeRatio = 1080/1440
	# root.tk.call('tk', 'scaling', 2.0*sizeRatio)
	AMR_support.set_Tk_var()
	top = TopLevel(root)
	AMR_support.init(root, top)
	root.mainloop()

w = None
def create_TopLevel(rt, *args, **kwargs):
	'''Starting point when module is imported by another module.
	   Correct form of call: 'create_TopLevel(root, *args, **kwargs)' .'''
	global w, w_win, root
	#rt = root
	root = rt
	w = tk.Toplevel (root)
	AMR_support.set_Tk_var()
	top = TopLevel (w)
	AMR_support.init(w, top, *args, **kwargs)
	return (w, top)

def destroy_TopLevel():
	global w
	w.destroy()
	w = None

class TopLevel:
	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])
		self.font = tkFont.Font(family='TkDefaultFont')

		top.geometry(str(750)+"x"+str(450))
		top.minsize(750, 450)
		# top.maxsize(2000, 600)
		top.resizable(1, 1)
		top.title("Amazing Mirror Randomizer")
		top.configure(background="#d9d9d9")
		top.configure(highlightbackground="#d9d9d9")
		top.configure(highlightcolor="black")

		## Menu Bar
		menubar = tk.Menu(top, bg=_bgcolor, fg=_fgcolor, tearoff=0)
		fileMenu = tk.Menu(menubar, tearoff=0)
		fileMenu.add_command(label="Load ROM...", command=AMR_support.setSourceRom)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="File", menu=fileMenu)
		top.config(menu=menubar)
		helpMenu = tk.Menu(menubar, tearoff=0)
		helpMenu.add_command(label="View Help...", command=self.showHelpPopup)
		helpMenu.add_separator()
		helpMenu.add_command(label="About...", command=self.showAboutPopup)
		menubar.add_cascade(label="Help", menu=helpMenu)
		top.config(menu=menubar)

		self.style.map('TCheckbutton',background=
			[('selected', _bgcolor), ('active', _ana2color)])
		self.style.map('TRadiobutton',background=
			[('selected', _bgcolor), ('active', _ana2color)])

		vMult = 700.0/600
		xOffset = -.06

		# Rom Input Label
		Rom_Name = "Kirby & The Amazing Mirror (USA) ROM"
		self.Label_RomInput = ttk.Label(top)
		romTextLength = self.getTextLength(Rom_Name)
		self.Label_RomInput.place(relx=.035, rely=.04*vMult, relheight=.05*vMult, relwidth=romTextLength)
		self.Label_RomInput.configure(background="#d9d9d9")
		self.Label_RomInput.configure(foreground="#000000")
		self.Label_RomInput.configure(font="TkDefaultFont")
		self.Label_RomInput.configure(relief="flat")
		self.Label_RomInput.configure(anchor='w')
		self.Label_RomInput.configure(justify='left')
		self.Label_RomInput.configure(text=Rom_Name)

		# Rom Input Entry
		self.Entry_RomInput = ttk.Entry(top)
		# old relwidth=.40
		self.Entry_RomInput.place(relx=.035+romTextLength-.01, rely=.04*vMult, relheight=.05*vMult, relwidth=.81-romTextLength)
		self.Entry_RomInput.configure(state='readonly')
		self.Entry_RomInput.configure(textvariable=AMR_support.sourceRom)
		self.Entry_RomInput.configure(background="#000000")
		self.Entry_RomInput.configure(cursor="ibeam")

		# Rom Input Button
		self.Button_RomInput = ttk.Button(top)
		self.Button_RomInput.place(relx=.845, rely=.0365*vMult, relheight=.057*vMult, relwidth=.12)
		self.Button_RomInput.configure(command=AMR_support.setSourceRom)
		self.Button_RomInput.configure(takefocus="")
		self.Button_RomInput.configure(text='Load ROM')

		# Use Settings Radio Button
		self.RadioButton_UseSettings = ttk.Radiobutton(top)
		self.RadioButton_UseSettings.place(relx=.035, rely=.11*vMult, relheight=.05*vMult, relwidth=self.getTextLength('Use Settings'))
		self.RadioButton_UseSettings.configure(variable=AMR_support.useSeed)
		self.RadioButton_UseSettings.configure(value="2")
		self.RadioButton_UseSettings.configure(text='Use Settings')
		self.RadioButton_UseSettings.configure(compound='none')
		self.tooltip_font = "TkDefaultFont"
		self.RadioButton_UseSettings_tooltip = ToolTip(self.RadioButton_UseSettings, self.tooltip_font, 'Use the settings defined below to create a random seed.')

		# Use Seed Radio Button
		stringLen = 10
		self.RadioButton_UseSeed = ttk.Radiobutton(top)
		self.RadioButton_UseSeed.place(relx=.035-.01+.81-self.getTextLength("W"*(stringLen+1))-self.getTextLength('Use Seed'), rely=.11*vMult, relheight=.057*vMult, relwidth=self.getTextLength('Use Seed'))
		self.RadioButton_UseSeed.configure(variable=AMR_support.useSeed)
		self.RadioButton_UseSeed.configure(text='''Use Seed''')
		self.tooltip_font = "TkDefaultFont"
		self.RadioButton_UseSeed_tooltip = ToolTip(self.RadioButton_UseSeed, self.tooltip_font, 'Recreate a specific set of changes according to a 10-character seed.')

		# Seed Input Entry
		self.Entry_SeedInput = ttk.Entry(top)
		self.Entry_SeedInput.place(relx=.035-.01+.81-self.getTextLength("W"*(stringLen+1)), rely=.11*vMult, relheight=.05*vMult, relwidth=self.getTextLength("W"*(stringLen+1)))
		self.Entry_SeedInput.configure(state='normal')
		self.Entry_SeedInput.configure(textvariable=AMR_support.seedInput)
		self.Entry_SeedInput.configure(takefocus="")
		self.Entry_SeedInput.configure(cursor="ibeam")
		self.Entry_SeedInput.bind('<Key>',AMR_support.keepUpperCharsSeed)
		self.Entry_SeedInput.bind('<KeyRelease>',AMR_support.keepUpperCharsSeed)

		# Frame
		self.TFrame1 = ttk.Frame(top)
		self.TFrame1.place(relx=.035, rely=.18*vMult, relheight=.55*vMult, relwidth=.93)
		self.TFrame1.configure(relief='groove')
		self.TFrame1.configure(borderwidth="2")
		self.TFrame1.configure(relief="groove")



		self.Label_AbilityDistribution = ttk.Label(top)
		self.Label_AbilityDistribution.place(relx=.23+xOffset, rely=.22*vMult, relheight=(19/450)*vMult, relwidth=105/700)
		self.Label_AbilityDistribution.configure(background="#d9d9d9")
		self.Label_AbilityDistribution.configure(foreground="#000000")
		self.Label_AbilityDistribution.configure(font="TkDefaultFont")
		self.Label_AbilityDistribution.configure(relief="flat")
		self.Label_AbilityDistribution.configure(anchor='w')
		self.Label_AbilityDistribution.configure(justify='left')
		self.Label_AbilityDistribution.configure(text='''Ability Distribution''')
		self.tooltip_font = "TkDefaultFont"
		self.Label_AbilityDistribution_tooltip = \
		ToolTip(self.Label_AbilityDistribution, self.tooltip_font, '''How should abilities be distributed among enemies?

- Pure Random (each enemy type has an equal chance of giving each ability)
- By Enemy Grouping (enemies that gave matching abilities in the original game (like Sword Knight and Heavy Knight) will still give matching abilities)
- By Ability Frequency (abilities will be tied to the same number of enemy types as in the original game; for example, two enemies gave Ice in the original game, so two random enemies will give Ice here)''')

		self.ComboBox_AbilityDistribution = ttk.Combobox(top)
		self.ComboBox_AbilityDistribution.place(relx=.23+xOffset, rely=.265*vMult, relheight=(21/450)*vMult, relwidth=143/700)
		self.value_list = ['Pure Random','By Enemy Grouping','By Ability Frequency',]
		self.ComboBox_AbilityDistribution.configure(values=self.value_list)
		self.ComboBox_AbilityDistribution.configure(state='readonly')
		self.ComboBox_AbilityDistribution.configure(textvariable=AMR_support.abilityDistributionType)
		self.ComboBox_AbilityDistribution.configure(background="#000000")

		self.Label_EnemiesWithoutAbility = ttk.Label(top)
		self.Label_EnemiesWithoutAbility.place(relx=.49+xOffset, rely=.22*vMult, relheight=(19/450)*vMult, relwidth=155/700)

		self.Label_EnemiesWithoutAbility.configure(background="#d9d9d9")
		self.Label_EnemiesWithoutAbility.configure(foreground="#000000")
		self.Label_EnemiesWithoutAbility.configure(font="TkDefaultFont")
		self.Label_EnemiesWithoutAbility.configure(relief="flat")
		self.Label_EnemiesWithoutAbility.configure(anchor='w')
		self.Label_EnemiesWithoutAbility.configure(justify='left')
		self.Label_EnemiesWithoutAbility.configure(text='''Enemies Without an Ability''')
		self.tooltip_font = "TkDefaultFont"
		self.Label_EnemiesWithoutAbility_tooltip = \
		ToolTip(self.Label_EnemiesWithoutAbility, self.tooltip_font, '''How should enemies that do not give an ability be handled?

- All Random (each enemy type may or may not give an ability)
- Basic Enemies Random (basic enemies like Waddle Dee may or may not give an ability; other enemies will)
- No Random (Unchanged) (basic enemies will still not give an ability; other enemies will)''')

		self.ComboBox_EnemiesWithoutAbility = ttk.Combobox(top)
		self.ComboBox_EnemiesWithoutAbility.place(relx=.49+xOffset, rely=.265*vMult, relheight=(21/450)*vMult, relwidth=143/700)
		self.value_list = ['All Random','Basic Enemies Random','No Random (Unchanged)',]
		self.ComboBox_EnemiesWithoutAbility.configure(values=self.value_list)
		self.ComboBox_EnemiesWithoutAbility.configure(state='readonly')
		self.ComboBox_EnemiesWithoutAbility.configure(textvariable=AMR_support.basicEnemyBehaviorType)

		self.Label_Percent1 = ttk.Label(top)
		self.Label_Percent1.place(relx=.83+xOffset, rely=.265*vMult, relheight=(21/450)*vMult, relwidth=14/700)
		self.Label_Percent1.configure(background="#d9d9d9")
		self.Label_Percent1.configure(foreground="#000000")
		self.Label_Percent1.configure(font="TkDefaultFont")
		self.Label_Percent1.configure(relief="flat")
		self.Label_Percent1.configure(anchor='w')
		self.Label_Percent1.configure(justify='left')
		self.Label_Percent1.configure(text='''%''')

		self.Entry_UndecidedEnemyChance = ttk.Entry(top)
		self.Entry_UndecidedEnemyChance.place(relx=.77+xOffset, rely=.265*vMult, relheight=(21/450)*vMult, relwidth=36/700)
		self.Entry_UndecidedEnemyChance.configure(textvariable=AMR_support.noneAbilityChanceEnemy)
		self.Entry_UndecidedEnemyChance.configure(takefocus="")
		self.Entry_UndecidedEnemyChance.configure(cursor="ibeam")
		self.Entry_UndecidedEnemyChance.bind('<Key>',AMR_support.keepNumsEnemies)
		self.Entry_UndecidedEnemyChance.bind('<KeyRelease>',AMR_support.keepNumsEnemies)

		self.Label_UndecidedEnemyChance = ttk.Label(top)
		self.Label_UndecidedEnemyChance.place(relx=.71+xOffset, rely=.1925*vMult, relheight=(32/450)*vMult, relwidth=146/700)
		self.Label_UndecidedEnemyChance.configure(background="#d9d9d9")
		self.Label_UndecidedEnemyChance.configure(foreground="#000000")
		self.Label_UndecidedEnemyChance.configure(font="TkDefaultFont")
		self.Label_UndecidedEnemyChance.configure(relief="flat")
		self.Label_UndecidedEnemyChance.configure(anchor='w')
		self.Label_UndecidedEnemyChance.configure(justify='center')
		self.Label_UndecidedEnemyChance.configure(text='''% Chance of Ability
from Undecided Enemies''')
		self.tooltip_font = "TkDefaultFont"
		self.Label_UndecidedEnemyChance_tooltip = \
		ToolTip(self.Label_UndecidedEnemyChance, self.tooltip_font, '''If an enemy may or may not give an ability, what is the % chance that it will?
100% - Always
0% - Never''')

		self.CheckButton_RandomizeMiniBosses = ttk.Checkbutton(top)
		self.CheckButton_RandomizeMiniBosses.place(relx=.23+xOffset, rely=.355*vMult, relwidth=150/700, relheight=(21/450)*vMult)
		self.CheckButton_RandomizeMiniBosses.configure(variable=AMR_support.includeMiniBosses)
		self.CheckButton_RandomizeMiniBosses.configure(offvalue="2")
		self.CheckButton_RandomizeMiniBosses.configure(takefocus="")
		self.CheckButton_RandomizeMiniBosses.configure(text='''Randomize Mini-Bosses''')
		self.tooltip_font = "TkDefaultFont"
		self.CheckButton_RandomizeMiniBosses_tooltip = \
		ToolTip(self.CheckButton_RandomizeMiniBosses, self.tooltip_font, '''Should Mini-Boss abilities also be randomized, or should they stay the same?''')

		self.CheckButton_RandomizeMinnyAndWheelie = ttk.Checkbutton(top)
		self.CheckButton_RandomizeMinnyAndWheelie.place(relx=.49+xOffset, rely=.355*vMult, relwidth=197/700, relheight=(21/450)*vMult)
		self.CheckButton_RandomizeMinnyAndWheelie.configure(variable=AMR_support.includeMinnyAndWheelie)
		self.CheckButton_RandomizeMinnyAndWheelie.configure(offvalue="2")
		self.CheckButton_RandomizeMinnyAndWheelie.configure(takefocus="")
		self.CheckButton_RandomizeMinnyAndWheelie.configure(text='''Randomize Minny and Wheelie''')
		self.tooltip_font = "TkDefaultFont"
		self.CheckButton_RandomizeMinnyAndWheelie_tooltip = \
		ToolTip(self.CheckButton_RandomizeMinnyAndWheelie, self.tooltip_font, '''Should Minny and Wheelie's abilities also be randomized, or should they stay the same?

Not Recommended; you need Mini and Wheel at certain parts of the game.''')

		self.Label_RandomizeObjects = ttk.Label(top)
		self.Label_RandomizeObjects.place(relx=.23+xOffset, rely=.445*vMult, relheight=(21/450)*vMult, relwidth=106/700)
		self.Label_RandomizeObjects.configure(background="#d9d9d9")
		self.Label_RandomizeObjects.configure(foreground="#000000")
		self.Label_RandomizeObjects.configure(font="TkDefaultFont")
		self.Label_RandomizeObjects.configure(relief="flat")
		self.Label_RandomizeObjects.configure(anchor='w')
		self.Label_RandomizeObjects.configure(justify='left')
		self.Label_RandomizeObjects.configure(text='''Randomize Objects''')
		self.tooltip_font = "TkDefaultFont"
		self.Label_RandomizeObjects_tooltip = \
		ToolTip(self.Label_RandomizeObjects, self.tooltip_font, '''Randomize other objects (like inhalable enemy projectiles; basically everything except star blocks)?

- Yes
- Basic Objects Only (randomize objects that do not already give an ability)
- No''')

		self.ComboBox_RandomizeObjects = ttk.Combobox(top)
		self.ComboBox_RandomizeObjects.place(relx=.23+xOffset, rely=.49*vMult, relheight=(21/450)*vMult, relwidth=143/700)
		self.value_list = ['Yes','Basic Objects Only','No',]
		self.ComboBox_RandomizeObjects.configure(values=self.value_list)
		self.ComboBox_RandomizeObjects.configure(state='readonly')
		self.ComboBox_RandomizeObjects.configure(textvariable=AMR_support.objectRandomizationType)

		self.Label_UndecidedObjectChance = ttk.Label(top)
		self.Label_UndecidedObjectChance.place(relx=.49+xOffset, rely=.4175*vMult, relheight=(32/450)*vMult, relwidth=146/700)
		self.Label_UndecidedObjectChance.configure(background="#d9d9d9")
		self.Label_UndecidedObjectChance.configure(foreground="#000000")
		self.Label_UndecidedObjectChance.configure(font="TkDefaultFont")
		self.Label_UndecidedObjectChance.configure(relief="flat")
		self.Label_UndecidedObjectChance.configure(anchor='w')
		self.Label_UndecidedObjectChance.configure(justify='center')
		self.Label_UndecidedObjectChance.configure(text='''% Chance of Ability
from Undecided Objects''')
		self.tooltip_font = "TkDefaultFont"
		self.Label_UndecidedObjectChance_tooltip = \
		ToolTip(self.Label_UndecidedObjectChance, self.tooltip_font, '''What is the % chance that a randomized object will give an ability?
100% - Always
0% - Never''')

		self.Entry_UndecidedObjectChance = ttk.Entry(top)
		self.Entry_UndecidedObjectChance.place(relx=.54+xOffset, rely=.49*vMult, relheight=(21/450)*vMult, relwidth=36/700)

		self.Entry_UndecidedObjectChance.configure(textvariable=AMR_support.noneAbilityChanceObject)
		self.Entry_UndecidedObjectChance.configure(takefocus="")
		self.Entry_UndecidedObjectChance.configure(cursor="ibeam")
		self.Entry_UndecidedObjectChance.bind('<Key>',AMR_support.keepNumsObjects)
		self.Entry_UndecidedObjectChance.bind('<KeyRelease>',AMR_support.keepNumsObjects)

		self.Label_Percent2 = ttk.Label(top)
		self.Label_Percent2.place(relx=.6+xOffset, rely=.49*vMult, relheight=(21/450)*vMult, relwidth=16/700)
		self.Label_Percent2.configure(background="#d9d9d9")
		self.Label_Percent2.configure(foreground="#000000")
		self.Label_Percent2.configure(font="TkDefaultFont")
		self.Label_Percent2.configure(relief="flat")
		self.Label_Percent2.configure(anchor='w')
		self.Label_Percent2.configure(justify='left')
		self.Label_Percent2.configure(text='''%''')

		# Number of Seeds Label
		self.Label_NumSeeds = ttk.Label(top)
		self.Label_NumSeeds.place(relx=.71+xOffset, rely=.445*vMult, relheight=.05*vMult, relwidth=.11)
		self.Label_NumSeeds.configure(background="#d9d9d9")
		self.Label_NumSeeds.configure(foreground="#000000")
		self.Label_NumSeeds.configure(font="TkDefaultFont")
		self.Label_NumSeeds.configure(relief="flat")
		self.Label_NumSeeds.configure(anchor='w')
		self.Label_NumSeeds.configure(justify='left')
		self.Label_NumSeeds.configure(text='# of Seeds')
		self.tooltip_font = "TkDefaultFont"
		self.Label_NumSeeds_tooltip = ToolTip(self.Label_NumSeeds, self.tooltip_font, 'How many seeds would you like to generate?')

		# Number of Seeds Dropdown
		self.ComboBox_NumSeeds = ttk.Combobox(top)
		self.ComboBox_NumSeeds.place(relx=.71+xOffset, rely=.49*vMult, relheight=.05*vMult, relwidth=.088)
		self.value_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',]
		self.ComboBox_NumSeeds.configure(values=self.value_list)
		self.ComboBox_NumSeeds.configure(state='readonly')
		self.ComboBox_NumSeeds.configure(textvariable=AMR_support.numSeeds)



		# Text Log Check Button
		self.CheckButton_GenerateTextLog = ttk.Checkbutton(top)
		self.CheckButton_GenerateTextLog.place(relx=.2, rely=.895, relheight=.05*vMult, relwidth=.20)
		self.CheckButton_GenerateTextLog.configure(variable=AMR_support.generateAbilityLog)
		self.CheckButton_GenerateTextLog.configure(takefocus="")
		self.CheckButton_GenerateTextLog.configure(text='Generate Text Log')
		self.tooltip_font = "TkDefaultFont"
		self.CheckButton_GenerateTextLog_tooltip = ToolTip(self.CheckButton_GenerateTextLog, self.tooltip_font, 'Would you like to generate a text file that details what abilities are tied to each enemy/object in the created seed?')

		# Create Rom Button
		self.Button_CreateRom = ttk.Button(top)
		self.Button_CreateRom.place(relx=.5, rely=.8915, relheight=.057*vMult, relwidth=.144)
		self.Button_CreateRom.configure(takefocus="")
		self.Label_NumSeeds.configure(anchor='w')
		self.Button_CreateRom.configure(text='''Randomize!''')

		# Other
		self.RadioButton_UseSettings.configure(command=self.prepareSettingsAndSeed)
		self.RadioButton_UseSeed.configure(command=self.prepareSettingsAndSeed)
		self.Button_CreateRom.configure(command=self.attemptRandomize)
		self.ComboBox_AbilityDistribution.bind('<<ComboboxSelected>>',self.changedAbilityDistributionType)
		self.ComboBox_EnemiesWithoutAbility.bind('<<ComboboxSelected>>',self.changedBasicEnemyBehaviorType)
		self.ComboBox_RandomizeObjects.bind('<<ComboboxSelected>>',self.changedObjectRandomizationType)
		self.prepareSettingsAndSeed()

	def getTextLength(self, text):
		return .03+self.font.measure(text)/1000.0

	def prepareSettingsAndSeed(self, unused=None):
		if AMR_support.useSeed.get()=="1":
			self.Entry_SeedInput.configure(state="normal")
			self.Label_AbilityDistribution.configure(state="disabled")
			self.ComboBox_AbilityDistribution.configure(state="disabled")
			self.Label_EnemiesWithoutAbility.configure(state="disabled")
			self.ComboBox_EnemiesWithoutAbility.configure(state="disabled")
			self.Label_UndecidedEnemyChance.configure(state="disabled")
			self.Entry_UndecidedEnemyChance.configure(state="disabled")
			self.CheckButton_RandomizeMiniBosses.configure(state="disabled")
			self.CheckButton_RandomizeMinnyAndWheelie.configure(state="disabled")
			self.Label_RandomizeObjects.configure(state="disabled")
			self.ComboBox_RandomizeObjects.configure(state="disabled")
			self.Label_UndecidedObjectChance.configure(state="disabled")
			self.Entry_UndecidedObjectChance.configure(state="disabled")
			self.Label_NumSeeds.configure(state="disabled")
			self.ComboBox_NumSeeds.configure(state="disabled")
		else:
			self.Entry_SeedInput.configure(state="disabled")
			self.Label_AbilityDistribution.configure(state="normal")
			self.ComboBox_AbilityDistribution.configure(state="readonly")
			if AMR_support.abilityDistributionType.get() != "Pure Random":
				self.Label_EnemiesWithoutAbility.configure(state="disabled")
				self.ComboBox_EnemiesWithoutAbility.configure(state="disabled")
			else:
				self.Label_EnemiesWithoutAbility.configure(state="normal")
				self.ComboBox_EnemiesWithoutAbility.configure(state="readonly")
			if AMR_support.basicEnemyBehaviorType.get() in ["No Random (Unchanged)", "N/A"]:
				self.Label_UndecidedEnemyChance.configure(state="disabled")
				self.Entry_UndecidedEnemyChance.configure(state="disabled")
			else:
				self.Label_UndecidedEnemyChance.configure(state="normal")
				self.Entry_UndecidedEnemyChance.configure(state="normal")
			self.CheckButton_RandomizeMiniBosses.configure(state="normal")
			self.CheckButton_RandomizeMinnyAndWheelie.configure(state="normal")
			self.Label_RandomizeObjects.configure(state="normal")
			self.ComboBox_RandomizeObjects.configure(state="readonly")
			if AMR_support.objectRandomizationType.get() != "Yes":
				self.Label_UndecidedObjectChance.configure(state="disabled")
				self.Entry_UndecidedObjectChance.configure(state="disabled")
			else:
				self.Label_UndecidedObjectChance.configure(state="normal")
				self.Entry_UndecidedObjectChance.configure(state="normal")
			self.Label_NumSeeds.configure(state="normal")
			self.ComboBox_NumSeeds.configure(state="readonly")

	def changedAbilityDistributionType(self, unused=None):
		if AMR_support.abilityDistributionType.get() != "Pure Random":
			AMR_support.basicEnemyBehaviorType.set("N/A")
		else:
			AMR_support.basicEnemyBehaviorType.set("All Random")
		if AMR_support.basicEnemyBehaviorType.get() in ["No Random (Unchanged)", "N/A"]:
			AMR_support.noneAbilityChanceEnemy.set("N/A")
		else:
			AMR_support.noneAbilityChanceEnemy.set("90")
		self.prepareSettingsAndSeed()

	def changedBasicEnemyBehaviorType(self, unused=None):
		if AMR_support.basicEnemyBehaviorType.get() in ["No Random (Unchanged)", "N/A"]:
			AMR_support.noneAbilityChanceEnemy.set("N/A")
		else:
			AMR_support.noneAbilityChanceEnemy.set("90")
		self.prepareSettingsAndSeed()

	def changedObjectRandomizationType(self, unused=None):
		if AMR_support.objectRandomizationType.get() != "Yes":
			AMR_support.noneAbilityChanceObject.set("N/A")
		else:
			AMR_support.noneAbilityChanceObject.set("90")
		self.prepareSettingsAndSeed()

	def attemptRandomize(self):
		results = randomize()
		if results[0]:
			showinfo("Success!", results[1])
		else:
			showerror("Error", results[1])

	def showHelpPopup(self):
		showinfo("Help",
			"To learn more about an option, move your mouse over it.\
			\nYou can generate multiple unique ROMs at once by changing the # of seeds.\
			\nYou can also generate a text log that gives information about a created seed.\
			\nGenerated ROMs will be placed in an \"output\" folder, which will be in the same folder as this program.")

	def showAboutPopup(self):
		showinfo("About", "Kirby & The Amazing Mirror Randomizer v0.92\nMade by GateGuy\n\nhttps://github.com/GateGuy/kamrandomizer")

# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import time, localtime, strftime

class ToolTip(tk.Toplevel):
	"""
	Provides a ToolTip widget for Tkinter.
	To apply a ToolTip to any Tkinter widget, simply pass the widget to the
	ToolTip constructor
	"""
	def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
				 delay=0.5, follow=True):
		"""
		Initialize the ToolTip

		Arguments:
		  wdgt: The widget this ToolTip is assigned to
		  tooltip_font: Font to be used
		  msg:  A static string message assigned to the ToolTip
		  msgFunc: A function that retrieves a string to use as the ToolTip text
		  delay:   The delay in seconds before the ToolTip appears(may be float)
		  follow:  If True, the ToolTip follows motion, otherwise hides
		"""
		self.wdgt = wdgt
		# The parent of the ToolTip is the parent of the ToolTips widget
		self.parent = self.wdgt.master
		# Initalise the Toplevel
		tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
		# Hide initially
		self.withdraw()
		# The ToolTip Toplevel should have no frame or title bar
		self.overrideredirect(True)

		# The msgVar will contain the text displayed by the ToolTip
		self.msgVar = tk.StringVar()
		if msg is None:
			self.msgVar.set('No message provided')
		else:
			self.msgVar.set(msg)
		self.msgFunc = msgFunc
		self.delay = delay
		self.follow = follow
		self.visible = 0
		self.lastMotion = 0
		# The text of the ToolTip is displayed in a Message widget
		tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
				font=tooltip_font,
				aspect=1000).grid()

		# Add bindings to the widget.  This will NOT override
		# bindings that the widget already has
		self.wdgt.bind('<Enter>', self.spawn, '+')
		self.wdgt.bind('<Leave>', self.hide, '+')
		self.wdgt.bind('<Motion>', self.move, '+')

	def spawn(self, event=None):
		"""
		Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
		Usually this is caused by entering the widget

		Arguments:
		  event: The event that called this funciton
		"""
		self.visible = 1
		# The after function takes a time argument in milliseconds
		self.after(int(self.delay * 1000), self.show)

	def show(self):
		"""
		Displays the ToolTip if the time delay has been long enough
		"""
		if self.visible == 1 and time() - self.lastMotion > self.delay:
			self.visible = 2
		if self.visible == 2:
			self.deiconify()

	def move(self, event):
		"""
		Processes motion within the widget.
		Arguments:
		  event: The event that called this function
		"""
		self.lastMotion = time()
		# If the follow flag is not set, motion within the
		# widget will make the ToolTip disappear
		#
		if self.follow is False:
			self.withdraw()
			self.visible = 1

		# Offset the ToolTip 10x10 pixes southwest of the pointer
		self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
		try:
			# Try to call the message function.  Will not change
			# the message if the message function is None or
			# the message function fails
			self.msgVar.set(self.msgFunc())
		except:
			pass
		self.after(int(self.delay * 1000), self.show)

	def hide(self, event=None):
		"""
		Hides the ToolTip.  Usually this is caused by leaving the widget
		Arguments:
		  event: The event that called this function
		"""
		self.visible = 0
		self.withdraw()

	def update(self, msg):
		"""
		Updates the Tooltip with a new message. Added by Rozen
		"""
		self.msgVar.set(msg)

# ===========================================================
#				   End of Class ToolTip
# ===========================================================

if __name__ == '__main__':
	main()