/* 一般法理学 — 站点配置（供 Giscus 评论区读取）
 *
 * repoId 已填入（取自本仓库的 node_id）。
 * categoryId 需要仓库先「开启 Discussions」并「安装 Giscus App」后，
 * 由维护者用 GitHub GraphQL 取得讨论分类的 node_id 填入此处（见维护说明）。
 * 在 categoryId 填充之前，评论区会显示「即将启用」占位提示，不会报错。
 */
window.SITE_CONFIG = {
  giscus: {
    repo: "blacksweetie01/blacksweetie01.github.io",
    repoId: "R_kgDOVWXpqQ",
    category: "Announcements",
    categoryId: "YOUR_CATEGORY_ID",   // ← 开启 Discussions + 安装 Giscus 后填入
    mapping: "pathname",              // 每篇文章/页面按路径对应一条讨论
    lang: "zh-CN"
  }
};
