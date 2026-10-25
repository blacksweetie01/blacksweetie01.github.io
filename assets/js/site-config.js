/* 一般法理学 — 站点配置（集中管理第三方接入）
   部署前请在下方填入你的真实账号信息；未填写时相关功能会优雅降级为提示。 */
window.SITE_CONFIG = {
  siteName: '一般法理学',

  // —— 邮件订阅（Buttondown，免费、隐私友好）——
  // 1) 在 https://buttondown.email 注册并创建一个 newsletter
  // 2) 把你的用户名（即登录名 / 个性域名）填到下面
  buttondownUser: 'YOUR_BUTTONDOWN_USERNAME',

  // —— 评论（Giscus，基于 GitHub Discussions，无第三方追踪）——
  // 配置步骤：
  // 1) 仓库需为「公开」且开启 Discussions（Settings → Features → Discussions）
  // 2) 安装 Giscus App：https://github.com/apps/giscus
  // 3) 到 https://giscus.app 按指引生成下列 repoId / categoryId
  giscus: {
    repo: 'YOUR_GITHUB_USER/YOUR_REPO',
    repoId: 'YOUR_REPO_ID',
    category: 'Announcements',
    categoryId: 'YOUR_CATEGORY_ID',
    mapping: 'pathname',      // 以页面路径区分讨论串
    lang: 'zh-CN'
  }
};
