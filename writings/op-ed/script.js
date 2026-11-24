(() => {
  'use strict';
  const progress = document.getElementById('scroll-progress-fill');
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
})();
