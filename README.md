# Suuyi’s Nook · 素衣的小站

面向 GitHub Pages 的个人介绍与项目展示网站。保留原站纸色、细线与昼夜主题，以独立页面提供明确层级。不需要安装 Node.js 或依赖。

## 页面结构

- 首页 `/`
- 关于 `/about/`
- 项目总览 `/projects/`
  - 研究实践 `/projects/research/`
  - 科学计算 `/projects/computation/`
  - 网页与工具 `/projects/web/`
    - 个人网站 `/projects/web/personal-site/`

“个人网站”是当前真实搭建的项目；其他两个分类为空，不代表已完成成果。

## 发布到 GitHub

1. 在 Suuyi-Nook 账号下创建公开仓库，名称为 `suuyi-nook.github.io`。
2. 上传本目录的文件和文件夹，确保 `index.html` 在仓库顶层。不要将 ZIP 直接上传作为网页。
3. 打开仓库 Settings → Pages，选择 Deploy from a branch，分支选 main，目录选 /(root)，保存。
4. 部署成功后地址为 https://suuyi-nook.github.io/ 。GitHub 首次发布可能需要数分钟。

GitHub 连接器的仓库权限与浏览器登录分别管理。如果连接器读不到新仓库，在 GitHub 的已安装应用设置中，把新仓库加入相应应用的可访问范围。

## 修改内容

日常只需要修改 `content.json` 中的介绍、分类和项目，再执行 `python build.py`。将生成后的 HTML 与修改过的文件一并提交，GitHub Pages 即可更新。也可以直接请 Codex 协助修改。

每个项目需要唯一的 slug、已有分类的 category、标题、摘要和 sections。生成器只依赖 Python 标准库。页面可以双击 index.html 预览，也可以执行 `python -m http.server 8765` 后打开 http://localhost:8765 。

主题保存在访问者自己的浏览器中。本站无登录、数据库、表单或跟踪脚本。不包含旧站私有配置、授权凭据和未公开研究材料。

## 来源与迁移边界

依据原站“素衣的学习、研究与生活记录”的页面结构与视觉方向制作静态公开版本。原站为 Vinext/React 项目；新版本仅承接个人介绍与项目展示，不依赖旧站的服务器运行环境。原站的访问权限和内容未修改。
