"""
Generate ~10,000 labelled training samples for cyberbullying detection.
Output: data/cyberbullying_data_full.csv  (2,500 rows per class, 10,000 total)

Run: python generate_data.py
"""
import csv
import os
import random

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT   = os.path.join(BASE_DIR, "data", "cyberbullying_data_full.csv")
TARGET   = 2500   # per class → 10 000 total


# ── Shared word banks ──────────────────────────────────────────────────────────
NAMES = [
    "Alex", "Jordan", "Sam", "Taylor", "Casey", "Morgan", "Riley", "Drew",
    "Quinn", "Blake", "Jesse", "Chris", "Dana", "Jamie", "Avery", "Skyler",
    "everyone", "guys", "team", "friends", "you all", "folks", "all of you",
]
POS_ADJ = [
    "amazing", "wonderful", "fantastic", "incredible", "great", "awesome",
    "brilliant", "excellent", "outstanding", "superb", "terrific", "magnificent",
    "splendid", "delightful", "phenomenal", "remarkable", "stellar", "exceptional",
    "breathtaking", "inspiring", "unforgettable", "impressive",
]
ACTIVITIES = [
    "hiking", "reading", "cooking", "gaming", "studying", "painting",
    "dancing", "running", "cycling", "swimming", "baking", "writing",
    "drawing", "gardening", "volunteering", "yoga", "photography",
    "kayaking", "climbing", "journalling", "sketching", "travelling",
]
SUBJECTS_POS = [
    "the movie", "that book", "the concert", "the game", "the show",
    "the documentary", "the podcast", "the article", "the event",
    "the restaurant", "the café", "the exhibition", "the play",
    "the lecture", "the workshop", "the performance", "the musical",
    "the gallery", "the festival", "the series",
]
REACTIONS = [
    "it was amazing", "loved every minute of it", "highly recommend it",
    "totally worth it", "exceeded my expectations", "really enjoyed it",
    "had a fantastic time", "absolutely loved it", "was blown away by it",
    "cannot recommend it enough", "was pleasantly surprised",
    "would go again in a heartbeat", "it left me speechless",
]
TIME_PERIODS = [
    "weekend", "week", "day", "evening", "morning", "holiday",
    "semester", "summer", "vacation", "break", "month", "afternoon",
]
TIME_REFS = [
    "this weekend", "tomorrow", "Friday evening", "next week",
    "on Saturday", "after class", "tonight", "this afternoon",
    "over the break", "this Friday", "sometime soon", "next Friday",
    "on Sunday", "this Thursday",
]
PLAN_ACTS = [
    "catch a movie", "grab coffee", "go hiking", "have a game night",
    "study together", "eat out", "go to the park", "watch the game",
    "do a road trip", "visit the museum", "check out the concert",
    "explore the city", "cook dinner together", "have a picnic",
    "go bowling", "play board games", "grab brunch", "go to the beach",
    "visit the art gallery", "try the new restaurant",
]
COMP_SUBJECTS = [
    "Your presentation", "Your artwork", "Your performance",
    "The project you worked on", "Your speech", "The event you organized",
    "Your essay", "Your design", "Your cooking", "The solution you proposed",
    "Your contribution", "Your idea", "Your teamwork", "Your effort",
    "The report you wrote", "The code you wrote", "Your creativity",
]
GREETINGS = ["Hey", "Hi", "Hello", "Good morning", "Good evening", "Howdy", "What's up", "Heyy"]


# ══════════════════════════════════════════════════════════════════════════════
#  CLASS 1 — NOT_CYBERBULLYING
# ══════════════════════════════════════════════════════════════════════════════
def _ncb():
    r = random
    verbs_past = ["finished", "watched", "tried", "visited", "read", "saw", "completed"]
    verbs_check = ["tried", "seen", "read", "visited", "checked out", "experienced"]
    good_news = [
        "got accepted", "got the job", "won first place", "passed the exam",
        "received the scholarship", "got promoted", "aced the interview",
    ]
    positivity = [
        "motivated", "inspired", "energized", "grateful", "happy", "blessed",
        "content", "optimistic", "upbeat", "thrilled",
    ]
    community = ["group", "community", "team", "class", "forum", "server", "club"]
    qualities = ["supportive", "kind", "helpful", "positive", "welcoming", "talented", "creative"]

    templates = [
        # ── Greetings
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}! How was your {r.choice(TIME_PERIODS)}?",
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}, how are you doing today?",
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}! Did you have a good {r.choice(TIME_PERIODS)}?",
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}, hope you're having a {r.choice(POS_ADJ)} day!",
        lambda: f"{r.choice(GREETINGS)} everyone! Hope you all had a wonderful {r.choice(TIME_PERIODS)}.",
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}! Long time no see, how's everything?",
        lambda: f"{r.choice(GREETINGS)} {r.choice(NAMES)}, checking in — how are things going?",
        # ── Sharing experiences
        lambda: f"Just {r.choice(verbs_past)} {r.choice(SUBJECTS_POS)} and {r.choice(REACTIONS)}!",
        lambda: f"Finally got around to {r.choice(SUBJECTS_POS)} — {r.choice(REACTIONS)}.",
        lambda: f"Has anyone {r.choice(verbs_check)} {r.choice(SUBJECTS_POS)}? {r.choice(REACTIONS).capitalize()}!",
        lambda: f"Just got back from {r.choice(ACTIVITIES)} — it was {r.choice(POS_ADJ)}!",
        lambda: f"Spent the {r.choice(TIME_PERIODS)} {r.choice(ACTIVITIES)} and {r.choice(REACTIONS)}.",
        lambda: f"I tried {r.choice(ACTIVITIES)} for the first time this {r.choice(TIME_PERIODS)} and {r.choice(REACTIONS)}.",
        lambda: f"Went to {r.choice(SUBJECTS_POS)} last {r.choice(['night','weekend','week'])} — {r.choice(REACTIONS)}.",
        lambda: f"Discovered {r.choice(SUBJECTS_POS)} recently and {r.choice(REACTIONS)}.",
        # ── Making plans
        lambda: f"Anyone {r.choice(['want to','up for','interested in'])} {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}?",
        lambda: f"We should {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}, who's in?",
        lambda: f"Thinking of {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)} — anyone interested?",
        lambda: f"Does anyone want to {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}?",
        lambda: f"Let's {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}, it'll be {r.choice(POS_ADJ)}!",
        lambda: f"Anyone free to {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}? Would be fun!",
        lambda: f"I'm planning to {r.choice(PLAN_ACTS)} {r.choice(TIME_REFS)}, feel free to join!",
        # ── Compliments and encouragement
        lambda: f"{r.choice(COMP_SUBJECTS)} was {r.choice(POS_ADJ)}, well done!",
        lambda: f"Congrats on your {r.choice(['promotion','achievement','milestone','graduation','award','success'])}! You totally deserve it!",
        lambda: f"{r.choice(COMP_SUBJECTS)} came out {r.choice(POS_ADJ)}! Great work.",
        lambda: f"Really impressed by {r.choice(COMP_SUBJECTS).lower()} — keep it up!",
        lambda: f"Just wanted to say {r.choice(COMP_SUBJECTS).lower()} was {r.choice(POS_ADJ)}. Proud of you!",
        lambda: f"Huge shoutout to {r.choice(NAMES)} — {r.choice(COMP_SUBJECTS).lower()} was {r.choice(POS_ADJ)}!",
        lambda: f"You should be really proud of yourself. {r.choice(COMP_SUBJECTS)} was {r.choice(POS_ADJ)}.",
        # ── Help requests
        lambda: f"Can someone help me with {r.choice(['this math problem','the assignment','the notes','this concept','the project'])}?",
        lambda: f"Does anyone know how to {r.choice(['solve','approach','understand','tackle','fix'])} this? Struggling a bit.",
        lambda: f"Any recommendations for {r.choice(['a good book','a fun activity','a restaurant nearby','a study resource','a tutorial'])}?",
        lambda: f"Can anyone share the {r.choice(['notes','slides','recording','schedule'])} from {r.choice(['today','yesterday'])}'s {r.choice(['class','meeting','lecture','session'])}?",
        lambda: f"Looking for advice on {r.choice(['choosing a career path','picking a course','improving my skills','studying more effectively'])} — any tips?",
        # ── Gratitude
        lambda: f"Thanks so much for {r.choice(['your help','the notes','the advice','your support','the feedback'])} — really appreciate it!",
        lambda: f"Really grateful for {r.choice(['your help','your time','the recommendation','your support'])}, thank you {r.choice(NAMES)}!",
        lambda: f"Just wanted to say thank you for {r.choice(['everything','your time','your help','your kindness'])}. Means a lot.",
        lambda: f"Thank you {r.choice(NAMES)} for always being so {r.choice(['helpful','kind','supportive','reliable','encouraging'])}!",
        # ── Announcements and reminders
        lambda: f"Reminder: {r.choice(['study group','team meeting','practice','workshop','club event','game night'])} {r.choice(TIME_REFS)} at {r.randint(3,9)}pm!",
        lambda: f"Don't forget about the {r.choice(['quiz','assignment','deadline','meeting','event','game'])} {r.choice(TIME_REFS)}!",
        lambda: f"Heads up — {r.choice(['the deadline','the event','practice','the trip','the meeting'])} is {r.choice(TIME_REFS)}.",
        lambda: f"Just a reminder that {r.choice(['registration','sign-ups','submissions','applications'])} close {r.choice(TIME_REFS)}.",
        # ── Good news
        lambda: f"I'm {r.choice(['so excited','thrilled','over the moon','really happy'])} about the upcoming {r.choice(['concert','trip','game','event','break'])}!",
        lambda: f"Great news — I {r.choice(good_news)}! So happy right now!",
        lambda: f"Just found out we {r.choice(['won','passed','got selected','hit the target','made the team'])}! Team effort everyone!",
        lambda: f"Exciting update: {r.choice(['the project got approved','we got the funding','the event is confirmed','registration is open'])}!",
        # ── Positivity and general
        lambda: f"The {r.choice(['weather','vibe','energy','atmosphere'])} today is {r.choice(POS_ADJ)}, perfect for {r.choice(ACTIVITIES)}!",
        lambda: f"Loving how {r.choice(qualities)} this {r.choice(community)} is — seriously the best!",
        lambda: f"Just {r.choice(['finished my workout','went for a run','did yoga','meditated','went for a walk'])} and feeling {r.choice(POS_ADJ)}!",
        lambda: f"Feeling really {r.choice(positivity)} today. Sending good vibes to everyone!",
        lambda: f"The {r.choice(['sunset','sunrise','view','scenery','sky'])} today was {r.choice(POS_ADJ)}, took so many photos!",
        lambda: f"I love how {r.choice(qualities)} everyone in this {r.choice(community)} is.",
        lambda: f"Looking forward to {r.choice(TIME_REFS)} — it's going to be {r.choice(POS_ADJ)}!",
        lambda: f"This {r.choice(TIME_PERIODS)} has been {r.choice(POS_ADJ)}, hope everyone else is having a good one too!",
        lambda: f"Happy {r.choice(['birthday','anniversary','graduation day'])} to {r.choice(NAMES)}! Hope it's {r.choice(POS_ADJ)}!",
        lambda: f"Wishing everyone a {r.choice(POS_ADJ)} {r.choice(['week','weekend','semester','holiday','day','break'])}!",
        lambda: f"Just wanted to share — this community has been {r.choice(POS_ADJ)} and so {r.choice(qualities)}.",
        lambda: f"Pro tip: {r.choice(SUBJECTS_POS)} is {r.choice(POS_ADJ)} and {r.choice(REACTIONS)} — definitely check it out.",
        lambda: f"Shoutout to everyone who showed up {r.choice(TIME_REFS)}, you were all {r.choice(POS_ADJ)}!",
        lambda: f"The best part of my {r.choice(TIME_PERIODS)} was definitely {r.choice(ACTIVITIES)} — {r.choice(REACTIONS)}.",
    ]

    samples = set()
    attempts = 0
    while len(samples) < n and attempts < n * 40:
        samples.add(random.choice(templates)())
        attempts += 1
    return list(samples)[:n]


# ══════════════════════════════════════════════════════════════════════════════
#  CLASS 2 — HATE_SPEECH
# ══════════════════════════════════════════════════════════════════════════════
def _hs():
    r = random

    ethnic_groups = [
        "People of that ethnic background", "That ethnic group", "Those from that community",
        "Members of that race", "People of that racial background", "That minority group",
        "People from that ancestry", "Those of that heritage", "That demographic group",
        "People with that cultural background",
    ]
    religious_groups = [
        "Followers of that religion", "Members of that faith",
        "Practitioners of that belief system", "That religious group",
        "People of that faith", "Those who follow that religion",
        "Believers of that doctrine", "That religious community",
    ]
    national_groups = [
        "People from that country", "Those immigrants", "Foreign nationals",
        "People from that region", "Those coming from overseas",
        "Migrants from that part of the world", "People from that background",
        "Those who moved here from abroad", "Outsiders from that country",
        "People of that nationality",
    ]
    gender_groups = [
        "Women", "Females", "Girls in the workplace",
        "Women in leadership", "Females in that field",
    ]
    orientation_groups = [
        "LGBTQ people", "Gay people", "That sexual minority group",
        "People of that orientation", "Those with that lifestyle",
        "People who identify that way",
    ]

    neg_ethnic = [
        "are all criminals and cannot be trusted",
        "are a drain on society and contribute nothing",
        "are inferior and have always been",
        "do not belong in civilized society",
        "are responsible for most of the crime here",
        "are genetically predisposed to failure",
        "have a culture of violence and corruption",
        "are fundamentally dishonest by nature",
        "will always be a burden on the rest of us",
        "are taking opportunities that belong to others",
        "are biologically incapable of success",
        "have a criminal mindset passed down through generations",
    ]
    neg_religious = [
        "is a violent cult that promotes hatred",
        "is incompatible with our way of life",
        "promotes terrorism and should be outlawed",
        "is destroying our values from within",
        "is nothing but a dangerous ideology",
        "cannot be trusted and should be expelled",
        "is a threat to national security",
        "secretly hates everyone who is different",
        "is fundamentally opposed to democracy",
        "has no place in a modern society",
    ]
    neg_national = [
        "are ruining our culture and stealing our jobs",
        "should be deported immediately regardless of status",
        "are a threat to national security and public safety",
        "are parasites living off taxpayer money",
        "are bringing disease and crime to our streets",
        "do not share our values and never will",
        "are too different to ever integrate properly",
        "are diluting our national identity",
        "have no right to be in this country",
        "are undermining everything we have built",
        "should never have been allowed in",
        "will never truly belong here",
    ]
    neg_gender = [
        "are too emotional to be in leadership roles",
        "should stay at home instead of competing with men",
        "are naturally less capable in technical fields",
        "do not belong in positions of authority",
        "are biologically inferior when it comes to logic",
        "are weakening every institution they join",
        "should focus on traditional roles only",
        "are not suited for demanding careers",
    ]
    neg_orientation = [
        "are mentally ill and need to be cured",
        "are an abomination against the natural order",
        "are destroying the institution of marriage",
        "are corrupting children and society",
        "should not be allowed to exist openly in public",
        "are a threat to family values and tradition",
        "should be kept away from impressionable youth",
        "have no place in a decent society",
    ]

    action_phrases = [
        "I completely agree — they should be expelled.",
        "Something needs to be done to remove them from our society.",
        "They are the root cause of all our problems.",
        "Society would be far better without them.",
        "We need to stand up against this invasion.",
        "They are replacing us and nobody seems to care.",
        "The sooner they are gone, the better for everyone.",
    ]
    framing = [
        "It is just a fact that", "Everyone knows that",
        "The truth is that", "People need to wake up and realize that",
        "It has always been true that", "Statistics clearly show that",
        "It is simply undeniable that", "You cannot argue with the fact that",
    ]

    templates = [
        # Ethnic discrimination
        lambda: f"{r.choice(ethnic_groups)} {r.choice(neg_ethnic)}.",
        lambda: f"{r.choice(framing)} {r.choice(ethnic_groups).lower()} {r.choice(neg_ethnic)}.",
        lambda: f"{r.choice(ethnic_groups)} have always been like this — {r.choice(neg_ethnic[3:])}.",
        lambda: f"Let us be honest: {r.choice(ethnic_groups).lower()} {r.choice(neg_ethnic)}.",
        lambda: f"Nobody wants to say it but {r.choice(ethnic_groups).lower()} {r.choice(neg_ethnic)}.",
        # Religious discrimination
        lambda: f"{r.choice(religious_groups)} {r.choice(neg_religious)}.",
        lambda: f"{r.choice(framing)} {r.choice(religious_groups).lower()} {r.choice(neg_religious)}.",
        lambda: f"The problem with {r.choice(religious_groups).lower()} is that it {r.choice(neg_religious[2:])}.",
        lambda: f"Anyone who does not see that {r.choice(religious_groups).lower()} {r.choice(neg_religious)} is blind.",
        # National/immigration discrimination
        lambda: f"{r.choice(national_groups)} {r.choice(neg_national)}.",
        lambda: f"{r.choice(framing)} {r.choice(national_groups).lower()} {r.choice(neg_national)}.",
        lambda: f"Wake up — {r.choice(national_groups).lower()} {r.choice(neg_national)}.",
        lambda: f"The reality is that {r.choice(national_groups).lower()} {r.choice(neg_national)}.",
        lambda: f"Open your eyes: {r.choice(national_groups).lower()} {r.choice(neg_national)}.",
        # Gender discrimination
        lambda: f"{r.choice(gender_groups)} {r.choice(neg_gender)}.",
        lambda: f"{r.choice(framing)} {r.choice(gender_groups).lower()} {r.choice(neg_gender)}.",
        lambda: f"The truth nobody wants to say: {r.choice(gender_groups).lower()} {r.choice(neg_gender)}.",
        lambda: f"Science proves it — {r.choice(gender_groups).lower()} {r.choice(neg_gender)}.",
        # Orientation discrimination
        lambda: f"{r.choice(orientation_groups)} {r.choice(neg_orientation)}.",
        lambda: f"{r.choice(framing)} {r.choice(orientation_groups).lower()} {r.choice(neg_orientation)}.",
        lambda: f"Traditional values are clear: {r.choice(orientation_groups).lower()} {r.choice(neg_orientation)}.",
        # Compound templates
        lambda: f"{r.choice(ethnic_groups)} {r.choice(neg_ethnic)}. {r.choice(action_phrases)}",
        lambda: f"{r.choice(national_groups)} {r.choice(neg_national)}. {r.choice(action_phrases)}",
        lambda: f"{r.choice(religious_groups)} {r.choice(neg_religious)}. {r.choice(action_phrases)}",
        lambda: f"{r.choice(framing)} {r.choice(ethnic_groups).lower()} {r.choice(neg_ethnic)}. {r.choice(action_phrases)}",
        # Mixed group targeting
        lambda: f"Both {r.choice(ethnic_groups).lower()} and {r.choice(national_groups).lower()} {r.choice(neg_ethnic)}.",
        lambda: f"{r.choice(national_groups)} and {r.choice(religious_groups).lower()} {r.choice(neg_national)}.",
        # Calls for exclusion
        lambda: f"We need to keep {r.choice(ethnic_groups).lower()} out — they {r.choice(neg_ethnic)}.",
        lambda: f"Why do we keep allowing {r.choice(national_groups).lower()} in when they {r.choice(neg_national)}?",
        lambda: f"It is time to stop tolerating {r.choice(religious_groups).lower()} that {r.choice(neg_religious[2:])}.",
        lambda: f"How long before we admit that {r.choice(orientation_groups).lower()} {r.choice(neg_orientation)}?",
    ]

    samples = set()
    attempts = 0
    while len(samples) < n and attempts < n * 40:
        samples.add(r.choice(templates)())
        attempts += 1
    return list(samples)[:n]


# ══════════════════════════════════════════════════════════════════════════════
#  CLASS 3 — HARASSMENT
# ══════════════════════════════════════════════════════════════════════════════
def _harass():
    r = random

    appearance = [
        "so ugly it hurts to look at you", "physically repulsive to everyone around you",
        "the worst looking person I have ever seen", "impossible to look at without cringing",
        "embarrassing to be seen with in public",
    ]
    intelligence = [
        "absolutely brain dead", "the dumbest person I have ever encountered",
        "too stupid to function in normal society", "aggressively and willfully stupid",
        "incapable of a single intelligent thought",
    ]
    worth = [
        "completely worthless to everyone around you", "a total waste of space and oxygen",
        "contributing absolutely nothing to anyone or anything",
        "a burden on every person who knows you",
        "the most irrelevant person I have ever had the misfortune of meeting",
    ]
    character = [
        "a genuinely terrible person", "deeply dishonest and manipulative",
        "one of the most unpleasant people I have ever encountered",
        "repulsive inside and out", "everything that is wrong with your generation",
    ]
    social = [
        "nobody likes you and everyone tolerates you out of pity",
        "everyone talks about how pathetic you are behind your back",
        "no one wants to spend time with you and they never will",
        "every person who meets you ends up regretting it",
        "people count down the seconds until you leave the room",
    ]
    consequence_self = [
        "and you are too stupid to even realize it",
        "and everyone around you already knows it",
        "and no amount of effort will ever change that",
        "and you will never be anything more than that",
        "and that is never going to change",
    ]
    direct_attacks = [
        "You make every single room worse the moment you walk in.",
        "I genuinely cannot stand the sight or sound of you.",
        "Your presence makes everyone around you deeply uncomfortable.",
        "I have never met anyone as deeply unpleasant as you.",
        "You are the kind of person decent people warn their friends about.",
        "No one will ever love someone as genuinely awful as you.",
        "You should be ashamed to show your face in public.",
        "Everyone laughs at you behind your back and you have no idea.",
        "The kindest thing you could do is never speak again.",
        "Your entire life is a joke and you are too clueless to see it.",
        "I feel genuine pity for anyone who has to interact with you.",
        "You are a burden on every single person who crosses your path.",
        "I do not understand how you can look yourself in the mirror.",
        "You have never had a single original thought in your entire life.",
        "You are the textbook definition of a complete failure as a human.",
    ]
    openers = [
        "You are", "Let's be real — you are", "Everyone knows you are",
        "Face it — you are", "The truth is you are", "I cannot believe how",
        "It is genuinely shocking how",
    ]

    templates = [
        # Appearance attacks
        lambda: f"You are {r.choice(appearance)} and you know it.",
        lambda: f"{r.choice(openers)} {r.choice(appearance)}.",
        lambda: f"I have never seen someone as {r.choice(['ugly','pathetic','repulsive','revolting'])} as you.",
        lambda: f"Honestly {r.choice(appearance)} — I am sorry but it is just true.",
        # Intelligence attacks
        lambda: f"You are {r.choice(intelligence)} and everyone can see it.",
        lambda: f"{r.choice(openers)} {r.choice(intelligence)}.",
        lambda: f"I genuinely cannot believe how {r.choice(['stupid','dumb','clueless','oblivious'])} you are.",
        lambda: f"You are {r.choice(intelligence)} {r.choice(consequence_self)}.",
        # Worth attacks
        lambda: f"You are {r.choice(worth)}.",
        lambda: f"{r.choice(openers)} {r.choice(worth)}.",
        lambda: f"Face it — you are {r.choice(worth)} {r.choice(consequence_self)}.",
        lambda: f"Everyone who knows you thinks you are {r.choice(worth)}.",
        # Character attacks
        lambda: f"You are {r.choice(character)} {r.choice(consequence_self)}.",
        lambda: f"{r.choice(openers)} {r.choice(character)}.",
        lambda: f"I have never met someone who is {r.choice(character)} the way you are.",
        # Social attacks
        lambda: f"The truth is {r.choice(social)}.",
        lambda: f"You need to accept that {r.choice(social)}.",
        lambda: f"Everyone can see that {r.choice(social)} {r.choice(consequence_self)}.",
        # Combined attacks
        lambda: f"You are {r.choice(appearance)} and {r.choice(intelligence)}.",
        lambda: f"You are {r.choice(worth)} and {r.choice(social)}.",
        lambda: f"You are {r.choice(intelligence)} and {r.choice(character)}.",
        lambda: f"Not only are you {r.choice(appearance)}, you are also {r.choice(intelligence)}.",
        lambda: f"You are {r.choice(worth)}. {r.choice(social).capitalize()}.",
        # Direct attack statements
        lambda: r.choice(direct_attacks),
        lambda: f"{r.choice(direct_attacks)} {r.choice(['And everyone agrees.','It is just a fact.','Deal with it.'])}",
        # Comparative insults
        lambda: f"I have seen better looking things at the bottom of a trash can than you.",
        lambda: f"You are less useful than a broken pencil and twice as {r.choice(['pointless','irritating','useless','dull'])}.",
        lambda: f"Even {r.choice(['a rock','an empty chair','a doorknob','a cardboard cutout'])} has more {r.choice(['personality','value','charisma','intelligence'])} than you.",
        # Existential attacks
        lambda: f"The world would be genuinely better without you in it and everyone knows it.",
        lambda: f"No amount of effort will ever make you likeable or worthwhile to anyone.",
        lambda: f"You are so deeply {r.choice(['annoying','irritating','insufferable','unbearable','pathetic'])} that people actively avoid you.",
        lambda: f"Everything about you — {r.choice(['your voice','your attitude','your personality','your presence'])} — is {r.choice(['unbearable','irritating','repulsive','awful'])}.",
        lambda: f"You are genuinely one of the most {r.choice(['unpleasant','pathetic','worthless','insufferable'])} people anyone has ever had to deal with.",
        lambda: f"I feel sorry for anyone unfortunate enough to know you — you bring nothing but misery.",
        lambda: f"Your {r.choice(['attitude','personality','behavior','presence'])} is {r.choice(['repulsive','insufferable','embarrassing','revolting'])} to everyone around you.",
        lambda: f"Nobody wants to hear what you have to say — just stop talking forever.",
        lambda: f"You are so {r.choice(['clueless','oblivious','ignorant','delusional'])} it is genuinely painful to watch you function.",
        lambda: f"I cannot believe someone like you actually exists and interacts with real people.",
    ]

    samples = set()
    attempts = 0
    while len(samples) < n and attempts < n * 40:
        samples.add(r.choice(templates)())
        attempts += 1
    return list(samples)[:n]


# ══════════════════════════════════════════════════════════════════════════════
#  CLASS 4 — CYBERBULLYING
# ══════════════════════════════════════════════════════════════════════════════
def _cyber():
    r = random

    threats_direct = [
        "make your life at school absolutely miserable",
        "make sure you regret ever crossing me",
        "ruin your reputation completely",
        "destroy everything you care about",
        "make every single day here a nightmare for you",
        "ensure you are completely alone by the end of the week",
        "turn everyone against you one by one",
        "hunt you down and make you pay for this",
        "expose you to everyone and destroy your life",
    ]
    leverage = [
        "I have your private messages and I will share them with everyone",
        "I have screenshots of everything you have said",
        "I have photos of you that you do not want people to see",
        "I know your secrets and I am ready to tell everyone",
        "I have access to your accounts and I can post whatever I want",
        "I have been recording our conversations",
        "I know where you live and who your family is",
    ]
    demands = [
        "give me what I asked for",
        "do exactly what I tell you",
        "do my homework for me",
        "stop talking to them immediately",
        "give me your lunch money every day",
        "follow all my accounts right now",
        "send me your login credentials",
        "stay away from our friend group",
        "publicly apologize to me",
        "leave the group immediately",
    ]
    exclusion = [
        "you are not welcome here anymore and everyone agrees",
        "we have decided to cut you off from the group permanently",
        "nobody wants you around and that is never going to change",
        "you are banned from sitting with us and do not even try",
        "everyone has voted and you are out — it is final",
        "we have all agreed to ignore your existence from now on",
        "you are no longer part of this friend group starting today",
    ]
    humiliation = [
        "I am going to post your embarrassing photos online for everyone to see",
        "I will tell everyone at school your most humiliating secret",
        "I am going to show the whole class those messages you sent",
        "I will make sure everyone knows what you really did",
        "I am going to share everything I know about you publicly",
        "I will announce your private business to the entire school",
    ]
    online_threats = [
        "I will get everyone to mass report your accounts until you get banned",
        "I am going to hack into your profiles and post whatever I want",
        "I will create fake accounts pretending to be you",
        "I am going to spam you with messages until you delete everything",
        "I will leave fake negative reviews on everything connected to you",
        "I will get all my followers to attack your pages",
    ]
    warn_phrases = [
        "You better not tell anyone about this or things will get much worse.",
        "Do not even think about going to a teacher — that will only make it worse.",
        "If you tell anyone, you will regret it deeply.",
        "Report me and see what happens — I dare you.",
        "Try to escape this and see what I do next.",
    ]
    conditional = [
        f"Do {r.choice(demands)} or I will {r.choice(threats_direct)}.",
        f"You have 24 hours to {r.choice(demands)} or I will {r.choice(threats_direct)}.",
        f"Either {r.choice(demands)} or I will {r.choice(threats_direct)} — your choice.",
    ]
    time_pressure = [
        "You have until tomorrow to decide.", "Clock is ticking — decide now.",
        "You have one hour.", "Do it today or face the consequences.",
        "This is your last warning.", "I am not playing around this time.",
    ]

    templates = [
        # Direct threats
        lambda: f"I am going to {r.choice(threats_direct)} starting right now.",
        lambda: f"You are going to regret this — I will {r.choice(threats_direct)}.",
        lambda: f"Watch your back because I will {r.choice(threats_direct)}.",
        lambda: f"You think you can get away with this? I will {r.choice(threats_direct)}.",
        lambda: f"Cross me again and I will {r.choice(threats_direct)}.",
        # Leverage / blackmail
        lambda: f"{r.choice(leverage)}, so you better do what I say.",
        lambda: f"{r.choice(leverage)}. Do what I want or I will use it.",
        lambda: f"I am warning you — {r.choice(leverage)} and I will not hesitate.",
        lambda: f"Did you forget that {r.choice(leverage)}? Better cooperate.",
        # Conditional threats (do X or I'll Y)
        lambda: f"Do {r.choice(demands)} or I will {r.choice(threats_direct)}.",
        lambda: f"You have 24 hours to {r.choice(demands)} or I will {r.choice(threats_direct)}.",
        lambda: f"Either {r.choice(demands)} or I will {r.choice(threats_direct)} — your choice.",
        lambda: f"{r.choice(leverage)}. {r.choice(demands).capitalize()} or everyone finds out.",
        lambda: f"I am telling you once: {r.choice(demands)} or I start sharing what I have.",
        # Social exclusion
        lambda: f"Just so you know — {r.choice(exclusion)}.",
        lambda: f"We met and decided: {r.choice(exclusion)}.",
        lambda: f"Official notice: {r.choice(exclusion)}.",
        lambda: f"Get used to being alone because {r.choice(exclusion)}.",
        lambda: f"You should know that {r.choice(exclusion)} — do not bother showing up.",
        # Humiliation threats
        lambda: f"{r.choice(humiliation)} unless you do what I say.",
        lambda: f"Do {r.choice(demands)} or {r.choice(humiliation).lower()}.",
        lambda: f"I am giving you one chance — {r.choice(demands)} or {r.choice(humiliation).lower()}.",
        lambda: f"Your reputation is in my hands. {r.choice(humiliation)}.",
        # Online harassment
        lambda: f"{r.choice(online_threats)} if you do not comply.",
        lambda: f"I already started — {r.choice(online_threats).lower()}.",
        lambda: f"You have no idea what I can do online. {r.choice(online_threats)}.",
        # Warning not to tell
        lambda: r.choice(warn_phrases),
        lambda: f"{r.choice(warn_phrases)} {r.choice(time_pressure)}",
        # Combined patterns
        lambda: f"{r.choice(leverage)}. {r.choice(humiliation)}. {r.choice(warn_phrases)}",
        lambda: f"I am going to {r.choice(threats_direct)}. {r.choice(online_threats)}.",
        lambda: f"You are out — {r.choice(exclusion)}. {r.choice(warn_phrases)}",
        lambda: f"Do {r.choice(demands)}. {r.choice(time_pressure)} Otherwise I will {r.choice(threats_direct)}.",
        # Manipulation
        lambda: f"I control what everyone thinks of you at this school, so you better listen to me.",
        lambda: f"I have been telling everyone lies about you and I will keep going unless you cooperate.",
        lambda: f"Your social life is completely in my hands — {r.choice(demands)} or lose everything.",
        lambda: f"I will make sure you have no friends left here if you keep this up.",
        lambda: f"Everyone will turn on you the moment I say the word — so {r.choice(demands)}.",
        lambda: f"I am going to make your life impossible until you {r.choice(demands)}.",
        lambda: f"I will follow you and make your life hell until you learn to respect me.",
        lambda: f"You cannot escape this — I will {r.choice(threats_direct)} no matter what you do.",
        lambda: f"We created a group chat specifically to coordinate how to make your life miserable.",
        lambda: f"I know every single one of your friends and I will turn them all against you.",
    ]

    samples = set()
    attempts = 0
    while len(samples) < n and attempts < n * 40:
        try:
            samples.add(r.choice(templates)())
        except Exception:
            pass
        attempts += 1
    return list(samples)[:n]


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("Generating dataset...")
    print(f"  Target per class : {TARGET}")

    not_cb   = _ncb()
    print(f"  not_cyberbullying : {len(not_cb)} samples")
    hate     = _hs()
    print(f"  hate_speech       : {len(hate)} samples")
    harass   = _harass()
    print(f"  harassment        : {len(harass)} samples")
    cyber    = _cyber()
    print(f"  cyberbullying     : {len(cyber)} samples")

    rows = (
        [(t, "not_cyberbullying") for t in not_cb] +
        [(t, "hate_speech")       for t in hate  ] +
        [(t, "harassment")        for t in harass] +
        [(t, "cyberbullying")     for t in cyber ]
    )
    random.shuffle(rows)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)

    total = len(rows)
    print(f"\nSaved {total} rows → {OUTPUT}")
    print("Done! Run train.py next to retrain models on the full dataset.\n")


if __name__ == "__main__":
    main()
