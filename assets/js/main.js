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

  // 订阅按钮 + 弹窗（全站注入；邮件订阅后端：SendFox）
  var SFX_ID = (window.SITE_CONFIG && window.SITE_CONFIG.subscribe && window.SITE_CONFIG.subscribe.sendfoxFormId) || '';
  var SFX_OK = SFX_ID && SFX_ID.indexOf('YOUR_') !== 0;

  var nav = document.getElementById('nav-links');
  if (nav) {
    var sb = document.createElement('button');
    sb.className = 'icon-btn';
    sb.setAttribute('data-subscribe-open', '');
    sb.textContent = '订阅';
    nav.appendChild(sb);
  }

  var subBox;
  if (SFX_OK) {
    subBox =
      '<div class="subscribe-box">' +
      '  <h2>订阅更新</h2>' +
      '  <p>留下你的邮箱，本站有新著译或文章发布时，你会收到邮件通知。随时可退订。</p>' +
      '  <div id="sendfox-mount"></div>' +
      '  <button class="icon-btn subscribe-close" data-subscribe-close>关闭</button>' +
      '</div>';
  } else {
    subBox =
      '<div class="subscribe-box">' +
      '  <h2>订阅更新</h2>' +
      '  <p>订阅服务正在开通，敬请期待。你也可以通过 <a class="feed-link" href="feed.xml" target="_blank">RSS</a> 订阅本站更新。</p>' +
      '  <button class="icon-btn subscribe-close" data-subscribe-close>关闭</button>' +
      '</div>';
  }

  var subOverlay = document.createElement('div');
  subOverlay.className = 'subscribe-overlay';
  subOverlay.id = 'subscribe-overlay';
  subOverlay.innerHTML = subBox;
  document.body.appendChild(subOverlay);

  // 懒加载 SendFox 表单（点击「订阅」首次打开时注入，避免每页都加载第三方脚本）
  var sfxInited = false;
  function initSendFox() {
    if (!SFX_OK || sfxInited) return;
    sfxInited = true;
    var mount = document.getElementById('sendfox-mount');
    if (!mount) return;
    var d = document.createElement('div');
    d.className = 'sendfox-form';
    d.id = SFX_ID;
    mount.appendChild(d);
    var s = document.createElement('script');
    s.src = 'https://cdn.sendfox.com/js/embed.js';
    s.setAttribute('data-form', SFX_ID);
    s.setAttribute('data-api', 'https://sendfox.com');
    s.async = true;
    document.body.appendChild(s);
  }

  document.querySelectorAll('[data-subscribe-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      subOverlay.classList.add('open');
      initSendFox();
    });
  });
  var subCloseBtn = subOverlay.querySelector('[data-subscribe-close]');
  if (subCloseBtn) subCloseBtn.addEventListener('click', function () { subOverlay.classList.remove('open'); });
  subOverlay.addEventListener('click', function (e) { if (e.target === subOverlay) subOverlay.classList.remove('open'); });

  // 摄影作品灯箱（点击看大图）
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.id = 'lightbox';
  document.body.appendChild(lb);
  lb.addEventListener('click', function () { lb.classList.remove('open'); lb.innerHTML = ''; });
  document.querySelectorAll('.photo-item img').forEach(function (img) {
    img.addEventListener('click', function () {
      lb.innerHTML = '';
      var big = document.createElement('img');
      big.src = img.src;
      lb.appendChild(big);
      lb.classList.add('open');
    });
  });

  // Cmd/Ctrl + K 唤起搜索
  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchBtn) searchBtn.click();
    }
    if (e.key === 'Escape') {
      subOverlay.classList.remove('open');
      lb.classList.remove('open');
    }
  });
})();
