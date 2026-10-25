/* 一般法理学 — 站点配置（供 Giscus 评论区读取）
 *
 * repoId / categoryId 均已填入（取自本仓库 Discussions 分类的 node_id）。
 * 评论区已启用：基于 Giscus（GitHub Discussions），无第三方追踪。
 * 读者需登录 GitHub 账号方可评论；每条讨论按页面路径自动对应。
 */
window.SITE_CONFIG = {
  /* 邮件订阅（Buttondown，免费、隐私友好）
   * 到 https://buttondown.email 注册免费账号后，把你的 Buttondown 用户名
   * 填入下方引号内（如 "zhaoyingnan"），全站「订阅」按钮即自动生效。
   * 再在 Buttondown 后台把 RSS 源设为本站 https://blacksweetie01.github.io/feed.xml，
   * 订阅者即可定期自动收到网站更新邮件。
   */
  buttondownUser: "",
  giscus: {
    repo: "blacksweetie01/blacksweetie01.github.io",
    repoId: "R_kgDOVWXpqQ",
    category: "General",
    categoryId: "DIC_kwDOVWXpqc4DJjaR",   // ← GitHub Discussions「General」分类 node_id
    mapping: "pathname",              // 每篇文章/页面按路径对应一条讨论
    lang: "zh-CN"
  }
};
