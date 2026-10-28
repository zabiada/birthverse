/**
 * BirthVerse — Client-Side Interactive Engine
 * Developed by Zabiada Arman
 *
 * Handles live-ticking counters, SVG lunar phase rendering, starfield canvas,
 * celebration confetti, smooth section navigation, and API communication.
 */

(() => {
  "use strict";

  let activeProfile = null;
  let liveTickerInterval = null;

  // DOM References
  const form = document.getElementById("birthday-form");
  const inputName = document.getElementById("input-name");
  const inputDate = document.getElementById("input-date");
  const errorBanner = document.getElementById("error-banner");
  const dashboard = document.getElementById("results-dashboard");

  const numFmt = new Intl.NumberFormat("en-US");

  // ---------------------------------------------------------------------------
  // 1. Web Audio API Gentle Harmonic Chime
  // ---------------------------------------------------------------------------
  function playCosmicChime() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const notes = [523.25, 659.25, 783.99, 1046.5];
      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);
        gain.gain.setValueAtTime(0.001, ctx.currentTime + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.045, ctx.currentTime + idx * 0.08 + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + idx * 0.08 + 1.1);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.08);
        osc.stop(ctx.currentTime + idx * 0.08 + 1.15);
      });
    } catch (_) {}
  }

  // ---------------------------------------------------------------------------
  // 2. Subtle Ambient Starfield Background
  // ---------------------------------------------------------------------------
  function initStarfield() {
    const canvas = document.getElementById("starfield-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const stars = Array.from({ length: 110 }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 1.4 + 0.3,
      alpha: Math.random() * 0.65 + 0.15,
      speed: Math.random() * 0.14 + 0.03,
      twinkle: Math.random() * 0.015 + 0.004,
    }));

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    function renderStars() {
      ctx.clearRect(0, 0, width, height);
      for (const s of stars) {
        s.y -= s.speed;
        if (s.y < 0) {
          s.y = height;
          s.x = Math.random() * width;
        }
        s.alpha += s.twinkle;
        if (s.alpha > 0.85 || s.alpha < 0.15) s.twinkle = -s.twinkle;

        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(226, 232, 240, ${s.alpha.toFixed(2)})`;
        ctx.fill();
      }
      requestAnimationFrame(renderStars);
    }
    renderStars();
  }

  // ---------------------------------------------------------------------------
  // 3. Confetti Celebration Burst
  // ---------------------------------------------------------------------------
  function triggerConfetti() {
    const canvas = document.getElementById("confetti-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ["#38bdf8", "#a855f7", "#ec4899", "#fbbf24", "#34d399"];
    const particles = Array.from({ length: 65 }, () => ({
      x: canvas.width / 2 + (Math.random() - 0.5) * 260,
      y: canvas.height * 0.28,
      vx: (Math.random() - 0.5) * 10,
      vy: Math.random() * -8 - 3,
      size: Math.random() * 6 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      rot: Math.random() * Math.PI * 2,
      vrot: (Math.random() - 0.5) * 0.18,
      alpha: 1,
    }));

    let frame = 0;
    function animateConfetti() {
      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = false;
      for (const p of particles) {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.24;
        p.rot += p.vrot;
        p.alpha -= 0.013;
        if (p.alpha > 0) {
          alive = true;
          ctx.save();
          ctx.globalAlpha = Math.max(0, p.alpha);
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rot);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
          ctx.restore();
        }
      }
      if (alive && frame < 105) {
        requestAnimationFrame(animateConfetti);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }
    animateConfetti();
  }

  // ---------------------------------------------------------------------------
  // 4. Dynamic SVG Moon Phase Renderer
  // ---------------------------------------------------------------------------
  function renderMoonSVG(cyclePosition) {
    const svg = document.getElementById("moon-svg");
    if (!svg) return;

    const r = 46;
    const cx = 60;
    const cy = 60;

    const isWaxing = cyclePosition <= 0.5;
    const phaseNorm = isWaxing ? cyclePosition * 2 : (cyclePosition - 0.5) * 2;
    const rx = Math.abs(Math.cos(phaseNorm * Math.PI)) * r;

    let litPath = "";
    if (cyclePosition < 0.02 || cyclePosition > 0.98) {
      litPath = "";
    } else if (Math.abs(cyclePosition - 0.5) < 0.02) {
      litPath = `<circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#moonLitGrad)" />`;
    } else if (isWaxing) {
      const sweepTerminator = cyclePosition < 0.25 ? 0 : 1;
      litPath = `<path d="M ${cx} ${cy - r} A ${r} ${r} 0 0 1 ${cx} ${cy + r} A ${rx.toFixed(2)} ${r} 0 0 ${sweepTerminator} ${cx} ${cy - r} Z" fill="url(#moonLitGrad)" />`;
    } else {
      const sweepTerminator = cyclePosition < 0.75 ? 1 : 0;
      litPath = `<path d="M ${cx} ${cy - r} A ${r} ${r} 0 0 0 ${cx} ${cy + r} A ${rx.toFixed(2)} ${r} 0 0 ${sweepTerminator} ${cx} ${cy - r} Z" fill="url(#moonLitGrad)" />`;
    }

    svg.innerHTML = `
      <defs>
        <radialGradient id="moonLitGrad" cx="35%" cy="35%" r="70%">
          <stop offset="0%" stop-color="#fef9c3" />
          <stop offset="65%" stop-color="#fde047" />
          <stop offset="100%" stop-color="#ca8a04" />
        </radialGradient>
        <filter id="moonGlow" x="-25%" y="-25%" width="150%" height="150%">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>
      <circle cx="${cx}" cy="${cy}" r="${r + 5}" fill="rgba(253, 224, 71, 0.08)" />
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="#141c33" stroke="rgba(148,163,184,0.32)" stroke-width="1.5" />
      <g filter="url(#moonGlow)">
        ${litPath}
      </g>
      <circle cx="46" cy="44" r="5.5" fill="rgba(15, 23, 42, 0.18)" />
      <circle cx="72" cy="52" r="8.5" fill="rgba(15, 23, 42, 0.14)" />
      <circle cx="55" cy="74" r="7" fill="rgba(15, 23, 42, 0.16)" />
    `;
  }

  // ---------------------------------------------------------------------------
  // 5. Render Historical Events & Famous Birthdays with Filtering
  // ---------------------------------------------------------------------------
  function renderHistorySection(history, monthDayFormatted) {
    document.getElementById("res-history-date-label").textContent = monthDayFormatted;
    document.getElementById("res-history-source").textContent = history.source || "Curated Historical Archive";

    const eventsGrid = document.getElementById("history-events-grid");
    const birthsWrapper = document.getElementById("famous-births-wrapper");
    const birthsGrid = document.getElementById("famous-births-grid");

    function populateEvents(filterCategory) {
      if (filterCategory === "births") {
        eventsGrid.classList.add("hidden");
        birthsWrapper.classList.remove("hidden");
        return;
      }

      eventsGrid.classList.remove("hidden");
      birthsWrapper.classList.remove("hidden");

      const filtered =
        filterCategory === "all"
          ? history.events
          : history.events.filter((ev) =>
              (ev.category || "").toLowerCase().includes(filterCategory.toLowerCase().split(" ")[0])
            );

      const listToShow = filtered.length > 0 ? filtered : history.events;

      eventsGrid.innerHTML = listToShow
        .map((ev) => {
          const badgeNote = ev.exact_date ? `Recorded on ${monthDayFormatted}` : "Era & Month Highlight";
          const linkHtml = ev.url
            ? `<a href="${ev.url}" target="_blank" rel="noopener noreferrer" class="wiki-link">Source Reference ↗</a>`
            : `<span>Historical Archive</span>`;
          return `
            <article class="event-card glass-card">
              <div>
                <div class="event-top">
                  <span class="event-year-badge">${ev.year}</span>
                  <span class="event-cat-pill">${ev.category || "World History"}</span>
                </div>
                <h3 class="event-title">${ev.title}</h3>
                <p class="event-desc">${ev.description}</p>
              </div>
              <div class="event-footer">
                <span>${badgeNote}</span>
                ${linkHtml}
              </div>
            </article>
          `;
        })
        .join("");
    }

    birthsGrid.innerHTML = (history.famous_births || [])
      .map((b) => {
        const initials = b.name
          .split(" ")
          .slice(0, 2)
          .map((w) => w[0] || "")
          .join("")
          .toUpperCase();
        return `
          <div class="birth-card glass-card">
            <div class="birth-avatar">${initials}</div>
            <div>
              <div class="birth-name">${b.name} <span class="highlight-cyan">(${b.year})</span></div>
              <div class="birth-role">${b.role}</div>
            </div>
          </div>
        `;
      })
      .join("");

    populateEvents("all");

    const tabBtns = document.querySelectorAll(".filter-tabs .tab-btn");
    tabBtns.forEach((btn) => {
      btn.onclick = () => {
        tabBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        populateEvents(btn.getAttribute("data-filter"));
      };
    });
  }

  // ---------------------------------------------------------------------------
  // 6. Populate Full Profile & Start Real-Time Ticker
  // ---------------------------------------------------------------------------
  function renderProfile(profile, celebrate = true) {
    activeProfile = profile;
    dashboard.classList.remove("hidden");
    errorBanner.classList.add("hidden");

    const { user, age_breakdown, next_birthday, biometrics, cosmic_journey, astronomy, milestones, history } = profile;

    // 1. Identity & Next Birthday
    document.getElementById("res-serial").textContent = user.serial_code;
    document.getElementById("res-greeting-name").textContent = user.name;
    document.getElementById("res-birth-weekday").textContent = user.birth_weekday;
    document.getElementById("res-weekday-lore").textContent = user.weekday_lore;
    document.getElementById("res-full-birthdate").textContent = user.birth_date_formatted;
    document.getElementById("res-day-of-year").textContent = `Day ${user.day_of_year} of the Year`;
    document.getElementById("res-leap-tag").textContent = `${age_breakdown.leap_years_experienced} Leap Days Lived`;
    document.getElementById("res-seasons-tag").textContent = `${numFmt.format(age_breakdown.seasons_experienced)} Seasons Experienced`;

    document.getElementById("res-next-turning").textContent = `Turning ${next_birthday.turning_age}`;
    document.getElementById("res-next-days").textContent = next_birthday.days_remaining;
    document.getElementById("res-next-hours").textContent = next_birthday.hours_remaining;
    document.getElementById("res-next-mins").textContent = next_birthday.minutes_remaining;
    document.getElementById("res-bday-progress").style.width = `${Math.min(100, Math.max(4, next_birthday.progress_pct))}%`;
    document.getElementById("res-next-date-sub").textContent = `${next_birthday.date_formatted} · Falls on a ${next_birthday.weekday}`;

    // Calendar Age
    document.getElementById("res-years").textContent = age_breakdown.years;
    document.getElementById("res-months").textContent = age_breakdown.months;
    document.getElementById("res-days").textContent = age_breakdown.days;
    document.getElementById("res-total-months-weeks").textContent = `${numFmt.format(age_breakdown.total_months)} total months · ${numFmt.format(age_breakdown.total_weeks)} total weeks`;

    // 2. History & Famous Births
    renderHistorySection(history, user.month_day_formatted);

    // 3. Time Capsule
    const cap = history.time_capsule;
    document.getElementById("res-capsule-year").textContent = cap.birth_year;
    document.getElementById("res-capsule-era").textContent = cap.era_name;
    document.getElementById("res-capsule-headline").textContent = cap.headline_milestone;
    document.getElementById("res-capsule-tech").textContent = cap.tech_vibe;
    document.getElementById("res-capsule-music").textContent = cap.music_vibe;
    document.getElementById("res-capsule-cinema").textContent = cap.cinema_vibe;
    document.getElementById("res-pop-then").textContent = `${cap.estimated_world_population_billion}B`;
    document.getElementById("res-pop-added").textContent = `+${cap.people_added_since_birth_billion}B`;
    document.getElementById("res-price-movie").textContent = cap.avg_movie_ticket;
    document.getElementById("res-price-gas").textContent = cap.avg_gallon_gas;
    document.getElementById("res-price-gold").textContent = cap.gold_per_oz;

    // 4. Static Biometrics & Cosmic Sub-labels
    document.getElementById("res-blood-pumped").textContent = `Approx. ${numFmt.format(biometrics.liters_blood_pumped)} liters circulated`;
    document.getElementById("res-hours-slept").textContent = `${numFmt.format(biometrics.hours_slept)} hrs`;
    document.getElementById("res-dreams-sub").textContent = `~${biometrics.years_slept} years asleep · ~${numFmt.format(biometrics.dreams_had)} dream cycles`;
    document.getElementById("res-moon-trips").textContent = `Equivalent to ${numFmt.format(cosmic_journey.moon_trips_equivalent)} lunar transit distances`;
    document.getElementById("res-full-moons").textContent = `Witnessed ${numFmt.format(cosmic_journey.full_moons_seen)} full synodic moons since birth`;

    // 5. Astronomy, Moon, Zodiac & Planets
    const moon = astronomy.moon_phase;
    document.getElementById("res-moon-illum").textContent = `${moon.illumination_pct}% Illuminated`;
    document.getElementById("res-moon-name").textContent = moon.phase_name;
    document.getElementById("res-moon-age").textContent = `Day ${moon.lunar_age_days} of 29.5-day synodic cycle`;
    document.getElementById("res-moon-lore").textContent = moon.lore;
    renderMoonSVG(moon.cycle_position);

    const wz = astronomy.western_zodiac;
    const cz = astronomy.chinese_zodiac;
    document.getElementById("res-zodiac-element").textContent = `${wz.element} · ${wz.modality}`;
    document.getElementById("res-west-symbol").textContent = wz.symbol;
    document.getElementById("res-west-sign").textContent = wz.sign;
    document.getElementById("res-west-ruler").textContent = `Ruled by ${wz.ruler}`;
    document.getElementById("res-east-code").textContent = cz.code;
    document.getElementById("res-east-title").textContent = cz.full_title;
    document.getElementById("res-zodiac-traits").textContent = `${wz.sign}: ${wz.traits} (${cz.full_title}: ${cz.traits})`;

    const stone = astronomy.birthstone;
    document.getElementById("res-birth-season").textContent = stone.season_north;
    document.getElementById("res-stone-name").textContent = stone.stone;
    document.getElementById("res-flower-name").textContent = `Floral Symbol: ${stone.flower}`;
    document.getElementById("res-stone-meaning").textContent = `Symbolizes: ${stone.meaning}.`;
    const gemOrb = document.getElementById("res-gem-orb");
    gemOrb.style.background = `radial-gradient(circle at 30% 30%, rgba(255,255,255,0.35), ${stone.color})`;
    gemOrb.style.boxShadow = `0 0 24px ${stone.color}66`;

    const planetsGrid = document.getElementById("planets-grid");
    planetsGrid.innerHTML = astronomy.planetary_ages
      .map(
        (p) => `
        <div class="planet-card glass-card">
          <div class="planet-top">
            <span class="planet-name">${p.name}</span>
            <span class="planet-code" style="color: ${p.color}">${p.code}</span>
          </div>
          <div class="planet-age" style="color: ${p.color}">${p.age} <small style="font-size:0.7rem;color:var(--text-muted)">yrs</small></div>
          <div class="planet-next">Turn ${p.next_birthday_age} on ${p.next_birthday_date}</div>
        </div>
      `
      )
      .join("");

    // 6. Unusual Temporal Milestones
    const milestonesGrid = document.getElementById("milestones-grid");
    milestonesGrid.innerHTML = milestones
      .map(
        (m) => `
        <div class="milestone-card glass-card ${m.is_past ? "past-milestone" : "future-milestone"}">
          <div>
            <div class="m-top">
              <span class="m-tag">${m.tag}</span>
              <span class="m-badge ${m.is_past ? "past" : "future"}">${m.status_text}</span>
            </div>
            <div class="m-title">${m.label}</div>
            <div class="m-date">${m.date_formatted}</div>
          </div>
          <div class="m-desc">${m.desc}</div>
        </div>
      `
      )
      .join("");

    // 7. Life Summary Card
    document.getElementById("pass-name").textContent = user.name;
    document.getElementById("pass-origin").textContent = `${user.birth_date_iso} (${user.birth_weekday})`;
    document.getElementById("pass-serial").textContent = user.serial_code;
    document.getElementById("pass-days-hours").textContent = `${numFmt.format(age_breakdown.total_days)} Days / ${numFmt.format(age_breakdown.total_hours)} Hrs`;
    document.getElementById("pass-astro").textContent = `${moon.phase_name} · ${wz.sign}`;
    document.getElementById("pass-distance").textContent = `${numFmt.format(cosmic_journey.solar_orbit_km)} km`;

    // Start Live Real-Time Ticker
    startLiveCounters(user.birth_timestamp_ms);

    if (celebrate) {
      playCosmicChime();
      triggerConfetti();
    }
  }

  // ---------------------------------------------------------------------------
  // 7. Real-Time Ticking Engine (Updates Every Second)
  // ---------------------------------------------------------------------------
  function startLiveCounters(birthTimestampMs) {
    if (liveTickerInterval) clearInterval(liveTickerInterval);

    function updateTick() {
      const nowMs = Date.now();
      const elapsedSec = Math.max(1, Math.floor((nowMs - birthTimestampMs) / 1000));
      const elapsedMins = Math.floor(elapsedSec / 60);
      const elapsedHours = Math.floor(elapsedSec / 3600);
      const elapsedDays = Math.floor(elapsedSec / 86400);

      document.getElementById("live-days").textContent = numFmt.format(elapsedDays);
      document.getElementById("live-hours").textContent = numFmt.format(elapsedHours);
      document.getElementById("live-minutes-sub").textContent = `${numFmt.format(elapsedMins)} total minutes experienced`;
      document.getElementById("live-seconds").textContent = numFmt.format(elapsedSec);

      const heartbeats = Math.floor(elapsedSec * (72.0 / 60.0));
      const breaths = Math.floor(elapsedSec * (16.0 / 60.0));
      const blinks = Math.floor(elapsedSec * (15.0 / 60.0) * (16.0 / 24.0));
      const solarKm = Math.floor(elapsedSec * 29.78);
      const galaxyKm = Math.floor(elapsedSec * 230.0);

      document.getElementById("live-heartbeats").textContent = numFmt.format(heartbeats);
      document.getElementById("live-breaths").textContent = numFmt.format(breaths);
      document.getElementById("live-blinks").textContent = numFmt.format(blinks);
      document.getElementById("live-solar-km").textContent = `${numFmt.format(solarKm)} km`;
      document.getElementById("live-galaxy-km").textContent = `${numFmt.format(galaxyKm)} km`;
    }

    updateTick();
    liveTickerInterval = setInterval(updateTick, 1000);
  }

  // ---------------------------------------------------------------------------
  // 8. Smooth Section Navigation & Active Link Highlight
  // ---------------------------------------------------------------------------
  const secLinks = document.querySelectorAll(".section-nav .sec-link");
  secLinks.forEach((link) => {
    link.addEventListener("click", () => {
      secLinks.forEach((l) => l.classList.remove("active"));
      link.classList.add("active");
    });
  });

  // ---------------------------------------------------------------------------
  // 9. API Submission & Event Listeners
  // ---------------------------------------------------------------------------
  async function fetchAndRenderBirthday(date, name, celebrate = true) {
    try {
      const qs = new URLSearchParams({ date, name: name || "" });
      const res = await fetch(`/api/analyze?${qs.toString()}`);
      const payload = await res.json();
      if (!res.ok || !payload.ok) {
        errorBanner.textContent = payload.error || "Unable to analyze that birth date.";
        errorBanner.classList.remove("hidden");
        return;
      }
      renderProfile(payload.data, celebrate);
    } catch (err) {
      errorBanner.textContent = `Connection error: ${err.message}`;
      errorBanner.classList.remove("hidden");
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    fetchAndRenderBirthday(inputDate.value, inputName.value, true);
  });

  // Copy Summary & Print Card
  document.getElementById("btn-copy-summary").addEventListener("click", async () => {
    if (!activeProfile) return;
    const u = activeProfile.user;
    const a = activeProfile.age_breakdown;
    const as = activeProfile.astronomy;
    const summary = [
      `BIRTHVERSE LIFE SUMMARY (${u.serial_code})`,
      `Developed by Zabiada Arman`,
      `Name: ${u.name}`,
      `Born: ${u.birth_date_formatted} (${u.birth_weekday})`,
      `Lived: ${numFmt.format(a.total_days)} Days · ${numFmt.format(a.total_hours)} Hours · ${numFmt.format(a.total_seconds)} Seconds`,
      `Moon at Birth: ${as.moon_phase.phase_name} (${as.moon_phase.illumination_pct}% illuminated)`,
      `Zodiac: ${as.western_zodiac.sign} | ${as.chinese_zodiac.full_title}`,
      `Distance Orbiting the Sun: ${numFmt.format(activeProfile.cosmic_journey.solar_orbit_km)} km`,
    ].join("\n");

    try {
      await navigator.clipboard.writeText(summary);
      const btn = document.getElementById("btn-copy-summary");
      const orig = btn.textContent;
      btn.textContent = "Copied to Clipboard";
      setTimeout(() => (btn.textContent = orig), 2200);
    } catch (_) {}
  });

  document.getElementById("btn-print-passport").addEventListener("click", () => {
    window.print();
  });

  // Initial Boot
  initStarfield();
  const defaultDate = "2000-10-28";
  inputDate.value = defaultDate;
  fetchAndRenderBirthday(defaultDate, "", false);
})();
