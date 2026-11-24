(() => {
  'use strict';
  const progress = document.getElementById('scroll-progress-fill');
  const chapterLinks = [...document.querySelectorAll('[data-chapter]')];
  const sections = chapterLinks.map(a => document.getElementById(a.dataset.chapter)).filter(Boolean);
  let pending = false;

  function update() {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    if (progress) progress.style.width = Math.min(100, Math.max(0, scrollY / max * 100)) + '%';
    const threshold = Math.min(180, Math.max(130, window.innerHeight * 0.25));
    let active = sections[0]?.id;
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= threshold) active = section.id;
    }
    for (const link of chapterLinks) {
      const selected = link.dataset.chapter === active;
      link.classList.toggle('active', selected);
      if (selected) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
    pending = false;
  }

  function schedule() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(update);
    }
  }
  window.addEventListener('scroll', schedule, {passive: true});
  window.addEventListener('resize', schedule, {passive: true});
  window.addEventListener('hashchange', schedule);
  window.addEventListener('load', schedule);
  document.fonts?.ready.then(schedule);
  update();
})();
