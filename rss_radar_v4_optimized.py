import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import sys
import json
import hashlib
import random
import time
import os
from datetime import datetime, timezone, timedelta

# Configuration
SEEN_FILE = "seen_posts.txt"
HIGH_INTENT = ["looking for hackathon", "any hackathons", "hackathon in", "join a team", "find hackathon", "upcoming hackathons"]
MID_INTENT = ["hackathon ideas", "hackathon experience"]
TEMPLATES = [
    "I had the same problem — hackathons are weirdly scattered. I started tracking some here: {link}. Might help.",
    "Yeah this is annoying. There’s no central place. I’ve been using {link} to keep track.",
    "You might want to check this: {link}. It’s not perfect but better than searching Reddit threads."
]

def get_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_seen(md5_hash):
    with open(SEEN_FILE, "a") as f:
        f.write(md5_hash + "\n")

def classify_intent(title):
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in HIGH_INTENT):
        return "HIGH"
    if any(keyword in title_lower for keyword in MID_INTENT):
        return "MID"
    return "LOW"

def fetch_rss(query_url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SignalRadar/1.0'}
    seen_set = load_seen()
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(query_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            leads = []
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text
                url = entry.find('atom:link', ns).attrib['href']
                
                # Deduplication
                post_id = get_md5(title)
                if post_id in seen_set:
                    continue
                
                # Intent Classification
                intent = classify_intent(title)
                if intent == "LOW":
                    continue
                
                # DELAY ONLY FOR RELEVANT ITEMS (Optimized)
                time.sleep(random.randint(1, 3))
                
                # Response Generation
                template = random.choice(TEMPLATES)
                reply = template.format(link="Hackamaps.com")
                
                leads.append({
                    "post_title": title,
                    "url": url,
                    "intent_level": intent,
                    "suggested_reply": reply,
                    "id": post_id
                })
                
                # Mark as seen
                save_seen(post_id)
                seen_set.add(post_id)
                
            return leads
        except Exception as e:
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Provide an RSS URL."}))
        sys.exit(1)
        
    target_url = sys.argv[1]
    results = fetch_rss(target_url)
    print(json.dumps(results, indent=2))
