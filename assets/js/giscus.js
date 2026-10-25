/* 一般法理学 — Giscus 评论加载（懒加载 + 未配置降级）
   在需要评论的页面放置 <div id="giscus-mount"></div> 并引入本脚本。 */
(function () {
  'use strict';
  var mount = document.getElementById('giscus-mount');
  if (!mount) return;

  var cfg = (window.SITE_CONFIG && window.SITE_CONFIG.giscus) || {};
  var notConfigured =
    !cfg.repoId || !cfg.categoryId ||
    String(cfg.repoId).indexOf('YOUR_') === 0 ||
    String(cfg.repo).indexOf('YOUR_') === 0;

  if (notConfigured) {
    mount.innerHTML =
      '<p class="muted" style="border:1px dashed var(--line);padding:1rem;border-radius:6px">' +
      '评论区即将启用：基于 Giscus（GitHub Discussions），无第三方追踪。' +
      '部署前请在 <code>assets/js/site-config.js</code> 中填入 Giscus 配置。</p>';
    return;
  }

  var s = document.createElement('script');
  s.src = 'https://giscus.app/client.js';
  s.async = true;
  s.crossOrigin = 'anonymous';
  s.setAttribute('data-repo', cfg.repo);
  s.setAttribute('data-repo-id', cfg.repoId);
  s.setAttribute('data-category', cfg.category);
  s.setAttribute('data-category-id', cfg.categoryId);
  s.setAttribute('data-mapping', cfg.mapping || 'pathname');
  s.setAttribute('data-reactions-enabled', '1');
  s.setAttribute('data-emit-metadata', '0');
  s.setAttribute('data-input-position', 'bottom');
  s.setAttribute('data-theme', 'preferred_color_scheme'); // 跟随站点明暗
  s.setAttribute('data-lang', cfg.lang || 'zh-CN');
  s.setAttribute('data-loading', 'lazy');
  mount.appendChild(s);
})();
