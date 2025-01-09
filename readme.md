# Visa Bulletin Reader
This is a simple web scraper to get the latest visa bulletin information from the [travel.state.gov](https://travel.state.gov/) website. I started this with a goal of learning python and web scrapping capabilities.

## Goal/Outcome
- To get the latest visa bulletin information from the travel.state.gov website.
- Currently built as a command line tool, with prompt to select the visa bulletin type and country.
- Future goal is to build a web application to display the information in a more user friendly way.

## Tech Requirement Primers

- Find the section "recent_bulletins" from ul type.
- Look for tags with "Upcoming Visa Bulletin" and if not found/available, then go for "Current Visa Bulletin".
- Navigate or find the link with the format as
  - https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/{currentYear}/visa-bulletin-for-{wildcard}-{currentYear}.html

### Finding the information required

- Find the table type occurrences
  - Pick first 2 and render the data
