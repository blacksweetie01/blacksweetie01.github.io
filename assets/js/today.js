/* 主页「今日」：展示今天的公历日期，hover / 点击日期显示农历与黄历宜忌。
 * 农历与黄历由本地 assets/js/lunar.js（lunar-javascript）计算，无任何外部网络依赖。
 */
(function () {
  function byId(id) { return document.getElementById(id); }
  function set(el, t) { if (el) el.textContent = t; }
  function arr(v) { return Array.isArray(v) ? v.join('、') : (v == null ? '' : ('' + v)); }
  function safe(fn, d) { try { var r = fn(); return r == null ? d : r; } catch (e) { return d; } }

  function getLunar(date) {
    try {
      var S = window.Solar || (window.Lunar && window.Lunar.Solar);
      if (S && S.fromDate) return S.fromDate(date).getLunar();
      if (window.Lunar && window.Lunar.fromDate) return window.Lunar.fromDate(date);
    } catch (e) {}
    return null;
  }

  function renderDate() {
    var now = new Date();
    var ys = ['日', '一', '二', '三', '四', '五', '六'];
    set(byId('today-year'), now.getFullYear() + ' 年');
    set(byId('today-md'), (now.getMonth() + 1) + ' 月 ' + now.getDate() + ' 日');
    set(byId('today-week'), '星期' + ys[now.getDay()]);
    bind();
  }

  function row(k, v, cls) {
    return '<div class="pop-r' + (cls ? (' pop-' + cls) : '') + '"><span class="pop-k">' + k +
      '</span><span class="pop-v">' + v + '</span></div>';
  }

  function fillLunar() {
    var lunar = getLunar(new Date());
    var lEl = byId('today-lunar'), pop = byId('today-pop');
    if (!lunar) { if (lEl) lEl.textContent = '农历（加载失败）'; return; }

    var yGZ = safe(function () { return lunar.getYearInGanZhi(); }, '');
    var sx = safe(function () { return lunar.getYearShengXiao(); }, '');
    var mCn = safe(function () { return lunar.getMonthInChinese(); }, '');
    var dCn = safe(function () { return lunar.getDayInChinese(); }, '');
    var dGZ = safe(function () { return lunar.getDayInGanZhi(); }, '');

    var solar = safe(function () {
      var S = window.Solar || (window.Lunar && window.Lunar.Solar);
      return S.fromDate(new Date());
    }, null);
    var xz = solar ? safe(function () { return solar.getXingZuo(); }, '') : '';

    var yi = arr(safe(function () { return lunar.getDayYi(); }, []));
    var ji = arr(safe(function () { return lunar.getDayJi(); }, []));
    var chongSX = safe(function () { return lunar.getDayChongShengXiao(); }, '');
    var sha = safe(function () { return lunar.getDaySha(); }, '');
    var chong = (chongSX || sha) ? ('冲' + chongSX + '煞' + sha) : '';
    var jishen = arr(safe(function () { return lunar.getDayJiShen(); }, []));
    var xiongsha = arr(safe(function () { return lunar.getDayXiongSha(); }, []));
    var pzParts = [safe(function () { return lunar.getPengZuGan(); }, ''),
                   safe(function () { return lunar.getPengZuZhi(); }, '')].filter(Boolean);
    var pzText = pzParts.join('；');
    var tianshen = safe(function () { return lunar.getDayTianShen(); }, '');
    var tsType = safe(function () { return lunar.getDayTianShenType(); }, '');
    var cai = safe(function () { return lunar.getDayPositionCaiDesc(); }, '');
    var yin = safe(function () { return lunar.getDayPositionYinGuiDesc(); }, '');

    if (lEl) lEl.textContent = '农历 ' + yGZ + '（' + sx + '）年 ' + mCn + '月' + dCn;

    var rows = [];
    rows.push(row('干支', yGZ + '年 ' + mCn + '月' + dCn + ' · 日柱 ' + dGZ));
    if (xz) rows.push(row('星座', xz));
    if (yi) rows.push(row('宜', yi, 'good'));
    if (ji) rows.push(row('忌', ji, 'bad'));
    if (tianshen) rows.push(row('值神', tianshen + (tsType ? ('（' + tsType + '）') : '')));
    if (chong) rows.push(row('冲煞', chong));
    if (jishen) rows.push(row('吉神', jishen));
    if (xiongsha) rows.push(row('凶神', xiongsha));
    if (pzText) rows.push(row('彭祖', pzText));
    if (cai || yin) rows.push(row('方位', (cai ? ('财神' + cai) : '') + (yin ? (' · 阴贵' + yin) : '')));

    if (pop) {
      pop.innerHTML = '<div class="pop-h">' + yGZ + '（' + sx + '）年 · ' + mCn + '月' + dCn + '</div>' +
        rows.join('') +
        '<div class="pop-foot">将鼠标移开或点击空白处收起 · 农历库推算，仅供参考</div>';
    }
  }

  function bind() {
    var card = byId('today-card'), trigger = byId('today-trigger'), pop = byId('today-pop');
    if (!card || !trigger || !pop) return;
    function open() { card.classList.add('open'); pop.setAttribute('aria-hidden', 'false'); }
    function close() { if (card.classList.contains('pinned')) return; card.classList.remove('open'); pop.setAttribute('aria-hidden', 'true'); }
    function unpin() { card.classList.remove('pinned', 'open'); pop.setAttribute('aria-hidden', 'true'); }
    trigger.addEventListener('mouseenter', open);
    trigger.addEventListener('mouseleave', close);
    trigger.addEventListener('focus', open);
    trigger.addEventListener('blur', close);
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      if (card.classList.contains('pinned')) unpin();
      else { card.classList.add('pinned'); open(); }
    });
    document.addEventListener('click', function () { if (card.classList.contains('pinned')) unpin(); });
  }

  function init() { renderDate(); fillLunar(); }

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);

  /* 容错：若 lunar.js 尚未就绪，稍后重试最多约 5 秒 */
  var tries = 0;
  var timer = setInterval(function () {
    if (typeof (window.Lunar || window.Solar) !== 'undefined') {
      clearInterval(timer);
      if (byId('today-pop')) fillLunar();
    } else if (++tries > 40) {
      clearInterval(timer);
    }
  }, 120);
})();
