/* 一般法理学 — 交互脚本（原生 JS，零依赖）
   功能：主题切换(持久化+跟随系统)、移动端菜单、站内搜索浮层(Cmd/Ctrl+K 全文过滤) */
(function () {
  'use strict';
  var root = document.documentElement;

  // 主题
  var saved = localStorage.getItem('theme');
  if (saved) {
    root.setAttribute('data-theme', saved);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    root.setAttribute('data-theme', 'dark');
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  });

  // 移动端菜单
  document.querySelectorAll('[data-menu-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var nav = document.getElementById('nav-links');
      if (nav) nav.classList.toggle('open');
    });
  });

  // 搜索浮层
  var searchBtn = document.querySelector('[data-search-open]');
  var overlay = document.getElementById('search-overlay');
  var input = document.getElementById('search-input');
  if (searchBtn && overlay && input) {
    searchBtn.addEventListener('click', function () {
      overlay.classList.add('open');
      input.focus();
    });
    var closeBtn = overlay.querySelector('[data-search-close]');
    if (closeBtn) closeBtn.addEventListener('click', function () { overlay.classList.remove('open'); });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) overlay.classList.remove('open'); });
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      document.querySelectorAll('[data-searchable]').forEach(function (el) {
        var text = el.textContent.toLowerCase();
        el.style.display = (!q || text.indexOf(q) !== -1) ? '' : 'none';
      });
    });
  }

  // 译后记/后记 收起与展开（仅内容超长时显示按钮）
  document.querySelectorAll('.aw-toggle').forEach(function (btn) {
    var id = btn.getAttribute('data-target');
    var aw = id ? document.getElementById(id) : null;
    if (!aw) return;
    var fs = parseFloat(getComputedStyle(aw).fontSize) || 16;
    var threshold = 32 * fs; // 与 CSS .afterword.collapsible max-height:32em 对应
    aw.classList.add('collapsible');
    if (aw.scrollHeight > threshold + 24) {
      btn.hidden = false;
    } else {
      aw.classList.remove('collapsible'); // 内容较短则不裁剪、不显示按钮
    }
    btn.addEventListener('click', function () {
      var expanded = aw.classList.toggle('expanded');
      btn.classList.toggle('expanded', expanded);
      btn.textContent = expanded ? '收起' : '展开全文';
    });
  });

  // Cmd/Ctrl + K 唤起搜索
  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchBtn) searchBtn.click();
    }
  });
})();
