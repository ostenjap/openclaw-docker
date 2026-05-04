import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import sys
import json
from datetime import datetime, timezone, timedelta

def fetch_rss(query_url, max_age_hours=24):
    req = urllib.request.Request(query_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        results = []
        now = datetime.now(timezone.utc)
        
        for entry in root.findall('atom:entry', ns):
            link = entry.find('atom:link', ns).attrib['href']
            
            # V2 FILTER: Reject base subreddits (e.g. reddit.com/r/name/)
            # Most base subreddit links in search RSS end with a trailing slash or lack the /comments/ segment
            if "/comments/" not in link:
                continue
                
            updated_str = entry.find('atom:updated', ns).text
            try:
                updated_time = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
            except ValueError:
                updated_time = now
                
            if (now - updated_time) > timedelta(hours=max_age_hours):
                continue
                
            title = entry.find('atom:title', ns).text
            author = entry.find('atom:author/atom:name', ns).text
            
            results.append({
                "title": title,
                "author": author,
                "url": link,
                "age_hours": round((now - updated_time).total_seconds() / 3600, 1)
            })
            
        return results[:5]
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide an RSS URL.")
        sys.exit(1)
        
    target_url = sys.argv[1]
    leads = fetch_rss(target_url)
    print(json.dumps(leads, indent=2))
