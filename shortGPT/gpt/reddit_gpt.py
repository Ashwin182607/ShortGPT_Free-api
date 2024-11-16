from shortGPT.gpt import gpt_utils
import random
import json
from enum import Enum

class RedditStoryType(Enum):
    AITA = "AmITheAsshole"  # Am I The Asshole stories
    TIFU = "TIFU"  # Today I Fucked Up stories
    MALICIOUS_COMPLIANCE = "MaliciousCompliance"  # Malicious compliance stories
    PETTY_REVENGE = "PettyRevenge"  # Petty revenge stories
    RELATIONSHIP = "Relationship"  # Relationship advice/stories
    CONFESSION = "Confession"  # Confessions
    LIFE_PRO_TIP = "LifeProTips"  # Life Pro Tips
    NOSLEEP = "NoSleep"  # Horror stories
    CHOOSING_BEGGARS = "ChoosingBeggars"  # Choosing beggars stories
    ENTITLED_PARENTS = "EntitledParents"  # Entitled parents stories

def generateRedditPostMetadata(title, story_type=None):
    """Generate Reddit post metadata with subreddit-specific formatting."""
    name = generateUsername()
    if title and title[0] == '"':
        title = title.replace('"', '')
        
    # Format title based on story type
    if story_type:
        if story_type == RedditStoryType.AITA:
            title = f"AITA for {title.lower()}"
        elif story_type == RedditStoryType.TIFU:
            title = f"TIFU by {title.lower()}"
        elif story_type == RedditStoryType.LIFE_PRO_TIP:
            title = f"LPT: {title}"
        elif story_type == RedditStoryType.NOSLEEP:
            title = f"{title} | r/nosleep"
            
    n_months = random.randint(1, 11)
    header = f"{name} - {n_months} months ago"
    
    # Adjust upvotes and comments based on story type
    base_comments = random.random() * 10 + 2
    base_upvotes = base_comments * (1.2 + random.random() * 2.5)
    
    # Popular subreddits get more engagement
    if story_type in [RedditStoryType.AITA, RedditStoryType.TIFU, RedditStoryType.NOSLEEP]:
        base_comments *= 2
        base_upvotes *= 2
    
    return title, header, f"{base_comments:.1f}k", f"{base_upvotes:.1f}k"

def getInterestingRedditQuestion(story_type=None):
    """Get an interesting Reddit question/prompt based on story type."""
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_generate_question.yaml')
    
    if story_type:
        system += f"\nThis should be a {story_type.value} style post."
        
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat}
    ]
    response = gpt_utils.gpt_completion(messages=messages, temperature=1.08)
    return response.choices[0].message.content

def createRedditScript(question, story_type=None):
    """Create a Reddit script with specific story type formatting."""
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_generate_script.yaml')
    
    if story_type:
        system += f"\nThis should follow the style of r/{story_type.value} posts."
        if story_type == RedditStoryType.AITA:
            system += "\nInclude a clear conflict and moral dilemma. End with 'AITA?'"
        elif story_type == RedditStoryType.TIFU:
            system += "\nDescribe an embarrassing or unfortunate situation. Include a TL;DR at the end."
        elif story_type == RedditStoryType.NOSLEEP:
            system += "\nMake it creepy and suspenseful. Follow r/nosleep rules of everything being treated as true."
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(question=question)}
    ]
    response = gpt_utils.gpt_completion(messages=messages, temperature=1.08)
    
    result = response.choices[0].message.content
    if story_type == RedditStoryType.TIFU:
        if "TL;DR" not in result:
            result += "\n\nTL;DR: " + question
    
    return f"Reddit, {question} {result}"

def getRealisticness(text, story_type=None):
    """Check how realistic the story is, considering the subreddit context."""
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_filter_realistic.yaml')
    
    if story_type:
        system += f"\nConsider this in the context of r/{story_type.value} posts."
        if story_type == RedditStoryType.NOSLEEP:
            system += "\nHorror stories can be supernatural but should maintain internal consistency."
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat.format(input=text)}
    ]
    
    while True:
        try:
            response = gpt_utils.gpt_completion(messages=messages, temperature=1)
            result = response.choices[0].message.content
            score = json.loads(result)['score']
            # Adjust score based on story type
            if story_type == RedditStoryType.NOSLEEP:
                score = min(score * 1.2, 1.0)  # More lenient for horror stories
            return score
        except Exception as e:
            print("Error in getRealisticness", e.args[0])

def generateUsername():
    """Generate a Reddit-style username."""
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/reddit_username.yaml')
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": chat}
    ]
    response = gpt_utils.gpt_completion(messages=messages, temperature=1.2)
    return response.choices[0].message.content.replace("u/", "")

def getStoryTypeFromText(text):
    """Detect the most suitable story type based on content."""
    chat = """Analyze this text and determine which subreddit it best fits into. Choose from:
    - AmITheAsshole (moral dilemmas)
    - TIFU (mistakes and their consequences)
    - MaliciousCompliance (following rules to spite someone)
    - PettyRevenge (minor acts of revenge)
    - Relationship (relationship issues)
    - Confession (personal confessions)
    - LifeProTips (helpful advice)
    - NoSleep (horror stories)
    - ChoosingBeggars (entitled customers/people)
    - EntitledParents (stories about entitled parents)
    
    Text to analyze: {text}
    """
    
    messages = [
        {"role": "system", "content": "You are a Reddit content analyzer. Respond with just the subreddit name."},
        {"role": "user", "content": chat.format(text=text)}
    ]
    
    response = gpt_utils.gpt_completion(messages=messages, temperature=0.3)
    result = response.choices[0].message.content.strip()
    
    try:
        return RedditStoryType[result.upper()]
    except KeyError:
        return None  # Default to None if no clear match
