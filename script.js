/* ==================================================
   Sumit Raghuwanshi — Portfolio interactions
   ================================================== */

/* ---------- Typewriter for hero role ---------- */
/* ✏️ EDIT: the phrases that type out in the hero */
const roles = [
  "AI & ML Developer 🤖",
  "Full-Stack Product Builder 💻",
  "Building @Apives & @Startives 🚀",
  "Java & DSA Enthusiast ☕",
  "Drone R&D Intern 🚁",
  "B.Tech AIML @SIRT Bhopal 🎓"
];

const typeEl = document.getElementById("typewriter");
let ri = 0, ci = 0, deleting = false;

function typeLoop() {
  if (!typeEl) return; // pages without a typewriter just skip
  const word = roles[ri];
  typeEl.textContent = word.slice(0, ci);
  let delay = deleting ? 45 : 90;

  if (!deleting && ci === word.length) {
    delay = 1800; deleting = true;
  } else if (deleting && ci === 0) {
    deleting = false;
    ri = (ri + 1) % roles.length;
    delay = 350;
  } else {
    ci += deleting ? -1 : 1;
  }
  setTimeout(typeLoop, delay);
}
typeLoop();

/* ---------- Navbar: scrolled style, mobile menu, active link ---------- */
const navbar = document.getElementById("navbar");
const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");
const links = document.querySelectorAll(".nav-link");

navToggle.addEventListener("click", () => {
  const open = navLinks.classList.toggle("open");
  navToggle.classList.toggle("open", open);
  navToggle.setAttribute("aria-expanded", open);
});
links.forEach(l => l.addEventListener("click", () => {
  navLinks.classList.remove("open");
  navToggle.classList.remove("open");
}));

window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 30);

  // highlight current section in the menu
  const pos = window.scrollY + 140;
  document.querySelectorAll("section[id]").forEach(sec => {
    if (pos >= sec.offsetTop && pos < sec.offsetTop + sec.offsetHeight) {
      links.forEach(l => l.classList.toggle("active", l.getAttribute("href") === "#" + sec.id));
    }
  });
}, { passive: true });

/* ---------- Reveal on scroll ---------- */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add("visible");
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach(el => revealObs.observe(el));

/* ---------- Animated skill bars & counters ---------- */
const fillObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const card = e.target;
    const pct = card.querySelector(".skill-pct").dataset.pct;
    card.querySelector(".skill-fill").style.width = pct + "%";
    countUp(card.querySelector(".skill-pct"), 0, pct, "%", 1200);
    fillObs.unobserve(card);
  });
}, { threshold: 0.4 });
document.querySelectorAll(".skill").forEach(el => fillObs.observe(el));

function countUp(el, from, to, suffix = "", ms = 1400) {
  const t0 = performance.now();
  function step(t) {
    const p = Math.min((t - t0) / ms, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(from + (to - from) * eased) + suffix;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

const factObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const n = e.target;
    countUp(n.querySelector(".fact-num"), 0, +n.querySelector(".fact-num").dataset.count,
            n.querySelector(".fact-num").dataset.suffix || "");
    factObs.unobserve(n);
  });
}, { threshold: 0.5 });
document.querySelectorAll(".fact").forEach(el => factObs.observe(el));

/* ---------- Cursor glow ---------- */
const glow = document.querySelector(".cursor-glow");
window.addEventListener("pointermove", e => {
  glow.style.left = e.clientX + "px";
  glow.style.top = e.clientY + "px";
}, { passive: true });

/* ---------- 3D tilt on project cards ---------- */
document.querySelectorAll("[data-tilt]").forEach(card => {
  card.addEventListener("pointermove", e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - .5;
    const y = (e.clientY - r.top) / r.height - .5;
    card.style.transform = `perspective(900px) rotateY(${x * 10}deg) rotateX(${-y * 8}deg) translateY(-4px)`;
  });
  card.addEventListener("pointerleave", () => { card.style.transform = ""; });
});

/* ---------- 3D parallax on hero photo (follows the cursor) ---------- */
const heroPhoto = document.getElementById("heroPhoto3d");
const heroWord = document.querySelector(".hero-word");
if (heroPhoto && window.matchMedia("(hover:hover)").matches) {
  window.addEventListener("pointermove", e => {
    const x = e.clientX / window.innerWidth - .5;   // -0.5 … 0.5
    const y = e.clientY / window.innerHeight - .5;
    heroPhoto.style.transform =
      `perspective(1100px) rotateY(${x * 6}deg) rotateX(${-y * 4}deg) translateZ(18px)`;
    if (heroWord) heroWord.style.transform =
      `translateX(-50%) translate(${x * -14}px, ${y * -8}px)`;
  }, { passive: true });
  window.addEventListener("pointerleave", () => {
    heroPhoto.style.transform = "";
    if (heroWord) heroWord.style.transform = "";
  });
}

/* ---------- Contact form (demo handler) ---------- */
/* ✏️ EDIT: for real email delivery, point the form at a service like
   Formspree: replace the demo handler below with
   form.action = "https://formspree.io/f/YOUR_ID" and method="POST".   */
const form = document.getElementById("contactForm");
const status = document.getElementById("formStatus");
form && form.addEventListener("submit", e => {
  e.preventDefault();
  status.textContent = "✅ Thanks! (Demo mode — connect a form service to actually send.)";
  form.reset();
});

