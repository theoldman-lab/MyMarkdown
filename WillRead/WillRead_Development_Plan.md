# WillRead 开发方案

## 一、开发总则

### 1.1 开发原则

| 原则 | 说明 |
|------|------|
| **迭代交付** | 每 2-3 周一个可演示的迭代版本，避免长时间开发不可用 |
| **插件优先** | 格式解析严格按插件接口开发，禁止硬编码格式逻辑 |
| **测试驱动** | 核心插件和 Rust 后端必须有单元测试，前端关键组件有集成测试 |
| **文档同步** | 每个功能完成时同步更新 README 和内部文档 |
| **跨平台验证** | 每个迭代必须在 Windows/macOS/Linux 三平台验证核心功能 |

### 1.2 开发环境要求

| 依赖 | 版本要求 | 用途 |
|------|----------|------|
| Rust | >= 1.75 | 后端开发 |
| Node.js | >= 20 LTS | 前端开发 |
| npm / pnpm | npm >= 10 或 pnpm >= 9 | 前端包管理 |
| Tauri CLI | >= 2.0 | Tauri 构建工具 |
| Git | >= 2.40 | 版本控制 |

**推荐 IDE：** VS Code + rust-analyzer + Tauri 插件 + ES6 插件

---

## 二、开发阶段详细规划

### Phase 1: 基础框架 (MVP)

**目标：** 跑通 Tauri 骨架，实现 PDF 基础查看功能

**预计迭代：** 2-3 次（约 4-6 周）

#### 1.1 项目初始化

| 任务 | 产出 |
|------|------|
| 初始化 Tauri v2 项目 | `willread/` 项目骨架 |
| 配置 Vite + React + TypeScript | 前端开发环境可用 |
| 配置 TailwindCSS | 基础样式系统 |
| 配置 Zustand | 状态管理就绪 |
| 编写 `.gitignore` / `.editorconfig` | 项目规范文件 |

#### 1.2 Rust 后端基础

| 任务 | 产出 |
|------|------|
| 定义 `FormatPlugin` Trait | `plugins/mod.rs` |
| 实现 `PluginRegistry` | `plugins/registry.rs` |
| 实现 Tauri Commands（`open_document`, `render_page`） | `commands/document.rs` |
| 配置 `Cargo.toml` 依赖 | 依赖锁定 |

#### 1.3 PDF 插件

| 任务 | 产出 |
|------|------|
| 集成 `pdfium-render` | PDF 解析能力 |
| 实现 `PdfPlugin` (Trait 实现) | `plugins/pdf.rs` |
| 实现 PDF 页渲染（Rust → Base64 PNG） | 前端可接收图片数据 |
| PDFium 二进制分发方案 | 构建脚本或 build.rs 下载 |

#### 1.4 前端阅读器

| 任务 | 产出 |
|------|------|
| 实现 `ReaderView` 组件 | 基本布局 |
| 实现 `PdfViewer` 组件 | PDF 页面渲染 |
| 实现翻页、缩放功能 | 基础交互 |
| 实现文件打开对话框 | 文件选择 |
| 实现键盘快捷键（← → + - Ctrl+O） | 快捷操作 |

#### 1.5 Phase 1 验收标准

- [ ] 能打开 PDF 文件并显示第一页
- [ ] 能翻页、放大/缩小
- [ ] 三平台（Win/macOS/Linux）编译通过并可运行
- [ ] 启动时间 < 3 秒

---

### Phase 2: 多格式支持

**目标：** 完善插件体系，支持 Markdown、EPUB、CBZ

**预计迭代：** 3-4 次（约 6-8 周）

#### 2.1 Markdown 插件

| 任务 | 产出 |
|------|------|
| 集成 `comrak` | Markdown 解析为 HTML |
| 实现 `MarkdownPlugin` | `plugins/markdown.rs` |
| 前端实现 `MarkdownViewer`（含 highlight.js） | 语法高亮渲染 |
| 支持 frontmatter 元数据解析 | 标题/作者提取 |
| 支持内部锚点跳转 | 长文档导航 |

#### 2.2 EPUB 插件

| 任务 | 产出 |
|------|------|
| 集成 `epub` crate | EPUB 结构解析 |
| 实现 OPF/NCX 解析 | 目录和阅读顺序 |
| 实现 `EpubPlugin` | `plugins/epub.rs` |
| 前端实现 `EpubViewer`（iframe 渲染） | EPUB 内容显示 |
| 实现章节预加载 | 性能优化 |

#### 2.3 CBZ 漫画插件

| 任务 | 产出 |
|------|------|
| 集成 `zip` + `image` crate | 图片解压 |
| 实现 `ComicPlugin` | `plugins/comic.rs` |
| 前端实现 `ComicViewer`（单页/双页/长滚动） | 三种查看模式 |
| 实现自然排序文件名 | 正确排序页码 |
| 实现前后预加载（前后各 2 页） | 流畅翻页 |

#### 2.4 书架功能（基础）

| 任务 | 产出 |
|------|------|
| 实现 `LibraryView` 组件 | 网格视图 |
| 实现文件扫描（递归目录） | 自动发现文档 |
| 实现封面提取（PDF 第一页/CBZ 第一图/EPUB 封面） | 封面显示 |
| 实现 JSON 持久化存储（书架数据） | 数据保存 |
| 实现排序/筛选（按格式） | 基本交互 |

#### 2.5 Phase 2 验收标准

- [ ] 可打开并渲染 Markdown/EPUB/CBZ 文件
- [ ] 书架能正确显示已添加的文档列表和封面
- [ ] 格式插件接口稳定，新增插件无需修改核心代码
- [ ] 渲染性能：PDF 翻页 < 500ms，漫画翻页 < 200ms

---

### Phase 3: 阅读体验

**目标：** 完善书签、目录、搜索、暗色模式等核心体验

**预计迭代：** 2-3 次（约 4-6 周）

#### 3.1 书签与阅读进度

| 任务 | 产出 |
|------|------|
| 设计 `BookmarkService` | `services/bookmark.rs` |
| 实现书签 CRUD（添加/查看/跳转/删除） | 完整功能 |
| 实现阅读进度自动保存 | 自动记录 |
| 实现「继续阅读」功能（自动跳转） | 体验优化 |
| 前端书签面板 UI | `BookmarkPanel.tsx` |

#### 3.2 目录导航

| 任务 | 产出 |
|------|------|
| 实现 `get_toc` 命令 | Tauri Command |
| 实现 EPUB/PDF 目录解析 | 多级目录支持 |
| 前端 `TocPanel` 组件 | 侧边栏目录 |
| 实现目录项点击跳转 | 快速导航 |

#### 3.3 全文搜索

| 任务 | 产出 |
|------|------|
| 实现 `extract_text` 命令 | 文本提取 |
| 实现简单全文搜索（PDF/EPUB） | 搜索功能 |
| 前端 `SearchPanel` 组件 | 搜索结果展示 |
| 搜索结果高亮 | 可视化 |

#### 3.4 暗色模式

| 任务 | 产出 |
|------|------|
| 实现主题状态管理 | `settingsStore.ts` |
| CSS 暗色模式变量体系 | `themes.css` |
| PDF 渲染反色（可选） | 夜间阅读体验 |
| Markdown/EPUB 暗色样式适配 | 样式适配 |

#### 3.5 Phase 3 验收标准

- [ ] 能添加书签并在书签间跳转
- [ ] 关闭文档后重新打开能自动恢复阅读进度
- [ ] PDF/EPUB 目录可显示并支持跳转
- [ ] 暗色模式切换流畅，无明显闪烁

---

### Phase 4: 增强功能

**目标：** 支持 MOBI/AZW3、CBR，完善高级功能

**预计迭代：** 3-4 次（约 6-8 周）

#### 4.1 MOBI/AZW3 支持

| 任务 | 产出 |
|------|------|
| 调研 Rust 生态 `mobi` crate | 可行性评估 |
| 实现 `MobiPlugin` | `plugins/mobi.rs` |
| 处理 DRM 情况（不支持/提示用户） | DRM 处理 |
| 前端适配 MOBI 渲染 | 复用 EpubViewer |

#### 4.2 CBR 支持

| 任务 | 产出 |
|------|------|
| 集成 `unrar` crate 或系统 unrar 命令 | RAR 解压 |
| 扩展 `ComicPlugin` 支持 CBR | CBR 查看 |
| 处理许可证问题（unrar 限制） | 法律合规 |

#### 4.3 键盘快捷键系统

| 任务 | 产出 |
|------|------|
| 实现快捷键配置系统 | JSON 配置 |
| 实现 `useKeyboard` Hook | 键盘事件处理 |
| 支持自定义快捷键映射 | 用户可定制 |
| 快捷键帮助面板（`?` 键） | 可发现性 |

#### 4.4 高级排版选项

| 任务 | 产出 |
|------|------|
| 实现字体/字号/行高设置 | 自定义设置 |
| 实现页面边距设置 | 排版控制 |
| 实现阅读方向支持（LTR/RTL/竖排） | 多语言排版 |
| Markdown/EPUB 排版选项持久化 | 配置保存 |

#### 4.5 打印支持

| 任务 | 产出 |
|------|------|
| 实现 PDF 打印命令 | Tauri Command |
| 前端打印对话框 | 打印 UI |
| 支持打印范围/份数设置 | 打印配置 |

#### 4.6 Phase 4 验收标准

- [ ] 能打开 MOBI/AZW3/CBR 文件
- [ ] 快捷键系统完整，可查看帮助
- [ ] 字体/排版设置生效
- [ ] PDF 打印功能正常

---

### Phase 5: 优化与发布

**目标：** 性能优化、国际化、安装包、自动化测试

**预计迭代：** 2-3 次（约 4-6 周）

#### 5.1 性能调优

| 任务 | 产出 |
|------|------|
| PDF 渲染性能分析（flamegraph） | 瓶颈定位 |
| 实现 LRU 页面缓存 | 缓存系统 |
| 实现 Web Worker 图片解码 | 主线程优化 |
| 实现虚拟滚动（长文档/漫画） | 渲染优化 |
| 内存泄漏检测与修复 | 稳定性 |

#### 5.2 国际化 (i18n)

| 任务 | 产出 |
|------|------|
| 集成 i18next（前端） | 国际化框架 |
| 提取所有 UI 文案为翻译文件 | 翻译资源 |
| 实现中文（简体/繁体）、英文、日文 | 多语言 |
| 实现语言自动检测 | 用户体验 |

#### 5.3 安装包打包

| 任务 | 产出 |
|------|------|
| 配置 Tauri bundle（MSI/DMG/DEB/RPM） | 安装包 |
| Windows: MSI + NSIS 可选 | Windows 安装 |
| macOS: DMG + 签名 | macOS 分发 |
| Linux: DEB + RPM + AppImage | Linux 分发 |
| 自动更新机制（Tauri updater） | 自动更新 |

#### 5.4 自动化测试

| 任务 | 产出 |
|------|------|
| Rust 单元测试（插件/服务） | `cargo test` |
| 前端组件测试（Vitest） | `npm test` |
| E2E 测试（Playwright） | 集成测试 |
| CI 流水线（GitHub Actions） | 自动化 |

#### 5.5 Phase 5 验收标准

- [ ] 三平台安装包可正常安装和卸载
- [ ] 自动化测试覆盖率 > 70%
- [ ] 启动时间 < 2 秒，内存 < 150MB
- [ ] 多语言切换正常

---

## 三、里程碑汇总

| 里程碑 | 内容 | 累计迭代 | 可交付成果 |
|--------|------|----------|------------|
| **M1** | Phase 1 完成 | 2-3 | PDF 查看器 MVP，三平台可运行 |
| **M2** | Phase 2 完成 | 5-7 | 多格式支持 + 基础书架 |
| **M3** | Phase 3 完成 | 7-10 | 书签/进度/目录/搜索/暗色 |
| **M4** | Phase 4 完成 | 10-14 | MOBI/AZW3/CBR + 高级功能 |
| **M5** | Phase 5 完成 | 12-17 | v1.0 发布版本 |

---

## 四、CI/CD 流水线

### 4.1 GitHub Actions 配置

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-rust:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test
        working-directory: src-tauri

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test

  build:
    needs: [test-rust, test-frontend]
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run tauri build
```

### 4.2 流水线阶段

| 阶段 | 触发条件 | 操作 |
|------|----------|------|
| **PR 检查** | 创建/更新 PR | 代码检查、单元测试、类型检查 |
| **Merge 构建** | PR 合并到 develop | 三平台构建、E2E 测试 |
| **Release 构建** | 打 Tag（v*） | 三平台安装包构建、签名、上传 |
| **Nightly** | 每日定时 | 集成测试、性能基准测试 |

### 4.3 代码质量门禁

| 检查项 | 要求 |
|--------|------|
| Rust `cargo clippy` | 0 warnings |
| Rust `cargo fmt` | 格式检查通过 |
| ESLint | 0 errors |
| TypeScript 类型检查 | 0 errors |
| 测试覆盖率 | Rust > 80%, Frontend > 60% |

---

## 五、测试策略

### 5.1 测试金字塔

```
         ╱  E2E 测试  ╲          ← 少量关键路径（10%）
        ╱──────────────╲
       ╱  集成测试        ╲        ← 组件交互（20%）
      ╱────────────────────╲
     ╱  单元测试              ╲      ← 核心逻辑（70%）
    ╱──────────────────────────╲
```

### 5.2 Rust 测试

```rust
// src-tauri/src/plugins/pdf.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pdf_plugin_creation() {
        let plugin = PdfPlugin::new();
        assert_eq!(plugin.format_name(), "pdf");
    }

    #[tokio::test]
    async fn test_pdf_page_count() {
        let plugin = PdfPlugin::new();
        let path = Path::new("test_assets/sample.pdf");
        let count = plugin.page_count(path).await.unwrap();
        assert_eq!(count, 5);  // sample.pdf has 5 pages
    }

    #[tokio::test]
    async fn test_pdf_render_page() {
        let plugin = PdfPlugin::new();
        let path = Path::new("test_assets/sample.pdf");
        let options = RenderOptions { dpi: 72.0, width: 800, height: 600, grayscale: false };
        let content = plugin.render_page(path, 0, &options).await.unwrap();
        assert_eq!(content.content_type, ContentType::ImagePng);
        assert!(!content.data.is_empty());
    }
}
```

### 5.3 前端测试

```typescript
// src/store/__tests__/readerStore.test.ts

import { describe, it, expect } from 'vitest';
import { useReaderStore } from '../readerStore';

describe('readerStore', () => {
  it('should initialize with null document', () => {
    const store = useReaderStore.getState();
    expect(store.currentDoc).toBeNull();
  });

  it('should update zoom', () => {
    useReaderStore.getState().setZoom(150);
    expect(useReaderStore.getState().currentDoc?.zoom).toBe(150);
  });
});
```

### 5.4 E2E 测试（Playwright）

```typescript
// tests/e2e/pdf-viewer.spec.ts

import { test, expect } from '@playwright/test';

test('can open and view PDF', async ({ page }) => {
  await page.goto('/');
  await page.click('[data-testid="open-file"]');
  // ... 模拟文件选择
  await expect(page.locator('img')).toBeVisible();
  await page.keyboard.press('ArrowRight');
  // ... 验证翻页
});
```

---

## 六、版本管理

### 6.1 分支策略（Git Flow）

```
main ────────────────────────────── v1.0 ───── v1.1
  ╲                                  ╱
develop ─── feat/pdf ──────────────╱
            feat/epub ────────────╱
            fix/render-bug ──────╱
```

| 分支 | 用途 | 保护规则 |
|------|------|----------|
| `main` | 发布版本，每个 commit 对应一个 release | 禁止直接 push，仅接受来自 release/* 的 merge |
| `develop` | 开发主分支 | 禁止直接 push，仅接受 PR |
| `feat/*` | 功能分支 | 完成后 PR 到 develop |
| `fix/*` | 修复分支 | 完成后 PR 到 develop 或 main（hotfix） |
| `release/*` | 发布准备分支 | 从 develop 拉出，测试后 merge 到 main + develop |

### 6.2 语义化版本 (SemVer)

```
主版本.次版本.修订版
  │      │      │
  │      │      └── 不兼容的 API 修改 → 增加主版本
  │      └───────── 向下兼容的功能 → 增加次版本
  └──────────────── 向下兼容的修复 → 增加修订版
```

| 版本 | 说明 | 示例 |
|------|------|------|
| `v0.1.0` | MVP（Phase 1） | PDF 查看 |
| `v0.2.0` | 多格式（Phase 2） | + Markdown/EPUB/CBZ |
| `v0.3.0` | 阅读体验（Phase 3） | + 书签/搜索/暗色 |
| `v0.4.0` | 增强功能（Phase 4） | + MOBI/CBR |
| `v1.0.0` | 正式发布（Phase 5） | 性能优化 + 安装包 |

### 6.3 Commit 规范（Conventional Commits）

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(pdf): add zoom and rotation support` |
| `fix` | 修复 | `fix(epub): fix chapter parsing error` |
| `docs` | 文档 | `docs: update design document` |
| `style` | 代码格式 | `style: run cargo fmt` |
| `refactor` | 重构 | `refactor(plugins): extract common render logic` |
| `test` | 测试 | `test(pdf): add unit tests for PdfPlugin` |
| `chore` | 构建/工具 | `chore: update dependencies` |

---

## 七、开发规范

### 7.1 Rust 代码规范

- 遵循 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- `cargo fmt` + `cargo clippy` 必须通过
- 错误处理统一使用 `Result<T, PluginError>`
- 异步函数使用 `async_trait`
- 公共 API 需文档注释

### 7.2 前端代码规范

- TypeScript strict mode
- ESLint + Prettier
- 组件使用函数式 + Hooks
- 状态管理使用 Zustand，禁止组件内 useReducer 管理跨组件状态
- CSS 使用 Tailwind，禁止内联 style（除动态计算外）

### 7.3 文件命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| Rust 模块 | snake_case | `plugin_registry.rs` |
| React 组件 | PascalCase | `PdfViewer.tsx` |
| Hooks | camelCase + use 前缀 | `useDocument.ts` |
| Store 文件 | camelCase + Store 后缀 | `readerStore.ts` |
| 测试文件 | 同名 + `.test` | `pdf.test.ts` |

---

## 八、风险管理

### 8.1 技术风险

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| PDFium 二进制分发失败 | 中 | 高 | 备选 mupdf-sys，build.rs 自动下载 |
| MOBI 解析库不成熟 | 高 | 中 | Phase 4 延后或用 Python Calibre 子进程 |
| Tauri v2 API 不稳定 | 低 | 中 | 锁定版本，关注 Tauri 更新日志 |
| 跨平台 WebView 差异 | 中 | 中 | 提前做 POC，避免使用最新 Web API |

### 8.2 项目风险

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 范围蔓延 | 高 | 高 | 严格遵循 Phase 计划，新需求放入 backlog |
| 性能不达标 | 中 | 高 | 每阶段做性能基准，早期发现问题 |
| 测试不足导致回归 | 中 | 中 | CI 门禁，PR 必须有测试 |

---

## 九、文档计划

### 9.1 开发期文档

| 文档 | 位置 | 更新时机 |
|------|------|----------|
| `DESIGN.md` | 项目根目录 | 架构变更时 |
| `DEVELOPMENT.md` | 项目根目录 | 开发环境/规范变更 |
| `CHANGELOG.md` | 项目根目录 | 每次 release |
| API 文档 | `src-tauri/docs/` | Tauri Commands 变更 |
| 插件开发指南 | `docs/plugin-guide.md` | 插件接口变更 |

### 9.2 用户文档（Phase 5）

| 文档 | 内容 |
|------|------|
| `README.md` | 简介、安装、快速开始 |
| 用户手册 | 各格式使用说明、快捷键、设置 |
| FAQ | 常见问题（字体、DRM、性能） |

---

## 十、发布计划

### 10.1 发布渠道

| 渠道 | 阶段 | 说明 |
|------|------|------|
| GitHub Releases | M1 起 | 每个里程碑发布二进制 |
| Homebrew (macOS) | M5 | `brew install willread` |
| AUR (Arch Linux) | M5 | AUR package |
| Microsoft Store | v1.0 后 | Windows 分发 |

### 10.2 v1.0 发布检查清单

- [ ] 所有 Phase 1-5 功能完成
- [ ] 三平台测试通过率 > 95%
- [ ] 性能基准达标（启动 < 2s，内存 < 150MB）
- [ ] 安全审计通过（无已知漏洞）
- [ ] 用户文档完整
- [ ] 安装包签名完成
- [ ] 自动更新机制验证通过

---

*WillRead 开发方案 v1.0 — 一个应用，阅读万物。*
