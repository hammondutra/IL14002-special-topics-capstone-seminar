(() => {
  'use strict';
  const progress = document.getElementById('scroll-progress-fill');
  const chapterLinks = [...document.querySelectorAll('[data-chapter]')];
  const sections = chapterLinks.map((a) => document.getElementById(a.dataset.chapter)).filter(Boolean);
  let framePending = false;

  function updateScroll() {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const percent = Math.min(100, Math.max(0, window.scrollY / max * 100));
    if (progress) progress.style.width = `${percent}%`;
    framePending = false;
  }
  window.addEventListener('scroll', () => {
    if (framePending) return;
    framePending = true;
    window.requestAnimationFrame(updateScroll);
  }, { passive: true });
  window.addEventListener('resize', updateScroll, { passive: true });
  updateScroll();


  if ('IntersectionObserver' in window) {
    const navigationObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        chapterLinks.forEach((a) => {
          const active = a.dataset.chapter === entry.target.id;
          a.classList.toggle('active', active);
          if (active) a.setAttribute('aria-current', 'location');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-12% 0px -68% 0px', threshold: 0 });
    sections.forEach((section) => navigationObserver.observe(section));

  }
})();
