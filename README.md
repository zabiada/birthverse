# BirthVerse — Historical & Temporal Life Analytics

**Developed by Zabiada Arman**

BirthVerse is a Python web application that transforms a user's birth date into an interactive historical, astronomical, and temporal profile. By entering a name and birth date, users can explore major world events that occurred on their birthday, real-time lived duration metrics, astronomical alignments at birth, and landmark life milestones.

---

## Key Features

1. **Real-Time Temporal Life Clock**
   - Computes exact calendar age in years, months, and days.
   - Displays live-ticking counters for **Total Days Lived**, **Total Hours Lived**, **Total Minutes**, and **Real-Time Seconds Alive**.
   - Includes a next-birthday countdown timer, leap-year tracker, and traditional day-of-the-week lore.

2. **On This Day in World History & Notable Shared Birthdays**
   - Hybrid historical engine combining live Wikimedia "On This Day" chronicles (when online) with a curated local archive of world history, scientific breakthroughs, cultural milestones, and notable figures who share the user's birthday.

3. **Birth Year Cultural & Demographic Time Capsule**
   - Compares global population at the user's birth against net global population growth since that year.
   - Highlights defining technology, music, cinema, and historical economic benchmarks (average cinema ticket, fuel price, and gold per troy ounce) from the user's birth era.

4. **Physiological & Orbital Telemetry**
   - Real-time estimation of physiological cycles since birth: heartbeats (~72 bpm), respiratory cycles (~16 breaths/min), waking eye blinks, and cumulative sleep/REM cycles.
   - Calculates cosmic distances traveled since birth via Earth's solar orbit (`29.78 km/s`) and galactic motion through the Milky Way (`230 km/s`).

5. **Astronomical Birth Chart & Planetary Ages**
   - Astronomically computes the exact lunar phase, illumination percentage, and synodic cycle day on the user's birth date, rendered via a dynamic SVG moon phase diagram.
   - Calculates orbital ages and upcoming birthdays across Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune, alongside Western Zodiac, Lunar Year Zodiac, and Birthstone metadata.

6. **Landmark Temporal Milestones & Printable Summary Card**
   - Computes exact calendar dates for rare temporal milestones including the **10,000th Day on Earth**, **1 Billionth Second Alive ($10^9\text{ s}$)**, and **100,000th / 250,000th / 500,000th Hour**.
   - Generates a clean, printable and copyable **Official Birthday & Life Summary Card**.

---

## Project Documentation

Formal project documents (prepared by **Zabiada Arman**) are included in the `docs/` directory in both Microsoft Word (`.docx`) and PDF (`.pdf`) formats:
- **Project Proposal**:
  - `docs/BirthVerse_Project_Proposal.docx`
  - `docs/BirthVerse_Project_Proposal.pdf`
- **Technical & User Documentation**:
  - `docs/BirthVerse_Project_Documentation.docx`
  - `docs/BirthVerse_Project_Documentation.pdf`

---

## Quick Start

Requires Python 3 (zero external third-party packages required to run the web server):

```bash
python3 app.py
```

Open **http://127.0.0.1:8080** in your web browser.
