"""
Historical events, famous birthdays, and birth-year cultural time capsule data.
Combines live Wikimedia 'On This Day' API fetching (when online) with a rich,
curated local database so the app works reliably both online and offline.
"""

from __future__ import annotations
import urllib.request
import urllib.error
import json
from typing import Any


# Curated exact-date highlights (month, day) -> list of events
EXACT_DATE_EVENTS: dict[tuple[int, int], list[dict[str, Any]]] = {
    (1, 1): [
        {"year": 1863, "category": "World History", "title": "Emancipation Proclamation Takes Effect", "description": "President Abraham Lincoln's Emancipation Proclamation officially goes into effect, proclaiming the freedom of enslaved people in Confederate territory."},
        {"year": 1983, "category": "Science & Tech", "title": "Birth of the Modern Internet (TCP/IP)", "description": "ARPANET officially switches to the TCP/IP protocol suite, marking the technical birth of the modern Internet."},
        {"year": 1999, "category": "World History", "title": "The Euro Currency Launches", "description": "The Euro is officially introduced as an accounting currency in 11 European Union member nations."},
    ],
    (2, 14): [
        {"year": 1990, "category": "Science & Tech", "title": "Voyager 1 Takes the 'Pale Blue Dot' Photo", "description": "At Carl Sagan's request, NASA's Voyager 1 turns its camera around from 6 billion kilometers away to photograph Earth as a tiny 'Pale Blue Dot'."},
        {"year": 2005, "category": "Pop Culture", "title": "YouTube Is Founded", "description": "Steve Chen, Chad Hurley, and Jawed Karim register YouTube.com, revolutionizing global video sharing."},
    ],
    (3, 14): [
        {"year": 1879, "category": "Famous Birth", "title": "Albert Einstein Is Born", "description": "Theoretical physicist Albert Einstein is born in Ulm, Germany, on what the world now celebrates as Pi Day (3.14)."},
        {"year": 2019, "category": "Science & Tech", "title": "Pi Calculated to 31.4 Trillion Digits", "description": "Emma Haruka Iwao calculates the value of Pi to a world-record 31.4 trillion digits using cloud supercomputing."},
    ],
    (4, 12): [
        {"year": 1961, "category": "Science & Tech", "title": "First Human in Space", "description": "Cosmonaut Yuri Gagarin aboard Vostok 1 becomes the first human to journey into outer space and orbit the Earth."},
        {"year": 1981, "category": "Science & Tech", "title": "First Space Shuttle Launch (STS-1)", "description": "NASA launches Space Shuttle Columbia on STS-1, the first orbital flight of the Space Shuttle program."},
    ],
    (7, 20): [
        {"year": 1969, "category": "Science & Tech", "title": "Apollo 11 Moon Landing", "description": "Neil Armstrong and Buzz Aldrin land the Apollo Lunar Module Eagle on the Moon; Armstrong takes 'one small step for [a] man, one giant leap for mankind.'"},
        {"year": 1976, "category": "Science & Tech", "title": "Viking 1 Lands on Mars", "description": "NASA's Viking 1 lander successfully touches down at Chryse Planitia on Mars, sending back the first clear photos from the Martian surface."},
    ],
    (8, 6): [
        {"year": 1991, "category": "Science & Tech", "title": "World Wide Web Goes Public", "description": "Tim Berners-Lee posts the first public summary of the World Wide Web project and opens the first web server to the public."},
        {"year": 2012, "category": "Science & Tech", "title": "Curiosity Rover Lands on Mars", "description": "NASA's Curiosity rover lands in Gale Crater on Mars using a pioneering rocket-powered 'sky crane' maneuver."},
    ],
    (10, 28): [
        {"year": 1886, "category": "World History", "title": "Dedication of the Statue of Liberty", "description": "U.S. President Grover Cleveland officially dedicates the Statue of Liberty (Liberty Enlightening the World) in New York Harbor, a gift from France."},
        {"year": 1918, "category": "World History", "title": "Independence of Czechoslovakia", "description": "Czechoslovakia declares independence from the Austro-Hungarian Empire at the conclusion of World War I."},
        {"year": 1955, "category": "Famous Birth", "title": "Bill Gates Is Born", "description": "Technologist and philanthropist Bill Gates, co-founder of Microsoft, is born in Seattle, Washington."},
        {"year": 1965, "category": "Culture & Architecture", "title": "St. Louis Gateway Arch Completed", "description": "The final stainless-steel keystone section of the 630-foot Gateway Arch designed by Eero Saarinen is placed in St. Louis, Missouri."},
    ],
    (11, 9): [
        {"year": 1989, "category": "World History", "title": "Fall of the Berlin Wall", "description": "East Germany opens checkpoints through the Berlin Wall, allowing citizens to cross freely and heralding the end of the Cold War."},
        {"year": 1934, "category": "Famous Birth", "title": "Carl Sagan Is Born", "description": "Astronomer, planetary scientist, and legendary science communicator Carl Sagan is born in Brooklyn, New York."},
    ],
    (12, 25): [
        {"year": 2021, "category": "Science & Tech", "title": "James Webb Space Telescope Launches", "description": "The James Webb Space Telescope launches from French Guiana on an Ariane 5 rocket to peer back to the dawn of the cosmos."},
        {"year": 1642, "category": "Famous Birth", "title": "Isaac Newton Is Born (OS)", "description": "Mathematician and physicist Sir Isaac Newton is born in Woolsthorpe, England."},
    ],
}


# Monthly thematic & deterministic historical database so ANY date (1..366) gets rich, accurate historical events
MONTHLY_HISTORICAL_POOL: dict[int, list[dict[str, Any]]] = {
    1: [
        {"year": 1610, "category": "Science & Tech", "title": "Galileo Discovers Jupiter's Moons", "description": "Galileo Galilei points his telescope at Jupiter and observes the four Galilean moons, transforming humanity's understanding of the cosmos."},
        {"year": 1896, "category": "Science & Tech", "title": "First Public Demonstration of X-Rays", "description": "Wilhelm Röntgen's discovery of X-rays is demonstrated to the world, ushering in modern medical imaging."},
        {"year": 1927, "category": "Pop Culture", "title": "First Transatlantic Telephone Call", "description": "Commercial radio-telephone service connects New York and London for the first time in history."},
        {"year": 1958, "category": "Science & Tech", "title": "Explorer 1 Launches & Discovers Van Allen Belts", "description": "The first U.S. satellite, Explorer 1, reaches orbit and detects Earth's radiation belts."},
        {"year": 2001, "category": "Science & Tech", "title": "Wikipedia Goes Online", "description": "Jimmy Wales and Larry Sanger launch Wikipedia, creating the largest collaborative encyclopedia in human history."},
        {"year": 2007, "category": "Science & Tech", "title": "Original iPhone Unveiled", "description": "Steve Jobs introduces the first iPhone on stage in San Francisco, redefining personal computing and mobile communication."},
    ],
    2: [
        {"year": 1876, "category": "Science & Tech", "title": "Telephone Patent Filed", "description": "Alexander Graham Bell files his landmark patent for transmitting vocal sounds telegraphically."},
        {"year": 1922, "category": "Pop Culture", "title": "James Joyce's 'Ulysses' Published in Paris", "description": "Shakespeare and Company in Paris publishes James Joyce's modernist masterpiece 'Ulysses'."},
        {"year": 1946, "category": "Science & Tech", "title": "ENIAC Computer Unveiled", "description": "The Electronic Numerical Integrator and Computer (ENIAC), the first general-purpose electronic digital computer, is unveiled at the University of Pennsylvania."},
        {"year": 1953, "category": "Science & Tech", "title": "Double Helix Structure of DNA Discovered", "description": "Rosalind Franklin's X-ray diffraction data along with Watson and Crick's model reveal the double-helix structure of DNA."},
        {"year": 1964, "category": "Pop Culture", "title": "The Beatles Perform on The Ed Sullivan Show", "description": "An estimated 73 million viewers tune in as The Beatles make their historic American television debut."},
        {"year": 2016, "category": "Science & Tech", "title": "First Direct Detection of Gravitational Waves", "description": "Physicists at LIGO announce the historic observation of gravitational waves from two colliding black holes, confirming Einstein's century-old prediction."},
    ],
    3: [
        {"year": 1781, "category": "Science & Tech", "title": "Discovery of the Planet Uranus", "description": "Astronomer William Herschel observes Uranus, the first planet discovered with the aid of a telescope."},
        {"year": 1895, "category": "Pop Culture", "title": "Lumière Brothers Screen the First Motion Picture", "description": "Auguste and Louis Lumière demonstrate their Cinématographe in Paris, marking the birth of cinema."},
        {"year": 1933, "category": "World History", "title": "First 'Fireside Chat' Broadcast", "description": "Radio broadcasts bring national leadership directly into living rooms, changing political communication forever."},
        {"year": 1965, "category": "Science & Tech", "title": "First Spacewalk in History", "description": "Cosmonaut Alexei Leonov exits Voskhod 2 for 12 minutes, performing the first extravehicular activity (spacewalk) in space."},
        {"year": 1989, "category": "Science & Tech", "title": "Tim Berners-Lee Proposes the World Wide Web", "description": "At CERN, Tim Berners-Lee writes 'Information Management: A Proposal,' laying out the architecture of the Web."},
        {"year": 2012, "category": "Science & Tech", "title": "Solo Dive to the Mariana Trench", "description": "Filmmaker and explorer James Cameron pilots the Deepsea Challenger nearly 11 km down to Challenger Deep."},
    ],
    4: [
        {"year": 1912, "category": "World History", "title": "Maiden Voyage of the RMS Titanic", "description": "The ocean liner RMS Titanic embarks on its historic and fateful maiden transatlantic voyage."},
        {"year": 1955, "category": "Science & Tech", "title": "Polio Vaccine Declared Safe and Effective", "description": "Dr. Jonas Salk's polio vaccine is announced to the world as safe and potent, saving millions of lives globally."},
        {"year": 1970, "category": "World History", "title": "First Earth Day Celebrated & Apollo 13 Rescue", "description": "Twenty million people participate in the first Earth Day, the same month NASA engineers bring the Apollo 13 crew safely home."},
        {"year": 1990, "category": "Science & Tech", "title": "Hubble Space Telescope Deployed in Orbit", "description": "Space Shuttle Discovery deploys the Hubble Space Telescope, opening an extraordinary window onto deep space."},
        {"year": 2003, "category": "Science & Tech", "title": "Human Genome Project Completed", "description": "International scientists announce the completion of the Human Genome Project, mapping 99% of the gene-containing human DNA sequence."},
        {"year": 2019, "category": "Science & Tech", "title": "First Ever Image of a Black Hole Released", "description": "The Event Horizon Telescope collaboration unveils the first direct visual image of the supermassive black hole at the heart of galaxy M87."},
    ],
    5: [
        {"year": 1844, "category": "Science & Tech", "title": "First Long-Distance Telegraph Message", "description": "Samuel Morse transmits 'What hath God wrought' from Washington, D.C., to Baltimore, ushering in instant telecommunications."},
        {"year": 1927, "category": "World History", "title": "First Solo Nonstop Transatlantic Flight", "description": "Charles Lindbergh lands the Spirit of St. Louis at Le Bourget Field in Paris after a 33.5-hour flight from New York."},
        {"year": 1953, "category": "World History", "title": "First Ascent of Mount Everest", "description": "Tenzing Norgay and Edmund Hillary reach the 8,848-meter summit of Mount Everest, the highest point on Earth."},
        {"year": 1961, "category": "Science & Tech", "title": "'We Choose to Go to the Moon' Address to Congress", "description": "President John F. Kennedy sets the ambitious goal of landing a human on the Moon and returning safely before the decade is out."},
        {"year": 1977, "category": "Pop Culture", "title": "Original 'Star Wars' Premieres in Theaters", "description": "George Lucas's 'Star Wars' debuts in cinemas, transforming visual effects and global pop culture."},
        {"year": 1994, "category": "World History", "title": "Channel Tunnel Officially Opens", "description": "The 50.5-kilometer undersea 'Chunnel' rail link connects Great Britain and continental Europe."},
    ],
    6: [
        {"year": 1215, "category": "World History", "title": "Sealing of the Magna Carta", "description": "At Runnymede, the Magna Carta establishes the foundational constitutional principle that everyone is subject to the law."},
        {"year": 1752, "category": "Science & Tech", "title": "Benjamin Franklin's Kite Experiment", "description": "Benjamin Franklin demonstrates the electrical nature of lightning, advancing the study of electricity."},
        {"year": 1944, "category": "World History", "title": "Allied Landings in Normandy", "description": "Operation Overlord marks a pivotal turning point in 20th-century world history."},
        {"year": 1963, "category": "Science & Tech", "title": "Valentina Tereshkova Becomes First Woman in Space", "description": "Aboard Vostok 6, Valentina Tereshkova orbits Earth 48 times, remaining the only woman to fly a solo space mission."},
        {"year": 1983, "category": "Science & Tech", "title": "Pioneer 10 Passes Beyond Neptune's Orbit", "description": "NASA's Pioneer 10 becomes the first human-made spacecraft to travel beyond the orbits of all solar system planets."},
        {"year": 1997, "category": "Pop Culture", "title": "'Harry Potter and the Philosopher's Stone' Published", "description": "J.K. Rowling's debut wizarding novel is published in London with an initial print run of just 500 hardcover copies."},
    ],
    7: [
        {"year": 1776, "category": "World History", "title": "Declaration of Independence Adopted", "description": "The Continental Congress adopts the Declaration of Independence in Philadelphia."},
        {"year": 1903, "category": "Pop Culture", "title": "First Tour de France Cycling Race", "description": "Sixty cyclists set out from Montgeron near Paris in the inaugural Tour de France endurance race."},
        {"year": 1928, "category": "Pop Culture", "title": "First Sliced Bread Sold & Penicillin Discovered", "description": "1928 brings both commercial sliced bread and Alexander Fleming's accidental discovery of penicillin."},
        {"year": 1962, "category": "Science & Tech", "title": "Telstar 1 Relays First Live Transatlantic Television", "description": "The Telstar 1 communications satellite beams the first live television pictures across the Atlantic Ocean."},
        {"year": 1996, "category": "Science & Tech", "title": "Dolly the Sheep Is Born", "description": "Scientists at the Roslin Institute in Scotland welcome Dolly, the first mammal cloned from an adult somatic cell."},
        {"year": 2012, "category": "Science & Tech", "title": "Discovery of the Higgs Boson Announced at CERN", "description": "Physicists at the Large Hadron Collider announce the discovery of the Higgs boson particle, completing the Standard Model of physics."},
    ],
    8: [
        {"year": 1839, "category": "Science & Tech", "title": "Daguerreotype Photography Gifted to the World", "description": "The French Academy of Sciences announces Louis Daguerre's photographic process as a 'free gift to the world.'"},
        {"year": 1911, "category": "Pop Culture", "title": "Mona Lisa Vanishes from the Louvre", "description": "The theft and eventual recovery of Leonardo da Vinci's Mona Lisa propels the painting to unmatched global fame."},
        {"year": 1963, "category": "World History", "title": "'I Have a Dream' Speech at the Lincoln Memorial", "description": "Dr. Martin Luther King Jr. delivers his iconic 'I Have a Dream' address to 250,000 civil rights marchers in Washington, D.C."},
        {"year": 1969, "category": "Pop Culture", "title": "Woodstock Music & Art Fair", "description": "Over 400,000 people gather on a dairy farm in Bethel, New York, for three days of peace and music."},
        {"year": 1977, "category": "Science & Tech", "title": "Voyager 2 Launches on the Grand Tour", "description": "Voyager 2 lifts off to visit Jupiter, Saturn, Uranus, and Neptune before entering interstellar space."},
        {"year": 2017, "category": "Science & Tech", "title": "First Neutron Star Merger Observed (GW170817)", "description": "Astronomers simultaneously detect gravitational waves and light from two colliding neutron stars, revealing how gold and platinum are forged in the cosmos."},
    ],
    9: [
        {"year": 1522, "category": "World History", "title": "First Circumnavigation of the Globe Completed", "description": "The carrack Victoria returns to Spain, completing the first documented voyage around the entire Earth."},
        {"year": 1928, "category": "Science & Tech", "title": "Alexander Fleming Discovers Penicillin", "description": "Returning to his London laboratory, Fleming notices a mold inhibiting bacterial growth—ushering in the age of antibiotics."},
        {"year": 1939, "category": "Pop Culture", "title": "'The Wizard of Oz' Technicolor Release", "description": "Audiences gasp as Dorothy opens the door from sepia-toned Kansas into the vibrant Technicolor world of Oz."},
        {"year": 1977, "category": "Science & Tech", "title": "Voyager 1 Launches Carrying the Golden Record", "description": "Voyager 1 rockets into space carrying a gold-plated phonograph record of Earth's sights, sounds, music, and greetings in 55 languages."},
        {"year": 1998, "category": "Science & Tech", "title": "Google Is Founded in a Menlo Park Garage", "description": "Larry Page and Sergey Brin incorporate Google with the mission to organize the world's information."},
        {"year": 2015, "category": "Science & Tech", "title": "NASA Confirms Evidence of Flowing Brine on Mars", "description": "Planetary scientists announce spectral evidence of seasonal hydrated salts on Martian slopes."},
    ],
    10: [
        {"year": 1492, "category": "World History", "title": "Transatlantic Voyages Connect the Hemispheres", "description": "Maritime navigation permanently links the Old and New Worlds, initiating the global Columbian Exchange."},
        {"year": 1908, "category": "Science & Tech", "title": "First Model T Ford Rolls Off the Line", "description": "Henry Ford introduces the affordable Model T, putting the world on wheels and pioneering modern assembly lines."},
        {"year": 1947, "category": "Science & Tech", "title": "Chuck Yeager Breaks the Sound Barrier", "description": "Piloting the Bell X-1 rocket plane 'Glamorous Glennis', Chuck Yeager becomes the first human to fly faster than the speed of sound (Mach 1.06)."},
        {"year": 1957, "category": "Science & Tech", "title": "Sputnik 1 Begins the Space Age", "description": "The launch of Sputnik 1, the first artificial Earth satellite, beeps from orbit and ignites the dawn of space exploration."},
        {"year": 1969, "category": "Science & Tech", "title": "First Message Sent Over ARPANET ('LO')", "description": "UCLA student Charley Kline sends the first host-to-host message to Stanford Research Institute over ARPANET."},
        {"year": 2001, "category": "Pop Culture", "title": "Original iPod Introduced ('1,000 Songs in Your Pocket')", "description": "Apple unveils the original 5GB iPod, transforming how the world listens to music."},
    ],
    11: [
        {"year": 1859, "category": "Science & Tech", "title": "Darwin Publishes 'On the Origin of Species'", "description": "Charles Darwin's foundational work on evolutionary biology sells out its entire 1,250-copy print run on the first day."},
        {"year": 1922, "category": "World History", "title": "Discovery of King Tutankhamun's Tomb", "description": "Archaeologist Howard Carter peers into the nearly intact 3,000-year-old tomb of Pharaoh Tutankhamun in the Valley of the Kings and sees 'wonderful things.'"},
        {"year": 1969, "category": "Pop Culture", "title": "'Sesame Street' Premieres on Television", "description": "Jim Henson's Muppets and a pioneering educational format debut on public television."},
        {"year": 1995, "category": "Pop Culture", "title": "Pixar's 'Toy Story' Premieres", "description": "'Toy Story' debuts as the world's first feature-length fully computer-animated film."},
        {"year": 2000, "category": "Science & Tech", "title": "First Permanent Crew Boards the International Space Station", "description": "Expedition 1 docks with the ISS, beginning an uninterrupted human presence in orbit that has lasted ever since."},
        {"year": 2014, "category": "Science & Tech", "title": "Philae Lander Touches Down on a Comet", "description": "ESA's Rosetta mission achieves the first soft landing of a spacecraft on the nucleus of Comet 67P/Churyumov–Gerasimenko."},
    ],
    12: [
        {"year": 1901, "category": "World History", "title": "First Nobel Prizes Awarded in Stockholm", "description": "The inaugural Nobel Prizes in Physics, Chemistry, Medicine, Literature, and Peace are presented."},
        {"year": 1903, "category": "Science & Tech", "title": "Wright Brothers Achieve First Powered Flight", "description": "At Kitty Hawk, North Carolina, Orville and Wilbur Wright make the first controlled, sustained, powered heavier-than-air flights."},
        {"year": 1911, "category": "World History", "title": "Roald Amundsen Reaches the Geographic South Pole", "description": "Norwegian explorer Roald Amundsen and his team become the first humans to reach the South Pole."},
        {"year": 1947, "category": "Science & Tech", "title": "Invention of the Transistor at Bell Labs", "description": "John Bardeen, Walter Brattain, and William Shockley demonstrate the point-contact transistor, the building block of all modern electronics."},
        {"year": 1955, "category": "World History", "title": "Rosa Parks Sparks the Montgomery Bus Boycott", "description": "Rosa Parks refuses to give up her seat on a segregated bus in Montgomery, Alabama, galvanizing the U.S. Civil Rights Movement."},
        {"year": 1968, "category": "Science & Tech", "title": "Apollo 8 Captures the 'Earthrise' Photograph", "description": "Orbiting the Moon for the first time, astronaut William Anders photographs Earth rising above the lunar horizon."},
    ],
}


# Famous birthdays organized by month so every birthday gets real famous birthday twins/companions
MONTHLY_FAMOUS_BIRTHS: dict[int, list[dict[str, Any]]] = {
    1: [
        {"year": 1706, "name": "Benjamin Franklin", "role": "Polymath, Scientist & Founding Father"},
        {"year": 1929, "name": "Martin Luther King Jr.", "role": "Civil Rights Leader & Nobel Laureate"},
        {"year": 1935, "name": "Elvis Presley", "role": "Cultural Icon & King of Rock and Roll"},
        {"year": 1942, "name": "Stephen Hawking", "role": "Theoretical Physicist & Cosmologist"},
        {"year": 1942, "name": "Muhammad Ali", "role": "Heavyweight Champion & Humanitarian"},
        {"year": 1954, "name": "Oprah Winfrey", "role": "Media Mogul & Philanthropist"},
    ],
    2: [
        {"year": 1564, "name": "Galileo Galilei", "role": "Father of Observational Astronomy"},
        {"year": 1809, "name": "Charles Darwin & Abraham Lincoln", "role": "Born on the exact same day (Feb 12, 1809)!"},
        {"year": 1847, "name": "Thomas Alva Edison", "role": "Prolific Inventor & Innovator"},
        {"year": 1913, "name": "Rosa Parks", "role": "First Lady of Civil Rights"},
        {"year": 1955, "name": "Steve Jobs", "role": "Co-founder of Apple & Pixar"},
        {"year": 1963, "name": "Michael Jordan", "role": "Basketball Legend"},
    ],
    3: [
        {"year": 1475, "name": "Michelangelo", "role": "Renaissance Sculptor, Painter & Architect"},
        {"year": 1685, "name": "Johann Sebastian Bach", "role": "Baroque Composer & Master Musician"},
        {"year": 1879, "name": "Albert Einstein", "role": "Theoretical Physicist (Relativity)"},
        {"year": 1928, "name": "Fred Rogers", "role": "Beloved Educator & Television Host"},
        {"year": 1947, "name": "Elton John", "role": "Legendary Singer, Pianist & Composer"},
        {"year": 1986, "name": "Lady Gaga", "role": "Grammy & Oscar-Winning Artist"},
    ],
    4: [
        {"year": 1452, "name": "Leonardo da Vinci", "role": "Renaissance Polymath, Artist & Engineer"},
        {"year": 1564, "name": "William Shakespeare", "role": "Playwright & Poet"},
        {"year": 1889, "name": "Charlie Chaplin", "role": "Silent Film Pioneer & Director"},
        {"year": 1916, "name": "Claude Shannon", "role": "Father of Information Theory"},
        {"year": 1926, "name": "Sir David Attenborough", "role": "Naturalist & Broadcaster"},
        {"year": 1934, "name": "Jane Goodall", "role": "Primatologist & Conservationist"},
    ],
    5: [
        {"year": 1820, "name": "Florence Nightingale", "role": "Founder of Modern Nursing & Statistician"},
        {"year": 1907, "name": "Katharine Hepburn", "role": "Four-Time Academy Award Winner"},
        {"year": 1918, "name": "Richard Feynman", "role": "Nobel Laureate Quantum Physicist"},
        {"year": 1925, "name": "Malcolm X", "role": "Human Rights Activist"},
        {"year": 1929, "name": "Audrey Hepburn", "role": "Film Icon & UNICEF Goodwill Ambassador"},
        {"year": 1944, "name": "George Lucas", "role": "Creator of Star Wars & Indiana Jones"},
    ],
    6: [
        {"year": 1623, "name": "Blaise Pascal", "role": "Mathematician, Physicist & Inventor"},
        {"year": 1910, "name": "Jacques Cousteau", "role": "Oceanographer & Undersea Explorer"},
        {"year": 1912, "name": "Alan Turing", "role": "Father of Theoretical Computer Science & AI"},
        {"year": 1926, "name": "Marilyn Monroe", "role": "Hollywood Legend"},
        {"year": 1955, "name": "Sir Tim Berners-Lee", "role": "Inventor of the World Wide Web"},
        {"year": 1971, "name": "Elon Musk", "role": "Aerospace & Electric Vehicle Entrepreneur"},
    ],
    7: [
        {"year": 1856, "name": "Nikola Tesla", "role": "Electrical Engineer & AC Power Pioneer"},
        {"year": 1907, "name": "Frida Kahlo", "role": "Celebrated Mexican Painter"},
        {"year": 1918, "name": "Nelson Mandela", "role": "Anti-Apartheid Leader & South African President"},
        {"year": 1920, "name": "Rosalind Franklin", "role": "Chemist & X-Ray Crystallographer (DNA)"},
        {"year": 1961, "name": "Princess Diana", "role": "Humanitarian & Global Icon"},
        {"year": 1997, "name": "Malala Yousafzai", "role": "Youngest Nobel Peace Prize Laureate"},
    ],
    8: [
        {"year": 1870, "name": "Maria Montessori", "role": "Physician & Educational Reformer"},
        {"year": 1901, "name": "Louis Armstrong", "role": "Jazz Trumpeter & Vocalist"},
        {"year": 1918, "name": "Katherine Johnson", "role": "NASA Orbital Mechanics Mathematician"},
        {"year": 1930, "name": "Neil Armstrong", "role": "First Human to Walk on the Moon"},
        {"year": 1958, "name": "Michael Jackson", "role": "King of Pop"},
        {"year": 1986, "name": "Usain Bolt", "role": "Fastest Sprinter in Recorded History"},
    ],
    9: [
        {"year": 1791, "name": "Michael Faraday", "role": "Electromagnetism Pioneer"},
        {"year": 1890, "name": "Agatha Christie", "role": "Best-Selling Novelist of All Time"},
        {"year": 1916, "name": "Roald Dahl", "role": "Beloved Storyteller & Author"},
        {"year": 1946, "name": "Freddie Mercury", "role": "Legendary Frontman of Queen"},
        {"year": 1956, "name": "Mae Jemison", "role": "Physician & First Black Woman in Space"},
        {"year": 1981, "name": "Serena Williams & Beyoncé", "role": "Icons of Sports and Music"},
    ],
    10: [
        {"year": 1869, "name": "Mahatma Gandhi", "role": "Leader of Nonviolent Independence"},
        {"year": 1881, "name": "Pablo Picasso", "role": "Co-founder of Cubism & Modern Art Titan"},
        {"year": 1914, "name": "Jonas Salk", "role": "Virologist & Polio Vaccine Developer"},
        {"year": 1940, "name": "John Lennon & Pelé", "role": "Legends of Music and World Football"},
        {"year": 1955, "name": "Bill Gates", "role": "Co-founder of Microsoft & Philanthropist"},
        {"year": 1967, "name": "Julia Roberts", "role": "Academy Award-Winning Actress"},
    ],
    11: [
        {"year": 1867, "name": "Marie Skłodowska-Curie", "role": "Only Person to Win Nobel Prizes in Two Sciences"},
        {"year": 1840, "name": "Claude Monet", "role": "Founder of French Impressionist Painting"},
        {"year": 1934, "name": "Carl Sagan", "role": "Astronomer & 'Cosmos' Creator"},
        {"year": 1940, "name": "Bruce Lee", "role": "Martial Artist & Philosopher"},
        {"year": 1942, "name": "Jimi Hendrix", "role": "Revolutionary Electric Guitarist"},
        {"year": 1974, "name": "Leonardo DiCaprio", "role": "Actor & Environmental Advocate"},
    ],
    12: [
        {"year": 1770, "name": "Ludwig van Beethoven", "role": "Classical & Romantic Era Composer"},
        {"year": 1815, "name": "Ada Lovelace", "role": "World's First Computer Programmer"},
        {"year": 1901, "name": "Walt Disney", "role": "Animation Pioneer & Storyteller"},
        {"year": 1906, "name": "Grace Hopper", "role": "Computer Scientist & Compiler Pioneer"},
        {"year": 1946, "name": "Steven Spielberg", "role": "Legendary Film Director"},
        {"year": 1989, "name": "Taylor Swift", "role": "Global Singer-Songwriter"},
    ],
}


# Decade & Year Time Capsule: gives rich context about the world when the user was born
DECADE_TIME_CAPSULES: dict[int, dict[str, Any]] = {
    1940: {
        "era_name": "The Atomic & Swing Era (1940s)",
        "world_population_billion": 2.35,
        "tech_vibe": "Vacuum tube computers (ENIAC), vinyl LP records, Polaroid instant cameras, and FM radio broadcasts.",
        "music_vibe": "Big Band Swing, Bebop Jazz (Duke Ellington, Ella Fitzgerald, Frank Sinatra, Charlie Parker).",
        "cinema_vibe": "Casablanca, Citizen Kane, It's a Wonderful Life, Fantasia.",
        "avg_movie_ticket": "$0.35",
        "avg_gallon_gas": "$0.21",
        "gold_per_oz": "$34.70",
        "headline_milestone": "First programmable electronic computers and the founding of the United Nations.",
    },
    1950: {
        "era_name": "The Dawn of the Space Age & Rock 'n' Roll (1950s)",
        "world_population_billion": 2.75,
        "tech_vibe": "Transistor radios, black-and-white living room TVs, commercial jet airliners, and the first solar cells.",
        "music_vibe": "Birth of Rock 'n' Roll & Cool Jazz (Elvis Presley, Chuck Berry, Miles Davis, Billie Holiday).",
        "cinema_vibe": "Singin' in the Rain, Seven Samurai, Rear Window, Roman Holiday.",
        "avg_movie_ticket": "$0.50",
        "avg_gallon_gas": "$0.29",
        "gold_per_oz": "$35.00",
        "headline_milestone": "Discovery of the DNA double helix and the launch of Sputnik 1 into orbit.",
    },
    1960: {
        "era_name": "The Apollo Moonshot & Counterculture Era (1960s)",
        "world_population_billion": 3.35,
        "tech_vibe": "Apollo Guidance Computer, colour television, laser beams, audio cassettes, and the first computer mouse prototype.",
        "music_vibe": "The British Invasion, Motown Soul & Psychedelic Rock (The Beatles, Aretha Franklin, Jimi Hendrix).",
        "cinema_vibe": "2001: A Space Odyssey, The Sound of Music, Psycho, Lawrence of Arabia.",
        "avg_movie_ticket": "$1.05",
        "avg_gallon_gas": "$0.32",
        "gold_per_oz": "$35.20",
        "headline_milestone": "Humanity walks on the Moon for the first time and the first ARPANET message is sent.",
    },
    1970: {
        "era_name": "The Microprocessor & Voyager Era (1970s)",
        "world_population_billion": 4.08,
        "tech_vibe": "First microprocessors (Intel 4004), Apple II & Atari 2600, Sony Walkman, floppy disks, and pocket calculators.",
        "music_vibe": "Classic Rock, Funk, Disco & Punk (Queen, Stevie Wonder, Pink Floyd, ABBA, David Bowie).",
        "cinema_vibe": "Star Wars (1977), The Godfather, Jaws, Alien, Rocky.",
        "avg_movie_ticket": "$2.05",
        "avg_gallon_gas": "$0.57",
        "gold_per_oz": "$160.00",
        "headline_milestone": "Voyager 1 & 2 launch with the Golden Record and personal computing begins in garages.",
    },
    1980: {
        "era_name": "The Neon Arcade & Personal PC Era (1980s)",
        "world_population_billion": 4.85,
        "tech_vibe": "Macintosh 128K, IBM PC, Nintendo Entertainment System (NES), Compact Discs (CDs), VHS camcorders, and Space Shuttles.",
        "music_vibe": "Synth-Pop, Golden Age Hip-Hop & Arena Rock (Michael Jackson, Prince, Whitney Houston, Madonna, U2).",
        "cinema_vibe": "Back to the Future, E.T. the Extra-Terrestrial, The Empire Strikes Back, Raiders of the Lost Ark.",
        "avg_movie_ticket": "$3.55",
        "avg_gallon_gas": "$1.15",
        "gold_per_oz": "$420.00",
        "headline_milestone": "The Berlin Wall falls, TCP/IP unites the Internet, and the World Wide Web is invented at CERN.",
    },
    1990: {
        "era_name": "The Dot-Com & Millennium Horizon Era (1990s)",
        "world_population_billion": 5.75,
        "tech_vibe": "Dial-up modems, Netscape Navigator, Game Boy, PlayStation 1, Windows 95, DVDs, and early SMS text messages.",
        "music_vibe": "90s R&B, Grunge, Britpop & Hip-Hop Classics (Nirvana, Mariah Carey, Oasis, Tupac, Daft Punk, Radiohead).",
        "cinema_vibe": "Jurassic Park, The Matrix, Toy Story, The Lion King, Titanic, Pulp Fiction.",
        "avg_movie_ticket": "$4.45",
        "avg_gallon_gas": "$1.18",
        "gold_per_oz": "$360.00",
        "headline_milestone": "The Hubble Space Telescope opens our eyes to deep space and the Web goes global.",
    },
    2000: {
        "era_name": "The Digital Revolution & iPod Era (2000s)",
        "world_population_billion": 6.55,
        "tech_vibe": "Click-wheel iPods, flip phones (Motorola RAZR), Wikipedia, YouTube, USB flash drives, Wi-Fi, and the first iPhone.",
        "music_vibe": "2000s Pop, Indie Rock & Hip-Hop (Beyoncé, Eminem, Coldplay, Amy Winehouse, Kanye West, Rihanna).",
        "cinema_vibe": "The Lord of the Rings Trilogy, Spirited Away, The Dark Knight, WALL-E, Avatar.",
        "avg_movie_ticket": "$6.40",
        "avg_gallon_gas": "$2.15",
        "gold_per_oz": "$550.00",
        "headline_milestone": "The Human Genome Project is completed and permanent human habitation begins aboard the ISS.",
    },
    2010: {
        "era_name": "The Smartphone, Streaming & Deep Space Era (2010s)",
        "world_population_billion": 7.40,
        "tech_vibe": "4G LTE smartphones, iPads, reusable Falcon 9 orbital rockets, smartwatch wearables, and cloud streaming.",
        "music_vibe": "Global Streaming Pop, EDM & Trap (Taylor Swift, Kendrick Lamar, Adele, Bruno Mars, The Weeknd, BTS).",
        "cinema_vibe": "Inception, Interstellar, Parasite, Mad Max: Fury Road, Avengers: Endgame, Spider-Man: Into the Spider-Verse.",
        "avg_movie_ticket": "$8.45",
        "avg_gallon_gas": "$2.80",
        "gold_per_oz": "$1,350.00",
        "headline_milestone": "Discovery of the Higgs Boson, detection of gravitational waves, and the first photo of a black hole.",
    },
    2020: {
        "era_name": "The AI & Artemis Cosmic Renaissance (2020s)",
        "world_population_billion": 8.05,
        "tech_vibe": "Generative AI models, James Webb Space Telescope infrared views, mRNA biotechnology, and electric aviation.",
        "music_vibe": "Hyper-global Pop, Afrobeats, Latin Trap & Indie Pop (Dua Lipa, Bad Bunny, Billie Eilish, Olivia Rodrigo, SZA).",
        "cinema_vibe": "Everything Everywhere All at Once, Dune, Oppenheimer, Inside Out 2.",
        "avg_movie_ticket": "$10.75",
        "avg_gallon_gas": "$3.40",
        "gold_per_oz": "$2,150.00",
        "headline_milestone": "James Webb Space Telescope peers to the dawn of galaxies and AI transforms human creativity.",
    },
}


def fetch_wikimedia_on_this_day(month: int, day: int, timeout: float = 2.5) -> dict[str, list[dict[str, Any]]] | None:
    """
    Attempts to fetch real-time 'On This Day' events and births from Wikimedia's official feed API.
    Gracefully returns None if offline or rate-limited so the app never fails.
    """
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{month:02d}/{day:02d}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ChronosCosmosBirthdayExplorer/1.0 (Educational Python Web App)",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            raw = json.loads(resp.read().decode("utf-8"))
            events_out = []
            for item in (raw.get("selected") or raw.get("events") or [])[:12]:
                year = item.get("year")
                text = item.get("text", "")
                pages = item.get("pages") or []
                title = pages[0].get("titles", {}).get("normalized", "Historical Milestone") if pages else "Historical Milestone"
                thumb = pages[0].get("thumbnail", {}).get("source") if pages else None
                wiki_url = pages[0].get("content_urls", {}).get("desktop", {}).get("page") if pages else None
                events_out.append({
                    "year": year,
                    "category": "World History",
                    "title": title,
                    "description": text,
                    "thumbnail": thumb,
                    "url": wiki_url,
                    "exact_date": True,
                })

            births_out = []
            for b in (raw.get("births") or [])[:8]:
                year = b.get("year")
                text = b.get("text", "")
                pages = b.get("pages") or []
                name = text.split(",")[0].strip() if "," in text else text
                role = text.split(",", 1)[1].strip().capitalize() if "," in text else "Notable Figure"
                thumb = pages[0].get("thumbnail", {}).get("source") if pages else None
                wiki_url = pages[0].get("content_urls", {}).get("desktop", {}).get("page") if pages else None
                births_out.append({
                    "year": year,
                    "name": name,
                    "role": role,
                    "thumbnail": thumb,
                    "url": wiki_url,
                    "exact_date": True,
                })

            if events_out:
                return {"events": events_out, "births": births_out, "source": "Wikimedia Live Feed + Curated Archive"}
    except Exception:
        return None
    return None


def get_historical_data_for_date(year: int, month: int, day: int, try_live: bool = True) -> dict[str, Any]:
    """
    Returns rich historical events, famous shared birthdays, and a birth-year time capsule
    for the given birth date. Combines exact-date matches, Wikimedia live feed (if available),
    and curated monthly/decade archives.
    """
    live_data = fetch_wikimedia_on_this_day(month, day) if try_live else None

    exact_events = list(EXACT_DATE_EVENTS.get((month, day), []))
    for ev in exact_events:
        ev["exact_date"] = True

    month_pool = MONTHLY_HISTORICAL_POOL.get(month, MONTHLY_HISTORICAL_POOL[1])
    # Deterministically rotate the monthly pool based on the day so each day highlights distinct items first
    offset = (day - 1) % len(month_pool)
    rotated_pool = month_pool[offset:] + month_pool[:offset]

    combined_events: list[dict[str, Any]] = []
    seen_titles: set[str] = set()

    if live_data and live_data.get("events"):
        for ev in live_data["events"]:
            if ev["title"] not in seen_titles:
                seen_titles.add(ev["title"])
                combined_events.append(ev)

    for ev in exact_events:
        if ev["title"] not in seen_titles:
            seen_titles.add(ev["title"])
            combined_events.append(ev)

    for ev in rotated_pool:
        if ev["title"] not in seen_titles:
            seen_titles.add(ev["title"])
            ev_copy = dict(ev)
            ev_copy["exact_date"] = False
            combined_events.append(ev_copy)

    # Sort events chronologically or keep featured ones at top
    # Famous births
    famous_births: list[dict[str, Any]] = []
    if live_data and live_data.get("births"):
        famous_births.extend(live_data["births"][:6])

    curated_births = MONTHLY_FAMOUS_BIRTHS.get(month, MONTHLY_FAMOUS_BIRTHS[1])
    for b in curated_births:
        if not any(b["name"].lower() in existing["name"].lower() for existing in famous_births):
            famous_births.append(dict(b, exact_date=False))

    # Decade time capsule
    decade = (year // 10) * 10
    if decade < 1940:
        decade_key = 1940
    elif decade > 2020:
        decade_key = 2020
    else:
        decade_key = decade

    capsule = dict(DECADE_TIME_CAPSULES.get(decade_key, DECADE_TIME_CAPSULES[2000]))
    # Interpolate world population for exact year
    next_decade_key = min(decade_key + 10, 2020)
    pop_start = DECADE_TIME_CAPSULES[decade_key]["world_population_billion"]
    pop_end = DECADE_TIME_CAPSULES[next_decade_key]["world_population_billion"]
    year_fraction = max(0.0, min(1.0, (year - decade_key) / 10.0))
    est_pop = round(pop_start + (pop_end - pop_start) * year_fraction, 2)
    capsule["estimated_world_population_billion"] = est_pop
    capsule["people_added_since_birth_billion"] = round(max(0.0, 8.20 - est_pop), 2)
    capsule["birth_year"] = year

    return {
        "events": combined_events[:10],
        "famous_births": famous_births[:6],
        "time_capsule": capsule,
        "source": live_data["source"] if live_data else "Curated Historical & Cosmic Archive",
    }

