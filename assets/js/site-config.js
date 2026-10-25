/* 一般法理学 — 站点配置（供 Giscus 评论区读取）
 *
 * repoId / categoryId 均已填入（取自本仓库 Discussions 分类的 node_id）。
 * 评论区已启用：基于 Giscus（GitHub Discussions），无第三方追踪。
 * 读者需登录 GitHub 账号方可评论；每条讨论按页面路径自动对应。
 */
window.SITE_CONFIG = {
  giscus: {
    repo: "blacksweetie01/blacksweetie01.github.io",
    repoId: "R_kgDOVWXpqQ",
    category: "General",
    categoryId: "DIC_kwDOVWXpqc4DJjaR",   // ← GitHub Discussions「General」分类 node_id
    mapping: "pathname",              // 每篇文章/页面按路径对应一条讨论
    lang: "zh-CN"
  }
};
