/* 一般法理学 — 站点配置
 *
 * repoId / categoryId 均已填入（取自本仓库 Discussions 分类的 node_id）。
 * 评论区已启用：基于 Giscus（GitHub Discussions），无第三方追踪。
 * 读者需登录 GitHub 账号方可评论；每条讨论按页面路径自动对应。
 *
 * 邮件订阅后端：SendFox（免费 · 含 RSS 自动转发 · 上限 1,000 订阅者 · 无需信用卡）。
 * 到 https://sendfox.com 用邮箱注册（免费档即可）；进入 Growth → Forms 新建一个
 * 表单（Embedded form），复制嵌入代码里 <div ... id="数字"> 的「数字」填入下面引号内，
 * 例如 "123456"。填好后「订阅」按钮即内嵌 SendFox 表单，访客输入邮箱即可订阅。
 * 之后在 SendFox 后台 Growth → Smart Campaigns 把 RSS 源设为
 *   https://blacksweetie01.github.io/feed.xml
 * 网站每次更新，订阅者就会自动收到邮件。
 */
window.SITE_CONFIG = {
  subscribe: {
    sendfoxFormId: "YOUR_SENDFOX_FORM_ID"   // ← 在 SendFox 新建表单后，把表单 ID 填到这里（去掉 YOUR_ 前缀即生效）
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
