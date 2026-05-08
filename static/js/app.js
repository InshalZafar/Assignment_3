// ============================================================
//  LUXE TOURISM — front-end interactions
// ============================================================
(function () {
  'use strict';

  // ---- Theme toggle (persisted) ----
  const root = document.documentElement;
  const stored = localStorage.getItem('luxe-theme');
  if (stored === 'light') root.setAttribute('data-theme', 'light');

  document.addEventListener('click', (e) => {
    const t = e.target.closest('.theme-toggle');
    if (!t) return;
    const cur = root.getAttribute('data-theme');
    if (cur === 'light') {
      root.removeAttribute('data-theme');
      localStorage.setItem('luxe-theme', 'dark');
      t.textContent = '☾';
    } else {
      root.setAttribute('data-theme', 'light');
      localStorage.setItem('luxe-theme', 'light');
      t.textContent = '☀';
    }
  });

  // ---- Mobile menu ----
  document.addEventListener('click', (e) => {
    const m = e.target.closest('.menu-toggle');
    if (!m) return;
    document.querySelector('.nav-links')?.classList.toggle('open');
  });

  // ---- Toasts (auto-dismiss) ----
  document.querySelectorAll('.toast').forEach((t) => {
    setTimeout(() => {
      t.classList.add('fade-out');
      setTimeout(() => t.remove(), 300);
    }, 4000);
  });

  // ---- Star rating widget ----
  document.querySelectorAll('.star-rating[data-input]').forEach((widget) => {
    const inputName = widget.dataset.input;
    const input = document.querySelector(`input[name="${inputName}"]`);
    if (!input) return;
    const stars = widget.querySelectorAll('.star');
    const setVisual = (val) => stars.forEach((s, i) => {
      s.classList.toggle('filled', i < val);
    });
    setVisual(parseInt(input.value || '0', 10));

    stars.forEach((s, i) => {
      s.addEventListener('mouseenter', () => stars.forEach((x, j) => x.classList.toggle('hover', j <= i)));
      s.addEventListener('mouseleave', () => stars.forEach((x) => x.classList.remove('hover')));
      s.addEventListener('click', () => {
        input.value = i + 1;
        setVisual(i + 1);
      });
    });
  });

  // ---- Wishlist toggle (AJAX) ----
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.heart-btn[data-dest]');
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    const id = btn.dataset.dest;
    try {
      const res = await fetch(`/wishlist/toggle/${id}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      if (res.redirected) {
        window.location.href = '/login';
        return;
      }
      const data = await res.json();
      btn.classList.toggle('active', data.added);
      btn.textContent = data.added ? '♥' : '♡';
      showToast(data.added ? 'Saved to wishlist' : 'Removed from wishlist', 'success');
    } catch (err) {
      window.location.href = `/wishlist/toggle/${id}`;
    }
  });

  // ---- Toast util ----
  function showToast(msg, kind) {
    let stack = document.querySelector('.toast-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.className = 'toast-stack';
      document.body.appendChild(stack);
    }
    const t = document.createElement('div');
    t.className = 'toast ' + (kind || '');
    t.textContent = msg;
    stack.appendChild(t);
    setTimeout(() => {
      t.classList.add('fade-out');
      setTimeout(() => t.remove(), 300);
    }, 3500);
  }
  window.showToast = showToast;

  // ---- Scroll-reveal ----
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.fade-up').forEach((el) => io.observe(el));

  // ---- Animated counters ----
  const animateNum = (el) => {
    const target = parseInt(el.dataset.count || '0', 10);
    const dur = 1200;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.floor(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString();
    };
    requestAnimationFrame(tick);
  };
  const counterIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        animateNum(e.target);
        counterIO.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach((el) => counterIO.observe(el));

  // ---- Lightbox gallery ----
  document.addEventListener('click', (e) => {
    const img = e.target.closest('.gallery img');
    if (img) {
      const lb = document.querySelector('.lightbox');
      if (lb) {
        lb.querySelector('img').src = img.dataset.full || img.src;
        lb.classList.add('active');
      }
      return;
    }
    if (e.target.matches('.lightbox, .lightbox .close-btn')) {
      document.querySelector('.lightbox')?.classList.remove('active');
    }
  });

  // ---- Hero search → /search?q=... ----
  document.querySelectorAll('form.search-hero').forEach((f) => {
    f.addEventListener('submit', (e) => {
      // standard GET submission to /search; nothing to do
    });
  });

  // ---- Weather widget (Open-Meteo, no key) ----
  document.querySelectorAll('[data-weather]').forEach(async (el) => {
    const lat = parseFloat(el.dataset.lat || '0');
    const lng = parseFloat(el.dataset.lng || '0');
    if (!lat && !lng) {
      el.querySelector('.temp').textContent = '—';
      el.querySelector('.cond').textContent = 'No coordinates';
      return;
    }
    try {
      const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current=temperature_2m,weather_code,wind_speed_10m`);
      const data = await res.json();
      const c = data.current || {};
      el.querySelector('.temp').textContent = (c.temperature_2m ?? '—') + '°C';
      el.querySelector('.cond').textContent = `Wind ${c.wind_speed_10m ?? '—'} km/h • Code ${c.weather_code ?? '—'}`;
    } catch (err) {
      el.querySelector('.temp').textContent = '—';
      el.querySelector('.cond').textContent = 'Weather unavailable';
    }
  });

  // ---- Active nav link ----
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach((a) => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  // ---- Parallax hero ----
  const hero = document.querySelector('.hero');
  if (hero) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      hero.style.backgroundPositionY = `${y * 0.4}px`;
    }, { passive: true });
  }
})();
