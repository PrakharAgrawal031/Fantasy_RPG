import spacy

nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "attack": ["attack", "hit", "strike", "fight"],
    "run": ["run", "escape", "flee"],
    "use_item": ["use", "drink", "consume", "potion"],
    "explore": ["explore", "go", "walk", "travel", "move"],
    "rest": ["rest", "sleep", "heal"],
    "inventory": ["inventory", "bag", "items"],
    "equip": ["equip", "wear", "put on"],
    "exit": ["exit", "quit", "leave", "save"],
    "information": ["information", "show", "info"]
}

def get_intent(user_input):
    doc = nlp(user_input.lower())
    for token in doc:
        for intent, keywords in INTENT_KEYWORDS.items():
            if token.text in keywords:
                return intent
    return "unknown"
