import streamlit as st
import feedparser
import requests
from datetime import datetime
import urllib3
from bs4 import BeautifulSoup

# Suppress SSL warnings for institutional websites
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. THE 100-QUOTE DATABASE ---
QUOTES = [
    {"text": "The first principle is that you must not fool yourself, and you are the easiest person to fool.",
     "author": "Richard Feynman"},
    {"text": "Using evidence and reason to figure out how to benefit others as much as possible.",
     "author": "William MacAskill"},
    {"text": "Intelligence is the ability to process information such that you achieve your goals.",
     "author": "Eliezer Yudkowsky"},
    {"text": "Nature has placed mankind under the governance of two sovereign masters, pain and pleasure.",
     "author": "Jeremy Bentham"},
    {"text": "If you cannot explain it simply, you do not understand it well enough.", "author": "Albert Einstein"},
    {"text": "The most important century is the one we are living in.", "author": "Holden Karnofsky"},
    {"text": "To do more good, we need to think more clearly.", "author": "Julia Galef"},
    {"text": "Nothing in life is to be feared, it is only to be understood.", "author": "Marie Curie"},
    {"text": "The aim of life is to spend it on something that outlasts it.", "author": "William James"},
    {
        "text": "It makes no moral difference whether the person I can help is a neighbor's child ten yards away or a Bengali whose name I shall never know.",
        "author": "Peter Singer"},
    {"text": "The universe is not only queerer than we suppose, but queerer than we can suppose.",
     "author": "J.B.S. Haldane"},
    {"text": "Whatever can be destroyed by the truth should be.", "author": "P.C. Hodgell"},
    {"text": "Everything is complicated if you look at it hard enough.", "author": "Scott Alexander"},
    {"text": "Complexity is not a vice, but a reality to be managed.", "author": "Santa Fe Institute"},
    {"text": "The map is not the territory.", "author": "Alfred Korzybski"},
    {"text": "Somewhere, something incredible is waiting to be known.", "author": "Carl Sagan"},
    {"text": "Suffer more in imagination than in reality.", "author": "Seneca"},
    {"text": "You have power over your mind - not outside events.", "author": "Marcus Aurelius"},
    {"text": "The clearest way into the universe is through a forest wilderness.", "author": "John Muir"},
    {"text": "In wilderness is the preservation of the world.", "author": "Henry David Thoreau"},
    {"text": "The first step in intelligent tinkering is to keep all the pieces.", "author": "Aldo Leopold"},
    {"text": "A system is more than the sum of its parts.", "author": "Donella Meadows"},
    {"text": "Optimism is a strategy for making a better future.", "author": "Noam Chomsky"},
    {"text": "Extraordinary claims require extraordinary evidence.", "author": "Carl Sagan"},
    {"text": "The great difficulty is to keep the realistic and the idealistic in some sort of harmony.",
     "author": "Bertrand Russell"},
    {"text": "We suffer more often in imagination than in reality.", "author": "Seneca"},
    {"text": "What is not good for the beehive cannot be good for the bee.", "author": "Marcus Aurelius"},
    {
        "text": "The only way of discovering the limits of the possible is to venture a little way past them into the impossible.",
        "author": "Arthur C. Clarke"},
    {"text": "The future is already here - it is just not very evenly distributed.", "author": "William Gibson"},
    {"text": "Science is the art of the soluble.", "author": "Peter Medawar"},
    {"text": "One of the penalties of an ecological education is that one lives alone in a world of wounds.",
     "author": "Aldo Leopold"},
    {
        "text": "The sea, the great unifier, is man's only hope. Now, as never before, the old phrase has a literal meaning: we are all in the same boat.",
        "author": "Jacques Yves Cousteau"},
    {"text": "I would rather have questions that cannot be answered than answers that cannot be questioned.",
     "author": "Richard Feynman"},
    {"text": "A ship in port is safe, but that is not what ships are built for.", "author": "Grace Hopper"},
    {
        "text": "The more clearly we can focus our attention on the wonders and realities of the universe about us, the less taste we shall have for destruction.",
        "author": "Rachel Carson"},
    {"text": "Happiness is when what you think, what you say, and what you do are in harmony.",
     "author": "Mahatma Gandhi"},
    {"text": "It always seems impossible until it is done.", "author": "Nelson Mandela"},
    {"text": "The moral arc of the universe is long, but it bends toward justice.", "author": "Martin Luther King Jr."},
    {"text": "Do not judge each day by the harvest you reap but by the seeds that you plant.",
     "author": "Robert Louis Stevenson"},
    {"text": "Life is what happens when you are making other plans.", "author": "John Lennon"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
     "author": "Winston Churchill"},
    {"text": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "author": "Aristotle"},
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"text": "Not all those who wander are lost.", "author": "J.R.R. Tolkien"},
    {"text": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu"},
    {"text": "A person who never made a mistake never tried anything new.", "author": "Albert Einstein"},
    {"text": "Be the change that you wish to see in the world.", "author": "Mahatma Gandhi"},
    {"text": "The mind is everything. What you think you become.", "author": "Buddha"},
    {"text": "An unexamined life is not worth living.", "author": "Socrates"},
    {"text": "I think, therefore I am.", "author": "René Descartes"},
    {"text": "Man is condemned to be free.", "author": "Jean-Paul Sartre"},
    {"text": "One cannot step twice in the same river.", "author": "Heraclitus"},
    {"text": "Reason is, and ought only to be the slave of the passions.", "author": "David Hume"},
    {"text": "God is dead.", "author": "Friedrich Nietzsche"},
    {"text": "The world is all that is the case.", "author": "Ludwig Wittgenstein"},
    {"text": "Existence precedes essence.", "author": "Jean-Paul Sartre"},
    {"text": "Hell is other people.", "author": "Jean-Paul Sartre"},
    {"text": "The unexamined life is not worth living.", "author": "Socrates"},
    {"text": "To be is to be perceived.", "author": "George Berkeley"},
    {"text": "Virtue is knowledge.", "author": "Socrates"},
    {"text": "Know thyself.", "author": "Inscribed on the Temple of Apollo at Delphi"},
    {"text": "Man is a rational animal.", "author": "Aristotle"},
    {"text": "The only thing I know is that I know nothing.", "author": "Socrates"},
    {
        "text": "Act only according to that maxim whereby you can, at the same time, will that it should become a universal law.",
        "author": "Immanuel Kant"},
    {"text": "Happiness is the highest good.", "author": "Aristotle"},
    {"text": "The state is the individual writ large.", "author": "Plato"},
    {"text": "Man is by nature a political animal.", "author": "Aristotle"},
    {"text": "All men by nature desire to know.", "author": "Aristotle"},
    {"text": "The foundation of every state is the education of its youth.", "author": "Diogenes"},
    {
        "text": "The secret of happiness, you see, is not found in seeking more, but in developing the capacity to enjoy less.",
        "author": "Socrates"},
    {"text": "Wonder is the beginning of wisdom.", "author": "Socrates"},
    {"text": "He who has a why to live can bear almost any how.", "author": "Friedrich Nietzsche"},
    {"text": "That which does not kill us makes us stronger.", "author": "Friedrich Nietzsche"},
    {"text": "Without music, life would be a mistake.", "author": "Friedrich Nietzsche"},
    {"text": "There are no facts, only interpretations.", "author": "Friedrich Nietzsche"},
    {"text": "The individual has always had to struggle to keep from being overwhelmed by the tribe.",
     "author": "Friedrich Nietzsche"},
    {"text": "Amor Fati - Love your fate, which is in fact your life.", "author": "Friedrich Nietzsche"},
    {"text": "He who fights with monsters should look to it that he himself does not become a monster.",
     "author": "Friedrich Nietzsche"},
    {"text": "The demand to be loved is the greatest of all arrogant presumptions.", "author": "Friedrich Nietzsche"},
    {"text": "Everything that is done in the world is done by hope.", "author": "Martin Luther"},
    {"text": "Faith is taking the first step even when you do not see the whole staircase.",
     "author": "Martin Luther King Jr."},
    {"text": "In the end, we will remember not the words of our enemies, but the silence of our friends.",
     "author": "Martin Luther King Jr."},
    {
        "text": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
        "author": "Martin Luther King Jr."},
    {"text": "The time is always right to do what is right.", "author": "Martin Luther King Jr."},
    {"text": "Our lives begin to end the day we become silent about things that matter.",
     "author": "Martin Luther King Jr."},
    {"text": "Life's most persistent and urgent question is, 'What are you doing for others?'",
     "author": "Martin Luther King Jr."},
    {"text": "Change does not roll in on the wheels of inevitability, but comes through continuous struggle.",
     "author": "Martin Luther King Jr."},
    {"text": "We must accept finite disappointment, but never lose infinite hope.", "author": "Martin Luther King Jr."},
    {"text": "Forgiveness is not an occasional act, it is a constant attitude.", "author": "Martin Luther King Jr."},
    {"text": "Injustice anywhere is a threat to justice everywhere.", "author": "Martin Luther King Jr."},
    {"text": "The limit of your language are the limits of your world.", "author": "Ludwig Wittgenstein"},
    {"text": "We are what we pretend to be, so we must be careful about what we pretend to be.",
     "author": "Kurt Vonnegut"},
    {"text": "So it goes.", "author": "Kurt Vonnegut"},
    {
        "text": "Laughter and tears are both responses to frustration and exhaustion. I myself prefer to laugh, since there is less cleaning up to do afterward.",
        "author": "Kurt Vonnegut"},
    {"text": "True terror is to wake up one morning and discover that your high school class is running the country.",
     "author": "Kurt Vonnegut"},
    {"text": "We have to continually be jumping off cliffs and developing our wings on the way down.",
     "author": "Kurt Vonnegut"},
    {"text": "Enjoy the little things in life, for one day you may look back and realize they were the big things.",
     "author": "Kurt Vonnegut"},
    {
        "text": "I want to stay as close to the edge as I can without going over. Out on the edge you see all kinds of things you can't see from the center.",
        "author": "Kurt Vonnegut"},
    {
        "text": "Be soft. Do not let the world make you hard. Do not let pain make you hate. Do not let the bitterness steal your sweetness.",
        "author": "Kurt Vonnegut"},
]

# --- 2. THE TEXT FEEDS ---
FEEDS = {
    "Effective Altruism": {
        "EA Forum (Frontpage)": "https://forum.effectivealtruism.org/feed.xml?view=frontpage-rss",
        "GiveWell Blog": "https://blog.givewell.org/feed/",
        "80,000 Hours": "https://80000hours.org/feed/",
        "Giving What We Can": "https://www.givingwhatwecan.org/blog/feed.xml",
        "Animal Charity Evaluators": "https://animalcharityevaluators.org/feed/",
        "The Life You Can Save": "https://www.thelifeyoucansave.org/blog/feed/",
    },
    "Philosophy & Substack": {
        "Peter Singer (Bold Reasoning)": "https://boldreasoningwithpetersinger.substack.com/feed",
        "Bentham's Bulldog": "https://benthamsbulldog.substack.com/feed",
        "Cold Takes (Holden Karnofsky)": "https://www.cold-takes.com/rss/",
        "Slow Boring (Matt Yglesias)": "https://www.slowboring.com/feed",
        "Silver Bulletin (Nate Silver)": "https://www.natesilver.net/feed",
        "EA UK Newsletter": "https://eauk.substack.com/feed",
    },
    "Rationalism & AI Alignment": {
        "Eliezer Yudkowsky (LessWrong)": "https://www.lesswrong.com/feed.xml?view=author-rss&author=Eliezer_Yudkowsky",
        "LessWrong (Frontpage)": "https://www.lesswrong.com/feed.xml?view=frontpage-rss",
        "Astral Codex Ten (Scott Alexander)": "https://astralcodexten.substack.com/feed",
        "Don't Worry About the Vase (Zvi)": "https://thezvi.substack.com/feed",
        "Overcoming Bias (Robin Hanson)": "https://www.overcomingbias.com/feed",
        "AI Alignment Forum": "https://www.alignmentforum.org/feed.xml",
        "MIRI Updates": "https://intelligence.org/feed/",
        "Vitalik Buterin's Blog": "https://vitalik.ca/feed.xml"
    },
    "Science & Complexity": {
        "Quanta Magazine (Complexity)": "https://api.quantamagazine.org/feed/",
        "Santa Fe Institute": "https://www.santafe.edu/feeds/news",
        "ScienceDaily": "https://www.sciencedaily.com/rss/top/science.xml",
        "Nature": "https://www.nature.com/nature.rss",
        "Roots of Progress": "https://rootsofprogress.org/feed"
    },
    "Outdoors (Rafting/Backpacking)": {
        "Backpacker Magazine": "https://www.backpacker.com/feed/",
        "Paddling Magazine": "https://paddlingmag.com/feed/",
        "American Whitewater (Rafting News)": "https://www.americanwhitewater.org/content/News/rss/",
        "Outside Online (Camping & Skills)": "https://www.outsideonline.com/feed/",
    }
}

# --- 3. DASHBOARD UI ---
st.set_page_config(page_title="Personal Polymath Hub", layout="wide", page_icon="🔭")

day_index = datetime.now().timetuple().tm_yday % len(QUOTES)
q = QUOTES[day_index]

st.markdown(f"""
    <div style="background-color: #f8f9fb; padding: 30px; border-radius: 20px; border-left: 12px solid #1a2a6c; margin-bottom: 20px;">
        <h6 style="margin:0; color: #1a2a6c; letter-spacing: 3px;">CENTURY OF WISDOM</h6>
        <p style="font-size: 1.6em; font-family: 'Times New Roman', serif; color: #2c3e50; line-height: 1.3;">"{q['text']}"</p>
        <p style="text-align: right; font-weight: bold; font-size: 1.1em; color: #1a2a6c;"> - {q['author']}</p>
    </div>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def fetch_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    # Intercept SFI to scrape their news page directly
    if "santafe.edu" in url:
        try:
            response = requests.get("https://www.santafe.edu/news-center/news", headers=headers, timeout=12)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                entries = []

                # SFI article link elements in news-center
                for a_tag in soup.find_all('a', href=True):
                    if '/news-center/news/' in a_tag['href'] and a_tag.text.strip():
                        title = a_tag.text.strip()
                        link = a_tag['href']
                        if not link.startswith("http"):
                            link = "https://www.santafe.edu" + link

                        entries.append(type('Entry', (), {'title': title, 'link': link,
                                                          'summary': "Santa Fe Institute research and complexity news."})())

                        if len(entries) >= 5:
                            break
                if entries:
                    return entries
        except Exception:
            pass
        return []

    # Attempt 1: Standard HTTPS request with custom browser headers
    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            if feed.entries:
                return feed.entries
    except:
        pass

    # Attempt 2: Request without SSL certification verification
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=12)
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            if feed.entries:
                return feed.entries
    except:
        pass

    # Attempt 3: Direct parsing fallback
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            return feed.entries
    except:
        pass

    return []


st.title("Unified Home Dashboard")

tabs = st.tabs(list(FEEDS.keys()))

for i, category in enumerate(FEEDS.keys()):
    with tabs[i]:
        sources = FEEDS[category]
        cols = st.columns(2)

        for idx, (name, url) in enumerate(sources.items()):
            with cols[idx % 2]:
                st.header(name)
                entries = fetch_news(url)

                if not entries:
                    st.warning(f"Could not retrieve articles from {name}.")
                else:
                    for e in entries[:5]:
                        with st.expander(e.title):
                            st.markdown(f"**[Original Source]({e.link})**")
                            if hasattr(e, 'summary'):
                                text = e.summary.split('<')[0][:300].strip()
                                st.write(f"{text}...")
                    st.markdown("<br>", unsafe_allow_html=True)

# --- 4. GEOGRAPHIC BASE: FAIRVIEW PARK, OH ---
st.sidebar.title("📍 Fairview Park Base")
st.sidebar.markdown("""
**Backpacking & Camping:**
- [Cuyahoga Valley NP](https://www.nps.gov/cuva/index.htm)
- [Allegheny National Forest](https://www.fs.usda.gov/allegheny) (Top Tier Backpacking)

**Canoeing & Rafting:**
- [Rocky River Reservation](https://www.clevelandmetroparks.com/)
- [Cuyahoga River Water Trail](https://cuyahogariverwatertrail.org/)
- [Ohiopyle, PA](https://www.dcnr.pa.gov/StateParks/FindAPark/OhiopyleStatePark/Pages/default.aspx) (Best Rafting nearby)

**Local Service:**
- [VolunteerMatch Fairview Park](https://www.volunteermatch.org/search?l=Fairview+Park%2C+OH)
""")