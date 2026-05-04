---
name: reddit-radar
description: Scans Reddit RSS feeds to find developers and indie hackers looking for in-person hackathons globally.
metadata:
  openclaw:
    emoji: "🌍"
---
# Reddit Radar (Global Visual Discovery Strategy)

Use the `exec` tool to run the python RSS scraper against these new high-intent target feeds:
1. `https://www.reddit.com/search.rss?q=find+in+person+hackathons&sort=new`
2. `https://www.reddit.com/search.rss?q=where+to+find+hackathons&sort=new`
3. `https://www.reddit.com/r/hackathon/search.rss?q=upcoming&restrict_sr=on&sort=new`
4. `https://www.reddit.com/r/csMajors/search.rss?q=next+hackathon&restrict_sr=on&sort=new`
5. `https://www.reddit.com/r/SideProject/search.rss?q=hackathon&restrict_sr=on&sort=new`

## Filtering Logic
- REJECT any post older than 7 days (handled by the script, but verify the output).
- REJECT any post where the user is just showcasing a project.
- ACCEPT posts asking "How do I find hackathons?" or "Are there any hackathons in [City/Country]?"

## The "Strike" (Drafting the Reply)
When drafting replies for OJ to post:
- **The Hook**: Acknowledge that finding hackathons on standard sites (like Devpost) is annoying because it's just endless lists.
- **The Pivot**: "I built Hackamaps.com because I wanted to actually see where they are on a map, filterable by date."
- **Keep it brief**: Max 3 sentences. Builder-to-builder tone.
