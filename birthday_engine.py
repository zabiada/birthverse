"""
Core calculation engine for BirthVerse: Your Birthday Story & World History Explorer.
Developed by Zabiada Arman.

Computes exact lived duration (days, hours, minutes, seconds), biological & cosmic metrics,
lunar phase at birth, planetary ages across the solar system, zodiac & birthstones,
and past/future landmark temporal milestones.
"""

from __future__ import annotations
import datetime
import calendar
import math
from typing import Any
from history_data import get_historical_data_for_date


# Western Zodiac table (clean text & classical monochrome astronomical glyphs)
WESTERN_ZODIAC = [
    ((1, 20), (2, 18), "Aquarius", "AQ", "Air", "Fixed", "Uranus & Saturn", "Visionary, original, humanitarian, and intellectually curious."),
    ((2, 19), (3, 20), "Pisces", "PI", "Water", "Mutable", "Neptune & Jupiter", "Empathetic, artistic, intuitive, and deeply imaginative."),
    ((3, 21), (4, 19), "Aries", "AR", "Fire", "Cardinal", "Mars", "Bold, pioneering, energetic, and fiercely courageous."),
    ((4, 20), (5, 20), "Taurus", "TA", "Earth", "Fixed", "Venus", "Grounded, patient, appreciative of beauty, and steadfast."),
    ((5, 21), (6, 20), "Gemini", "GE", "Air", "Mutable", "Mercury", "Expressive, quick-witted, adaptable, and endlessly inquisitive."),
    ((6, 21), (7, 22), "Cancer", "CN", "Water", "Cardinal", "The Moon", "Protective, intuitive, loyal, and emotionally resonant."),
    ((7, 23), (8, 22), "Leo", "LE", "Fire", "Fixed", "The Sun", "Radiant, warm-hearted, creative, and naturally magnetic."),
    ((8, 23), (9, 22), "Virgo", "VI", "Earth", "Mutable", "Mercury", "Analytical, observant, thoughtful, and masterfully precise."),
    ((9, 23), (10, 22), "Libra", "LI", "Air", "Cardinal", "Venus", "Harmonious, diplomatic, aesthetic, and fair-minded."),
    ((10, 23), (11, 21), "Scorpio", "SC", "Water", "Fixed", "Pluto & Mars", "Passionate, perceptive, resourceful, and magnetic."),
    ((11, 22), (12, 21), "Sagittarius", "SG", "Fire", "Mutable", "Jupiter", "Adventurous, philosophical, optimistic, and free-spirited."),
    ((12, 22), (1, 19), "Capricorn", "CP", "Earth", "Cardinal", "Saturn", "Disciplined, ambitious, resilient, and strategically wise."),
]

# Birthstones & Flowers by Month
BIRTHSTONE_DATA: dict[int, dict[str, str]] = {
    1: {"stone": "Garnet", "color": "#dc2626", "meaning": "Protection, vitality & enduring friendship", "flower": "Carnation & Snowdrop", "season_north": "Deep Winter"},
    2: {"stone": "Amethyst", "color": "#9333ea", "meaning": "Serenity, clarity & royal wisdom", "flower": "Violet & Iris", "season_north": "Late Winter"},
    3: {"stone": "Aquamarine", "color": "#06b6d4", "meaning": "Courage, tranquil seas & youth", "flower": "Daffodil", "season_north": "Early Spring"},
    4: {"stone": "Diamond", "color": "#94a3b8", "meaning": "Invincible strength, clarity & eternal love", "flower": "Daisy & Sweet Pea", "season_north": "Mid Spring"},
    5: {"stone": "Emerald", "color": "#10b981", "meaning": "Rebirth, foresight & flourishing growth", "flower": "Lily of the Valley", "season_north": "Late Spring"},
    6: {"stone": "Pearl & Alexandrite", "color": "#64748b", "meaning": "Purity, intuition & luck", "flower": "Rose & Honeysuckle", "season_north": "Early Summer"},
    7: {"stone": "Ruby", "color": "#e11d48", "meaning": "Passion, nobility & radiant energy", "flower": "Larkspur & Water Lily", "season_north": "High Summer"},
    8: {"stone": "Peridot", "color": "#84cc16", "meaning": "Warmth, strength & solar glow", "flower": "Gladiolus & Poppy", "season_north": "Late Summer"},
    9: {"stone": "Sapphire", "color": "#2563eb", "meaning": "Truth, sincerity & celestial wisdom", "flower": "Aster & Morning Glory", "season_north": "Early Autumn"},
    10: {"stone": "Opal & Tourmaline", "color": "#ec4899", "meaning": "Creativity, kaleidoscopic hope & inspiration", "flower": "Marigold & Cosmos", "season_north": "Mid Autumn"},
    11: {"stone": "Citrine & Topaz", "color": "#f59e0b", "meaning": "Abundance, joy & golden warmth", "flower": "Chrysanthemum", "season_north": "Late Autumn"},
    12: {"stone": "Turquoise & Tanzanite", "color": "#0ea5e9", "meaning": "Good fortune, peace & cosmic insight", "flower": "Narcissus & Holly", "season_north": "Early Winter"},
}

# Day-of-the-week traditional lore
WEEKDAY_LORE: dict[str, str] = {
    "Monday": "Monday's child is fair of face — associated with the Moon, intuition, and calm reflection.",
    "Tuesday": "Tuesday's child is full of grace — ruled by Mars, bringing drive, warmth, and active spirit.",
    "Wednesday": "Wednesday's child is full of curiosity — ruled by Mercury, gifted in communication and intellect.",
    "Thursday": "Thursday's child has far to go — ruled by Jupiter, the planet of expansion, travel, and wisdom.",
    "Friday": "Friday's child is loving and giving — ruled by Venus, connected to art, harmony, and generosity.",
    "Saturday": "Saturday's child works hard for a living — ruled by Saturn, possessing deep focus and mastery.",
    "Sunday": "The child born on Sunday is bright and spirited — ruled by the Sun, radiating warmth and vitality.",
}

# Solar System orbital periods (in Earth days)
PLANET_ORBITS = [
    {"name": "Mercury", "period_days": 87.969, "code": "MER", "color": "#94a3b8", "tagline": "88-Day Solar Orbit"},
    {"name": "Venus", "period_days": 224.701, "code": "VEN", "color": "#fbbf24", "tagline": "225-Day Solar Orbit"},
    {"name": "Earth", "period_days": 365.256, "code": "EAR", "color": "#38bdf8", "tagline": "365.25-Day Solar Orbit"},
    {"name": "Mars", "period_days": 686.980, "code": "MAR", "color": "#f87171", "tagline": "687-Day Solar Orbit"},
    {"name": "Jupiter", "period_days": 4332.589, "code": "JUP", "color": "#fb923c", "tagline": "11.86-Year Solar Orbit"},
    {"name": "Saturn", "period_days": 10759.22, "code": "SAT", "color": "#fde047", "tagline": "29.45-Year Solar Orbit"},
    {"name": "Uranus", "period_days": 30688.5, "code": "URA", "color": "#67e8f9", "tagline": "84.0-Year Solar Orbit"},
    {"name": "Neptune", "period_days": 60182.0, "code": "NEP", "color": "#818cf8", "tagline": "164.8-Year Solar Orbit"},
]


def get_western_zodiac(month: int, day: int) -> dict[str, str]:
    for (m1, d1), (m2, d2), name, code, element, modality, ruler, traits in WESTERN_ZODIAC:
        if (month == m1 and day >= d1) or (month == m2 and day <= d2):
            return {
                "sign": name,
                "symbol": code,
                "element": element,
                "modality": modality,
                "ruler": ruler,
                "traits": traits,
            }
    return {
        "sign": "Capricorn",
        "symbol": "CP",
        "element": "Earth",
        "modality": "Cardinal",
        "ruler": "Saturn",
        "traits": "Disciplined, ambitious, resilient, and strategically wise.",
    }


def get_chinese_zodiac(year: int) -> dict[str, str]:
    animals = [
        ("Rat", "RAT", "Quick-witted, resourceful, versatile, and kind."),
        ("Ox", "OX", "Diligent, dependable, strong, and determined."),
        ("Tiger", "TGR", "Brave, confident, competitive, and charismatic."),
        ("Rabbit", "RBT", "Quiet, elegant, kind, and responsible."),
        ("Dragon", "DRG", "Confident, intelligent, enthusiastic, and naturally lucky."),
        ("Snake", "SNK", "Enigmatic, intelligent, intuitive, and wise."),
        ("Horse", "HRS", "Animated, active, energetic, and independent."),
        ("Goat", "GOT", "Calm, gentle, sympathetic, and artistic."),
        ("Monkey", "MNK", "Sharp, smart, curious, and inventive."),
        ("Rooster", "RST", "Observant, hardworking, courageous, and talented."),
        ("Dog", "DOG", "Honest, loyal, steadfast, and prudent."),
        ("Pig", "PIG", "Compassionate, generous, diligent, and warm."),
    ]
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    idx = (year - 1900) % 12
    elem_idx = ((year - 1924) % 10) // 2
    animal, code, traits = animals[idx]
    element = elements[elem_idx]
    return {
        "animal": animal,
        "code": code,
        "element": element,
        "full_title": f"{element} {animal}",
        "traits": traits,
    }


def calculate_moon_phase(year: int, month: int, day: int) -> dict[str, Any]:
    """
    Calculates the astronomical lunar phase on the given date using the synodic month
    cycle (29.530588853 days) anchored to the known new moon of Jan 6, 2000 18:14 UTC.
    """
    target_dt = datetime.datetime(year, month, day, 12, 0, 0)
    ref_new_moon = datetime.datetime(2000, 1, 6, 18, 14, 0)
    synodic_month = 29.530588853
    diff_days = (target_dt - ref_new_moon).total_seconds() / 86400.0
    cycle_pos = (diff_days % synodic_month) / synodic_month  # 0.0 to 1.0
    lunar_age_days = round(cycle_pos * synodic_month, 1)

    # Illumination percentage (0% at new moon 0.0, 100% at full moon 0.5)
    illumination = round((1.0 - math.cos(2.0 * math.pi * cycle_pos)) / 2.0 * 100.0, 1)

    if cycle_pos < 0.03 or cycle_pos >= 0.97:
        phase_name = "New Moon"
        lore = "Born under a New Moon — a symbol of fresh beginnings, quiet potential, and setting bold intentions."
    elif cycle_pos < 0.22:
        phase_name = "Waxing Crescent"
        lore = "Born under a Waxing Crescent — driven by curiosity, momentum, and building aspirations into reality."
    elif cycle_pos < 0.28:
        phase_name = "First Quarter"
        lore = "Born under a First Quarter Moon — decisive, action-oriented, and ready to overcome challenges."
    elif cycle_pos < 0.47:
        phase_name = "Waxing Gibbous"
        lore = "Born under a Waxing Gibbous Moon — analytical, refining, and inspiring growth in those around you."
    elif cycle_pos < 0.53:
        phase_name = "Full Moon"
        lore = "Born under a Full Moon — expressive, vibrant, deeply aware, and bringing clarity to complex situations."
    elif cycle_pos < 0.72:
        phase_name = "Waning Gibbous"
        lore = "Born under a Waning Gibbous Moon — a natural communicator, mentor, and sharer of knowledge."
    elif cycle_pos < 0.78:
        phase_name = "Last Quarter"
        lore = "Born under a Last Quarter Moon — reflective, principled, and independent in forging your path."
    else:
        phase_name = "Waning Crescent"
        lore = "Born under a Waning Crescent Moon — visionary, introspective, and deeply imaginative."

    return {
        "phase_name": phase_name,
        "illumination_pct": illumination,
        "cycle_position": round(cycle_pos, 4),
        "lunar_age_days": lunar_age_days,
        "lore": lore,
    }


def compute_birthday_profile(
    birth_date_str: str,
    birth_time_str: str = "00:00",
    user_name: str = "",
    try_live_history: bool = True,
) -> dict[str, Any]:
    """
    Computes the complete temporal, biological, cosmic, and historical profile
    for a user's birthday.
    """
    now = datetime.datetime.now()
    parts = [int(p) for p in birth_date_str.strip().split("-")]
    year, month, day = parts[0], parts[1], parts[2]

    hour, minute = 0, 0
    if birth_time_str and ":" in birth_time_str:
        try:
            t_parts = birth_time_str.strip().split(":")
            hour = max(0, min(23, int(t_parts[0])))
            minute = max(0, min(59, int(t_parts[1])))
        except ValueError:
            hour, minute = 0, 0

    birth_dt = datetime.datetime(year, month, day, hour, minute, 0)
    if birth_dt > now:
        raise ValueError("Your birth date cannot be in the future. Please select a past date.")

    delta = now - birth_dt
    total_seconds = max(1, int(delta.total_seconds()))
    total_minutes = total_seconds // 60
    total_hours = total_seconds // 3600
    total_days = delta.days
    total_weeks = total_days // 7

    # Exact calendar age breakdown (years, months, days)
    years = now.year - birth_dt.year
    months = now.month - birth_dt.month
    days = now.day - birth_dt.day
    if days < 0:
        months -= 1
        prev_month = 12 if now.month == 1 else now.month - 1
        prev_year = now.year - 1 if now.month == 1 else now.year
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
    if months < 0:
        years -= 1
        months += 12

    total_months_lived = years * 12 + months

    # Next birthday calculation
    try:
        next_bday = datetime.datetime(now.year, month, day, hour, minute, 0)
    except ValueError:
        next_bday = datetime.datetime(now.year, 2, 28, hour, minute, 0)

    if next_bday <= now:
        try:
            next_bday = datetime.datetime(now.year + 1, month, day, hour, minute, 0)
        except ValueError:
            next_bday = datetime.datetime(now.year + 1, 2, 28, hour, minute, 0)

    next_bday_delta = next_bday - now
    next_bday_days = next_bday_delta.days
    next_bday_hours = (next_bday_delta.seconds // 3600)
    next_bday_minutes = (next_bday_delta.seconds % 3600) // 60

    # Leap years experienced
    leap_years_count = 0
    for y in range(year, now.year + 1):
        if calendar.isleap(y):
            leap_dt = datetime.datetime(y, 2, 29, 23, 59, 59)
            if birth_dt <= leap_dt <= now:
                leap_years_count += 1

    # Biological & Cosmic metrics
    heartbeats = int(total_seconds * (72.0 / 60.0))
    breaths = int(total_seconds * (16.0 / 60.0))
    blinks = int(total_seconds * (15.0 / 60.0) * (16.0 / 24.0))
    hours_slept = round(total_hours * (8.0 / 24.0), 1)
    years_slept = round(hours_slept / (24.0 * 365.25), 2)
    dreams_had = int(total_days * 4.2)
    liters_blood_pumped = int(total_days * 7570)

    # Cosmic distances traveled since birth
    earth_spin_km = int(total_seconds * 0.4651)
    solar_orbit_km = int(total_seconds * 29.78)
    milky_way_km = int(total_seconds * 230.0)
    full_moons_seen = int(total_days / 29.53059)

    # Planetary ages
    planetary_ages = []
    for planet in PLANET_ORBITS:
        p_age = round(total_days / planet["period_days"], 2)
        next_whole = math.floor(total_days / planet["period_days"]) + 1
        days_until_next = max(1, int(round(next_whole * planet["period_days"] - total_days)))
        next_date = (now + datetime.timedelta(days=days_until_next)).strftime("%b %d, %Y")
        planetary_ages.append({
            "name": planet["name"],
            "code": planet["code"],
            "color": planet["color"],
            "tagline": planet["tagline"],
            "age": p_age,
            "next_birthday_age": next_whole,
            "days_until_next": days_until_next,
            "next_birthday_date": next_date,
        })

    # Unusual Past & Future Temporal Milestones
    milestone_specs = [
        {"label": "1,000 Days on Earth", "delta": datetime.timedelta(days=1000), "tag": "1K DAYS", "desc": "Your first thousand sunrises"},
        {"label": "5,000 Days on Earth", "delta": datetime.timedelta(days=5000), "tag": "5K DAYS", "desc": "Five thousand rotations of Earth"},
        {"label": "10,000th Day Alive", "delta": datetime.timedelta(days=10000), "tag": "10K DAYS", "desc": "A major five-digit day milestone (~27.4 years)"},
        {"label": "100,000th Hour Alive", "delta": datetime.timedelta(hours=100000), "tag": "100K HRS", "desc": "One hundred thousand hours lived (~11.4 years)"},
        {"label": "250,000th Hour Alive", "delta": datetime.timedelta(hours=250000), "tag": "250K HRS", "desc": "A quarter-million hours lived (~28.5 years)"},
        {"label": "500,000th Hour Alive", "delta": datetime.timedelta(hours=500000), "tag": "500K HRS", "desc": "Half a million hours on Earth (~57.0 years)"},
        {"label": "1 Billionth Second (10⁹ s)", "delta": datetime.timedelta(seconds=1_000_000_000), "tag": "1B SEC", "desc": "One billion seconds since birth (~31.7 years)"},
        {"label": "2 Billionth Second (2×10⁹ s)", "delta": datetime.timedelta(seconds=2_000_000_000), "tag": "2B SEC", "desc": "Two billion seconds of life (~63.4 years)"},
        {"label": "15,000th Day Alive", "delta": datetime.timedelta(days=15000), "tag": "15K DAYS", "desc": "Fifteen thousand days of experience (~41.1 years)"},
        {"label": "20,000th Day Alive", "delta": datetime.timedelta(days=20000), "tag": "20K DAYS", "desc": "Twenty thousand days on Earth (~54.8 years)"},
    ]

    milestones = []
    for m in milestone_specs:
        m_dt = birth_dt + m["delta"]
        is_past = m_dt <= now
        diff_days = abs((m_dt - now).days)
        milestones.append({
            "label": m["label"],
            "tag": m["tag"],
            "desc": m["desc"],
            "date_formatted": m_dt.strftime("%B %d, %Y"),
            "year": m_dt.year,
            "is_past": is_past,
            "status_text": f"Completed {diff_days:,}d ago" if is_past else f"In {diff_days:,} days",
        })

    birth_weekday = birth_dt.strftime("%A")
    next_bday_weekday = next_bday.strftime("%A")
    day_of_year = birth_dt.timetuple().tm_yday

    western_zodiac = get_western_zodiac(month, day)
    chinese_zodiac = get_chinese_zodiac(year)
    moon_phase = calculate_moon_phase(year, month, day)
    birthstone = BIRTHSTONE_DATA.get(month, BIRTHSTONE_DATA[1])
    history_bundle = get_historical_data_for_date(year, month, day, try_live=try_live_history)

    serial_code = f"BV-{year}{month:02d}{day:02d}-{western_zodiac['symbol']}-{total_days % 9999:04d}"

    return {
        "user": {
            "name": user_name.strip() or "Guest",
            "birth_date_iso": f"{year:04d}-{month:02d}-{day:02d}",
            "birth_time": f"{hour:02d}:{minute:02d}",
            "birth_date_formatted": birth_dt.strftime("%B %d, %Y"),
            "month_day_formatted": birth_dt.strftime("%B %d"),
            "birth_weekday": birth_weekday,
            "weekday_lore": WEEKDAY_LORE.get(birth_weekday, ""),
            "day_of_year": day_of_year,
            "is_leap_year_birth": calendar.isleap(year),
            "serial_code": serial_code,
            "birth_timestamp_ms": int(birth_dt.timestamp() * 1000),
        },
        "age_breakdown": {
            "years": years,
            "months": months,
            "days": days,
            "total_months": total_months_lived,
            "total_weeks": total_weeks,
            "total_days": total_days,
            "total_hours": total_hours,
            "total_minutes": total_minutes,
            "total_seconds": total_seconds,
            "leap_years_experienced": leap_years_count,
            "seasons_experienced": total_days // 91,
        },
        "next_birthday": {
            "date_formatted": next_bday.strftime("%B %d, %Y"),
            "weekday": next_bday_weekday,
            "turning_age": years + 1,
            "days_remaining": next_bday_days,
            "hours_remaining": next_bday_hours,
            "minutes_remaining": next_bday_minutes,
            "progress_pct": round(((365.25 - next_bday_days) / 365.25) * 100, 1),
        },
        "biometrics": {
            "heartbeats": heartbeats,
            "breaths": breaths,
            "blinks": blinks,
            "hours_slept": hours_slept,
            "years_slept": years_slept,
            "dreams_had": dreams_had,
            "liters_blood_pumped": liters_blood_pumped,
        },
        "cosmic_journey": {
            "earth_spin_km": earth_spin_km,
            "solar_orbit_km": solar_orbit_km,
            "milky_way_km": milky_way_km,
            "full_moons_seen": full_moons_seen,
            "moon_trips_equivalent": round(solar_orbit_km / 384400.0, 1),
        },
        "astronomy": {
            "moon_phase": moon_phase,
            "western_zodiac": western_zodiac,
            "chinese_zodiac": chinese_zodiac,
            "birthstone": birthstone,
            "planetary_ages": planetary_ages,
        },
        "milestones": milestones,
        "history": history_bundle,
    }
