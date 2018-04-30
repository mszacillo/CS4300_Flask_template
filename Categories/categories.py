# coding = utf-8
import re

#categories:
categoryDict = {}
categoryDict["breakup"] = "cheated, secret, relationship, drunken, mistake, bad, five, months, last_girlfriend, rough_past, fling, breakdown, last_encounter, forgave, three_months_ago, past_relationships, few_dates, this_past_week, new_boyfriend, the_past_weeks, the_past_two_years, realtionship, relationship_problems, fake_relationship, first_conversation, one_night_stand, parents_death, relationship, new_girlfriend, current_boyfriend, ex-girlfriend, big_fight, feelings, home_life, serious_relationship, break-up, last_relationship, good_relationship, the_past_few_weeks, incident, stupid_mistake, friendship, first_encounter, meltdown, love_life, the_past_few_months, first_fight, whole_incident, ex, drinking_problem, perfect_relationship, rehab, last_conversation, relationships, new_relationship, whole_deal, parents_divorce, little_incident, last_party, about_three_months, little_fight, whole_situation, long_distance_relationship, great_relationship, dated, huge_fight, last_boyfriend, heartbroken, sad_thing, rough_patch, breakup, high_school_years, the_past_2_years, depressed, break_ups, boyfriend, huge_argument, family_problems, these_past_few_months, nearly_a_year, long_relationship, real_relationship, fake_girlfriend, rough_time, dating, trust_issues, about_two_months, strong_feelings, past_relationship, first_boyfriend, guy_friend, big_argument, ex-boyfriend, cheating, first_love, girlfriend"
categoryDict["angry"] = "pissed, stupid, livid, upset, sad, surprised, happy, sick, ashamed, insulted, stubborn, serious, dissapointed, nervous, anger, guilty, worried, heartbroken, peeved, stressed, mad, defensive, harsh, protective, usual_self, sympathetic, suspicious, annoyed, angered, outraged, saddened, distraught, scared, infuriated, terrified, hurt, selfish, afraid, resentful, violent, irate, offended, angry, jealous, conflicted, enraged, angrier, curious, possessive, paranoid, emotional, disgusted, troubled, frightened, depressed, distressed, regretful, irritable, aggravated, disappointed, careless, frustrated, shocked, remorseful, furious, unhappy, irritated, embarrassed, aggressive, relieved, anxious, hysterical, concerned, hostile, riled, persistent, disturbed, devastated, flustered, agitated, confused"
categoryDict["sad"] = "pissed, distant, upset, sick, sad, happy, homesick, cry, ashamed, disapointed, hopeless, dissapointed, serious, nervous, broken, guilty, miserable, worried, heartbroken, old_self, mad, stressed, hopeful, glad, happier, sympathetic, though, embarassed, estatic, sadder, saddened, betrayed, distraught, scared, terrified, hurt, selfish, tired, upsets, heartbreaking, horrible, kinda, terrible, glum, scary, angry, excited, jealous, conflicted, depressing, upsetting, alone, curious, relived, emotional, depressed, regretful, bad, tragic, awful, disappointed, shy, weird, shocked, cause, devastated, saddens, unhappy, joyful, gloomy, relieved, anymore, care, bummed, concerned, embarrassed, nervouse, worrying, honestly, mean, lonely, lost, confused"
categoryDict["happy"] = "upset, sick, loved, sad, happy, love, surprised, homesick, guess, dissapointed, sure, nervous, genuinely, important, miserable, wanted, worried, heartbroken, trust, honestly, mad, hopeful, thrilled, glad, cared, happier, though, suppose, estatic, proud, always, supportive, scared, actually, special, wonderful, ecstatic, blessed, greatful, hope, angry, excited, jealous, pleased, much, great_friends, great, enthusiastic, contented, depressed, perfect, bad, disappointed, confident, weird, wish, overjoyed, grateful, care, unhappy, good, joyful, relieved, crazy, elated, positive, content, lucky, nice, optimistic, honest, fun, thankful, like, truly, because, lonely, understand"
categoryDict["love"] = "cherish, nt, loved, happy, love, understand, bet, honestly, special_one, thank, trust, remember, believe, friend unconditionally, whole, heart, lover, special, person, promise, baby, missed, hurts, only_you, hope, beautiful, loving, babe, greatful, loves, forgive, means, great, liked, wanna, alot, enjoy, yours, deserve, yes, miss, awesome, .and, appreciate, truely, cause, treasure, you,i, adore, wish, special_someone, care, gonna_love, good, said, mine, daddy, amazing, forget, best_girlfriend, adores, like, likes, dearly, biggest_fan, misses, because, mean"
categoryDict["tired"] = "complaining, exhausted, knackered, cranky, lazy, frustrated, weak, used, weary, late_last_night, sore, exausted, angry, dizzy, depressed, annoyed, grumpy, scared, early, fatigued, a_long_day, drowsy, hungry, upset, restless, worried, irritable, lonely, sleep, groggy, sleepy, little_sleep, thirsty, tiered, heavy, bored, tierd, tired, sick, stressed, hungover, late, enough_sleep, jet_lag, sad, jetlag, fussy, tiring"
categoryDict["relax"] = "relaxing, relaxation, warm, loosen, ease, cool, sooth, relaxed, calming, rest, soothe, relax, relieve, settle, calm, tense_muscles, breather, unwind"


#takes string of relevant category words given by empath and returns set of all words (also separates two word phrases)
def s2re (category):
	reg = re.findall("[A-z]+", category)
	for x in reg:
		re.split("[_]", x)
	return set(reg)

for key in categoryDict:
	categoryDict[key] = s2re(categoryDict[key])

#categoryDict = dictionary [key = name of category (string); value = set of words in category (set)], categories = list of categories selected
#example: selectCategory(["angry", "breakup"], categoryDict)
def selectCategory (categories, categoryDict):
	wordSet = set()
	for x in categories:
		wordSet = wordSet.union(categoryDict[x])
	return wordSet

#inverted index: term:[(song, count), (song, count)...]
#dictionary where key = songid, value = set of words in song ?? 
def createdicts (invdict):
	wordsetdict = {}
	for k,v in invdict:
		for x,y in v:
			if x not in wordsetdict:
				wordsetdict[x] = set()
			wordsetdict[x].append(k)
	return wordsetdict

#selectCategory = set of words in Category or Categories selected, songs = dictionary with songIDs and sets
def score (selectCategory, songs):
	scores = {}
	for word in selectCategory:
		for songDict in songs:
			if word in songDict:
				if songDict in scores:
					scores[songDict] = 1
				else:
					scores[songDict] +=1
	return scores

import heapq
# top n scores
def topnscores (scoresdict, n=10):
	return heapq.nlargest(n, scores, key=scores.get)












	









