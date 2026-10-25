/* 一般法理学 — 站点配置
 *
 * repoId / categoryId 均已填入（取自本仓库 Discussions 分类的 node_id）。
 * 评论区已启用：基于 Giscus（GitHub Discussions），无第三方追踪。
 * 读者需登录 GitHub 账号方可评论；每条讨论按页面路径自动对应。
 *
 * 邮件订阅后端：Substack 与 Buttondown 二选一，留空其一即可。
 * 当前优先用 Substack（免费、订阅者无限）；在 Substack 未配置前，
 * 回退到 Buttondown 用户名（generaljurisprudence）保证「订阅」按钮可用。
 */
window.SITE_CONFIG = {
  subscribe: {
    /* 方案 A：Substack（推荐·免费·订阅者无限）
     * 到 https://substack.com 注册并新建一份出版物（publication），
     * 把你的出版物地址填到下面引号内，例如 "https://generaljurisprudence.substack.com"
     * ——「订阅」按钮即内嵌 Substack 订阅框，访客输入邮箱即可订阅。
     * 之后你在 Substack 发布更新（可一句话+原文链接），订阅者会收到邮件。 */
    substackUrl: "",

    /* 方案 B：Buttondown（免费 ≤100 订阅者；RSS 自动转发需 $9/月）
     * 已填入你的用户名，作为 Substack 未配置时的兜底。 */
    buttondownUser: "generaljurisprudence"
  },
  giscus: {
    repo: "blacksweetie01/blacksweetie01.github.io",
    repoId: "R_kgDOVWXpqQ",
    category: "General",
    categoryId: "DIC_kwDOVWXpqc4DJjaR",   // ← GitHub Discussions「General」分类 node_id
    mapping: "pathname",              // 每篇文章/页面按路径对应一条讨论
    lang: "zh-CN"
  }
};
