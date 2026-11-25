import feedparser
import requests
import json
import random
import re

from pathlib import Path
from datetime import datetime

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

SITE_NAME = "☕ STW Coffee Club"

TODAY = datetime.now().strftime(
    "%A, %d %B %Y"
)

LAT = 51.3618
LON = -0.1945

FEEDS = {

    "surrey":
    "https://www.getsurrey.co.uk/?service=rss",

    "uk":
    "https://feeds.bbci.co.uk/news/uk/rss.xml",

    "india":
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",

    "money":
    "https://www.moneysavingexpert.com/feed/latest/",

    "nhs":
    "https://www.england.nhs.uk/feed/",

    "good":
    "https://www.goodnewsnetwork.org/feed/"
}

with open(
    "community.json",
    encoding="utf8"
) as f:

    DATA = json.load(f)


def clean(text):

    if not text:
        return ""

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    return text.strip()

def why_it_matters(summary):

    summary = clean(summary)

    if not summary:
        return "A useful update for our community."

    first_sentence = summary.split(".")[0].strip()

    if len(first_sentence) > 180:
        first_sentence = first_sentence[:180]

    return f"💡 {first_sentence}."

def random_fact():

    try:

        data = requests.get(
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            timeout=10
        ).json()

        return data["text"]

    except:

        return random.choice(
            DATA["numbers"]
        )
def get_story(url):

    try:

        feed = feedparser.parse(url)

        if not feed.entries:
            return None

        item = feed.entries[0]

        return {

            "title": item.title,

            "summary": clean(
                getattr(
                    item,
                    "summary",
                    ""
                )
            )[:250],

            "link": getattr(
                item,
                "link",
                ""
            )

        }

    except Exception:

        return None

def closing_message():
    messages = [
        "The laundry can wait. Your peace of mind comes first.",
        "A cup of chai and a good night's sleep solve many problems.",
        "Small moments with loved ones become treasured memories.",
        "You are doing better than you think."
    ]

    return random.choice(messages)

def get_stories(url, count=3):
    try:
        feed = feedparser.parse(url)
        results = []

        for item in feed.entries[:count]:
            results.append({
                "title": item.title,
                "summary": clean(
                    getattr(item, "summary", "")
                ),
                "link": getattr(item, "link", "")
            })

        return results

    except Exception:
        return []
def weather():

    try:

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={LAT}"
            f"&longitude={LON}"
            "&current=temperature_2m"
        )

        data = requests.get(
            url,
            timeout=10
        ).json()

        temp = round(
            data["current"]["temperature_2m"]
        )

        return (
            f"{temp}°C in Sutton today. "
            "Perfect weather for a warm chai."
        )

    except:

        return (
            "Weather currently unavailable."
        )

def history_today():

    try:

        data = requests.get(
            "https://history.muffinlabs.com/date",
            timeout=10
        ).json()

        event = random.choice(
            data["data"]["Events"]
        )

        return (
            event["year"],
            event["text"]
        )

    except:

        return None,None
def gbp_inr():

    try:

        data = requests.get(
            "https://open.er-api.com/v6/latest/GBP",
            timeout=10
        ).json()

        return round(
            data["rates"]["INR"],
            2
        )

    except:

        return None
def dinner_idea():

    try:

        meal = requests.get(
            "https://www.themealdb.com/api/json/v1/1/random.php",
            timeout=10
        ).json()["meals"][0]

        return (
            meal["strMeal"],
            meal["strArea"]
        )

    except:

        return (
            "Vegetable Pulao",
            "Indian"
        )


def card(title, content):

    return f"""
    <div class="card">
        <h2>{title}</h2>
        {content}
    </div>
    """


surrey = get_story(FEEDS["surrey"])
top_uk = get_stories(
    FEEDS["uk"],
    3
)
india = get_story(FEEDS["india"])
money = get_story(FEEDS["money"])
nhs = get_story(FEEDS["nhs"])
good = get_story(FEEDS["good"])

meal_name, meal_area = dinner_idea()
rate = gbp_inr()
body = ""

body += card(
    "🌸 Morning Dashboard",
    f"""
    <div class="mini-grid">

        <div class="mini-tile">
            <h4>😊 Smile</h4>
            {random.choice(DATA['smiles'])}
        </div>

        <div class="mini-tile">
            <h4>🌸 Affirmation</h4>
            {random.choice(DATA['affirmations'])}
        </div>

        <div class="mini-tile">
            <h4>❤️ Self Care</h4>
            {random.choice(DATA['selfcare'])}
        </div>

        <div class="mini-tile">
            <h4>🇬🇧 UK Tip</h4>
            {random.choice(DATA['britain_tips'])}
        </div>

        <div class="mini-tile">
            <h4>💷 Money</h4>
            {random.choice(DATA['money_minute'])}
        </div>

        <div class="mini-tile">
            <h4>👩‍👧 Mum's Corner</h4>
            {random.choice(DATA['mum_corner'])}
        </div>

        <div class="mini-tile">
            <h4>🧠 Learn</h4>
            {random.choice(DATA['learning'])}
        </div>

        <div class="mini-tile">
            <h4>🇮🇳 Home</h4>
            {random.choice(DATA['india_home'])}
        </div>

        <div class="mini-tile">
            <h4>📚 Skill</h4>
            {random.choice(DATA['skill_of_day'])}
        </div>

        <div class="mini-tile">
            <h4>💝 Kindness</h4>
            {random.choice(DATA['kindness'])}
        </div>

    </div>
    """
)

if rate:
    body += card(
        "💷 Exchange Rate",
        f"""
        <div class="highlight">
        £1 = ₹{rate}
        <br><br>
        Useful for sending money to family in India.
        </div>
        """
    )

body += card(
    "🌤 Today's Snapshot",
    f"""
    <div class="mini-grid">

        <div class="mini-tile">
        <h4>🌤 Weather</h4>
        {weather()}
        </div>

        <div class="mini-tile">
        <h4>😄 UK-Indian Moment</h4>
        {random.choice(DATA['uk_indian_moments'])}
        </div>

        <div class="mini-tile">
        <h4>🤯 Did You Know?</h4>
        {random_fact()}
        </div>

        <div class="mini-tile">
        <h4>💷 Worth Knowing</h4>
        {random.choice(DATA['worth_knowing'])}
        </div>

    </div>
    """
)

if nhs:
    body += card(
        "🏥 Health & Wellbeing",
        f"""
        <h3>{nhs['title']}</h3>

        <div class="highlight">
        {why_it_matters(nhs['summary'])}
        </div>

        <a class="button"
        href="{nhs['link']}"
        target="_blank">
        Read More →
        </a>
        """
    )

if surrey:
    body += card(
        "📍 Around Sutton",
        f"""
        <h3>{surrey['title']}</h3>

        <div class="highlight">
        {why_it_matters(surrey['summary'])}
        </div>

        <a class="button"
        href="{surrey['link']}"
        target="_blank">
        Read Story →
        </a>
        """
    )

tiles = ""

for story in top_uk:
    tiles += f"""
    <div class="news-tile">
        <h4>{story['title']}</h4>

        <p>
        {why_it_matters(story['summary'])}
        </p>

        <a
        class="button"
        href="{story['link']}"
        target="_blank">
        Read →
        </a>
    </div>
    """

body += card(
    "🔥 What's Hot Today",
    f"""
    <div class="tile-grid">
    {tiles}
    </div>
    """
)

if india:
    body += card(
        "🇮🇳 Back Home In India",
        f"""
        <h3>{india['title']}</h3>

        <div class="highlight">
        {why_it_matters(india['summary'])}
        </div>

        <a class="button"
        href="{india['link']}"
        target="_blank">
        Read Story →
        </a>
        """
    )

body += card(
    "☕ Chai Chat",
    f"""
    <div class="chai-box">
    <strong>Today's Question</strong>

    <br><br>

    {random.choice(DATA['questions'])}

    </div>
    """
)

body += card(
    "🎯 Tiny Challenge",
    f"<p>{random.choice(DATA['challenges'])}</p>"
)

body += card(
    "🌈 Thought For Today",
    f"<p>{random.choice(DATA['thoughts'])}</p>"
)

body += card(
    "🌈 Until Tomorrow",
    f"""
    <div class="highlight">
    {closing_message()}
    <br><br>
    See you tomorrow ☕
    </div>
    """
)

html = """
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>{site}</title>

<style>

:root {{

    --lavender:#9b7edc;
    --lavender-dark:#7b5fc4;
    --gold:#d4a64a;
    --gold-light:#f5d98f;

    --cream:#fffaf2;
    --card:#ffffff;

    --text:#2f2f2f;
    --muted:#6b6b6b;

    --shadow:
    0 6px 18px rgba(
    0,0,0,.08
    );

}}

body {{

    margin:0;

    background:
    linear-gradient(
    180deg,
    #fffcf7,
    #f8f2ff
    );

    color:var(--text);

    font-family:
    "Segoe UI",
    Arial,
    sans-serif;

    line-height:1.7;
}}

.container{{

    max-width:820px;

    margin:auto;

    padding:20px;
}}

.hero{{

    background:
    linear-gradient(
    135deg,
    var(--lavender),
    #c7a6ff
    );

    color:white;

    padding:40px;

    border-radius:28px;

    text-align:center;

    box-shadow:var(--shadow);

    margin-bottom:20px;
}}

.hero h1{{

    margin:0;

    font-size:42px;
}}

.card{{

    background:white;

    border-radius:22px;

    padding:24px;

    margin-bottom:18px;

    box-shadow:var(--shadow);

    border:1px solid #f0ebf8;
}}

.card h2{{

    margin-top:0;

    color:var(--lavender-dark);

    border-bottom:
    2px solid #f1ebfb;

    padding-bottom:10px;
}}

.highlight{{

    background:
    linear-gradient(
    90deg,
    #fff6de,
    #fffdf6
    );

    border-left:
    6px solid
    var(--gold);

    padding:16px;

    border-radius:12px;
}}

.button{{

    display:inline-block;

    margin-top:15px;

    background:
    linear-gradient(
    135deg,
    var(--gold),
    #f1c15f
    );

    color:#2f2f2f;

    text-decoration:none;

    padding:12px 18px;

    border-radius:10px;

    font-weight:700;
}}

.chai-box{{

    background:
    linear-gradient(
    135deg,
    #fff5fa,
    #ffffff
    );

    border:
    2px dashed
    var(--lavender);

    border-radius:18px;

    padding:18px;
}}

.tile-grid {{

    display:grid;

    grid-template-columns:
    repeat(
    auto-fit,
    minmax(220px,1fr)
    );

    gap:15px;
}}
.mini-grid{{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:12px;
    margin-top:10px;
}}

.mini-tile{{
    background:white;
    border-radius:12px;
    padding:15px;
    border:1px solid #ececec;
    font-size:14px;
    line-height:1.5;
}}

.mini-tile h4{{
    margin-top:0;
    margin-bottom:8px;
    color:#7b5fc4;
}}
.news-tile {{

    background:
    linear-gradient(
    135deg,
    #fff8e8,
    #ffffff
    );

    border-radius:14px;

    padding:15px;

    border:
    1px solid #f1e5c9;
}}
</style>

</head>

<body>

<div class="container">

<div class="hero">

<h1>{site}</h1>

<p>{today}</p>

<p>Learn • Share • Grow</p>

</div>

{body}

</div>

</body>
</html>
""".format(
    site=SITE_NAME,
    today=TODAY,
    body=body
)
html_file = OUTPUT / "newsletter.html"

with open(
    html_file,
    "w",
    encoding="utf8"
) as f:

    f.write(html)
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={
                "width": 1200,
                "height": 5000
            }
        )

        page.goto(
            html_file.resolve().as_uri()
        )

        page.screenshot(
            path=str(
                OUTPUT / "newsletter.png"
            ),
            full_page=True
        )

        browser.close()

    print("✅ newsletter.png generated")

except Exception as e:
    print(
        "❌ PNG generation failed:",
        e
    )
whatsapp = f"""
☕ *STW Coffee Club*
📅 {TODAY}
"""

if nhs:
    whatsapp += f"""

🏥 *Health & Wellbeing*

{nhs['title']}

🔗 {nhs['link']}
"""

if surrey:
    whatsapp += f"""

📍 *Around Sutton*

{surrey['title']}

🔗 {surrey['link']}
"""

for story in top_uk:
    whatsapp += f"""

🇬🇧 *UK Headline*

{story['title']}

🔗 {story['link']}
"""

if india:
    whatsapp += f"""

🇮🇳 *India News*

{india['title']}

🔗 {india['link']}
"""

if money:
    whatsapp += f"""

💷 *Money Saving*

{money['title']}

🔗 {money['link']}
"""

whatsapp += f"""

☕ Chai Chat

{random.choice(DATA['questions'])}

🎯 Challenge

{random.choice(DATA['challenges'])}
"""

with open(
    OUTPUT / "whatsapp_digest.txt",
    "w",
    encoding="utf8"
) as f:

    f.write(whatsapp)

print("✅ newsletter.html generated")
print("✅ whatsapp_digest.txt generated")
