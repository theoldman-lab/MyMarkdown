# WillRead 开发环境与开发方法指导

本文档面向 WillRead 项目的新加入开发者，包含完整的环境配置指南、开发工作流说明和开发方法指导。

---

## 一、开发环境需求

### 1.1 硬件需求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 4 核心 | 8 核心+ |
| 内存 | 8 GB | 16 GB+ |
| 硬盘 | 20 GB 可用空间 | SSD 50 GB+ |
| 网络 | 稳定连接（下载依赖） | — |

### 1.2 操作系统支持

| 系统 | 版本 | 架构 |
|------|------|------|
| Windows | 10 / 11 | x86_64, ARM64 |
| macOS | 12+ (Monterey) | Apple Silicon (arm64) / Intel (x86_64) |
| Linux | Ubuntu 20.04+ / Fedora 36+ / Arch | x86_64, ARM64 |

---

## 二、开发环境配置

### 2.1 依赖清单

| 软件 | 版本 | 用途 | 官网 |
|------|------|------|------|
| **Rust** | >= 1.75 (stable) | 后端开发 | https://rustup.rs |
| **Node.js** | >= 20 LTS | 前端开发 | https://nodejs.org |
| **pnpm** (推荐) 或 npm | pnpm >= 9 / npm >= 10 | 前端包管理 | https://pnpm.io |
| **Tauri CLI** | >= 2.0 | Tauri 构建工具 | 通过 `cargo install` 安装 |
| **Git** | >= 2.40 | 版本控制 | https://git-scm.com |

### 2.2 各平台安装步骤

#### Windows

```powershell
# 1. 安装 Visual Studio Build Tools
# 下载地址：https://visualstudio.microsoft.com/visual-cpp-build-tools/
# 安装时勾选 "Desktop development with C++"
# 确保勾选 "MSVC v143 build tools" 和 "Windows 10/11 SDK"

# 2. 安装 Rust
winget install Rustlang.Rustup
# 或访问 https://rustup.rs 下载 rustup-init.exe

# 3. 安装 Node.js
winget install OpenJS.NodeJS.LTS

# 4. 安装 pnpm
npm install -g pnpm

# 5. 安装 WebView2（Windows 10 1809+ 通常已自带）
# 如果没有，从 https://developer.microsoft.com/microsoft-edge/webview2/ 下载
```

#### macOS

```bash
# 1. 安装 Xcode Command Line Tools
xcode-select --install

# 2. 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 3. 安装 Node.js (推荐用 Homebrew)
brew install node

# 4. 安装 pnpm
brew install pnpm
```

#### Linux (Ubuntu/Debian)

```bash
# 1. 安装系统依赖
sudo apt update
sudo apt install -y \
  build-essential \
  curl \
  wget \
  file \
  libssl-dev \
  libgtk-3-dev \
  libwebkit2gtk-4.1-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev \
  libxdo-dev \
  libfuse2 \
  patchelf

# 2. 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 3. 安装 Node.js (使用 NodeSource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 4. 安装 pnpm
sudo npm install -g pnpm
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install -y \
  gcc gcc-c++ make \
  curl wget \
  openssl-devel \
  gtk3-devel \
  webkit2gtk4.1-devel \
  libappindicator-gtk3-devel \
  librsvg2-devel \
  libXdo-devel

# Rust, Node.js, pnpm 安装同上
```

#### Linux (Arch)

```bash
sudo pacman -S --needed \
  base-devel \
  curl wget \
  webkit2gtk-4.1 \
  gtk3 \
  libappindicator-gtk3 \
  librsvg \
  xdotool

# Rust, Node.js, pnpm 安装同上
```

### 2.3 项目初始化

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/willread.git
cd willread

# 2. 安装 Rust 工具链（如果尚未安装）
rustup default stable
rustup update

# 3. 安装 Tauri CLI
cargo install tauri-cli --version "^2.0"

# 4. 安装前端依赖
pnpm install

# 5. 安装 Rust 依赖（预编译，加速首次构建）
cd src-tauri && cargo fetch && cd ..

# 6. 验证环境
cargo tauri info
```

### 2.4 推荐 IDE 配置

#### VS Code (推荐)

安装以下扩展：

| 扩展名 | ID | 用途 |
|--------|-----|------|
| **rust-analyzer** | `rust-lang.rust-analyzer` | Rust 语言服务器 |
| **Even Better TOML** | `tamasfe.even-better-toml` | Cargo.toml 编辑 |
| **crates** | `serayuzgur.crates` | 依赖版本提示更新 |
| **ES7+ React/Redux Snippets** | `dsznajder.es7-react-js-snippets` | React 代码片段 |
| **Tailwind CSS IntelliSense** | `bradlc.vscode-tailwindcss` | Tailwind 自动补全 |
| **Pretty TypeScript Errors** | `ms-vscode.vscode-typescript-next` | 更好的 TS 错误提示 |
| **GitLens** | `eamodio.gitlens` | Git 增强 |

#### 推荐工作区配置 (`.vscode/settings.json`)

```json
{
  "rust-analyzer.cargo.features": "all",
  "rust-analyzer.checkOnSave.command": "clippy",
  "rust-analyzer.procMacro.enable": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[rust]": {
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  },
  "tailwindCSS.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  }
}
```

---

## 三、开发工作流

### 3.1 日常开发

```bash
# 启动开发模式（前端热重载 + Tauri 热重载）
pnpm tauri dev

# 仅启动前端开发服务器（更快，但不包含 Rust 后端）
pnpm dev

# 编译检查（前端）
pnpm type-check

# 编译检查（Rust）
cd src-tauri && cargo check

# 运行所有测试
pnpm test

# 仅运行 Rust 测试
cd src-tauri && cargo test

# 代码检查
pnpm lint

# 格式化代码
pnpm format
```

### 3.2 构建与打包

```bash
# 开发构建
pnpm tauri build --debug

# 生产构建
pnpm tauri build

# 指定平台构建（Linux）
pnpm tauri build --bundles deb rpm appimage

# 指定平台构建（macOS）
pnpm tauri build --bundles dmg

# 指定平台构建（Windows）
pnpm tauri build --bundles msi
```

### 3.3 开发命令速查表

| 命令 | 说明 |
|------|------|
| `pnpm tauri dev` | 开发模式（前端 + 后端热重载） |
| `pnpm tauri build` | 生产构建 |
| `pnpm tauri info` | 查看 Tauri 环境信息 |
| `pnpm tauri plugin add <plugin>` | 添加 Tauri 插件 |
| `cargo clippy -- -D warnings` | Rust 代码检查 |
| `cargo fmt` | Rust 代码格式化 |
| `cargo test` | 运行 Rust 测试 |

---

## 四、开发方法指导

### 4.1 开发流程（功能开发完整步骤）

以「添加新格式插件」为例，演示完整的开发流程：

#### 步骤 1: 创建功能分支

```bash
git checkout develop
git pull origin develop
git checkout -b feat/epub-support
```

#### 步骤 2: 定义插件接口（如尚未存在）

在 `src-tauri/src/plugins/mod.rs` 中确保 `FormatPlugin` Trait 已定义。

#### 步骤 3: 实现插件

```rust
// src-tauri/src/plugins/epub.rs

use crate::plugins::{FormatPlugin, PluginError, RenderedContent, RenderOptions, ContentType};
use std::path::Path;

pub struct EpubPlugin;

#[async_trait::async_trait]
impl FormatPlugin for EpubPlugin {
    fn format_name(&self) -> &str {
        "epub"
    }

    fn supported_extensions(&self) -> &[&str] {
        &[".epub"]
    }

    // 实现其他必需方法...
}
```

#### 步骤 4: 注册插件

```rust
// src-tauri/src/main.rs

use plugins::{PluginRegistry, EpubPlugin};

fn setup_plugin_registry() -> PluginRegistry {
    let mut registry = PluginRegistry::new();
    registry.register(Box::new(EpubPlugin));
    // ... 注册其他插件
    registry
}
```

#### 步骤 5: 实现前端查看器

```tsx
// src/components/Reader/EpubViewer.tsx

import React from 'react';

interface EpubViewerProps {
  content: string | null;
  // ...
}

export const EpubViewer: React.FC<EpubViewerProps> = ({ content }) => {
  return (
    <div className="epub-viewer prose">
      <div dangerouslySetInnerHTML={{ __html: content || '' }} />
    </div>
  );
};
```

#### 步骤 6: 编写测试

```rust
// src-tauri/src/plugins/epub.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_epub_extensions() {
        let plugin = EpubPlugin;
        assert!(plugin.supported_extensions().contains(&".epub"));
    }
}
```

#### 步骤 7: 自测验证

```bash
# 运行测试
cargo test

# 启动开发模式手动测试
pnpm tauri dev
```

#### 步骤 8: 提交并推送

```bash
git add .
git commit -m "feat(epub): implement EPUB format plugin and viewer"
git push origin feat/epub-support
```

#### 步骤 9: 创建 Pull Request

- 在 GitHub 上创建 PR，目标分支为 `develop`
- 填写 PR 描述，关联相关 Issue
- 等待 CI 检查通过
- Code Review 通过后合并

### 4.2 代码组织原则

#### Rust 模块组织

```
src-tauri/src/
├── main.rs              # 入口，最小化逻辑
├── lib.rs               # 核心逻辑导出
├── plugins/             # 格式插件
│   ├── mod.rs           # Trait 定义
│   ├── registry.rs      # 注册与路由
│   ├── pdf.rs           # PDF 实现
│   ├── markdown.rs      # Markdown 实现
│   └── ...
├── services/            # 核心服务
│   ├── mod.rs
│   ├── cache.rs         # 缓存
│   ├── bookmark.rs      # 书签
│   └── config.rs        # 配置
└── commands/            # Tauri Commands
    ├── mod.rs
    ├── document.rs      # 文档操作
    ├── reader.rs        # 阅读器控制
    └── settings.rs      # 设置
```

**规则：**
- 每个模块只暴露最小公共 API
- Trait 定义放在 `mod.rs` 中
- 具体实现放在独立文件中
- 服务间通过接口交互，避免循环依赖

#### 前端组件组织

```
src/
├── components/          # UI 组件
│   ├── Reader/          # 阅读器相关
│   ├── Library/         # 书架相关
│   ├── Sidebar/         # 侧边栏
│   ├── Toolbar/         # 工具栏
│   └── Settings/        # 设置
├── store/               # Zustand 状态管理
├── hooks/               # 自定义 Hooks
├── utils/               # 工具函数
└── styles/              # 全局样式
```

**规则：**
- 组件文件使用 PascalCase 命名
- 每个组件文件只导出一个主组件
- 相关子组件放在同名目录中
- 状态逻辑抽离到 store 目录
- 工具函数抽离到 utils 目录

### 4.3 状态管理规范

#### Zustand 使用指南

```typescript
// src/store/readerStore.ts

import { create } from 'zustand';

// 1. 定义状态接口
interface ReaderState {
  // 数据
  currentDoc: Document | null;
  content: string | null;
  isLoading: boolean;

  // 操作
  openDocument: (path: string) => Promise<void>;
  closeDocument: () => void;
  setZoom: (zoom: number) => void;
}

// 2. 创建 store
export const useReaderStore = create<ReaderState>((set, get) => ({
  // 初始状态
  currentDoc: null,
  content: null,
  isLoading: false,

  // 操作实现
  openDocument: async (path: string) => {
    set({ isLoading: true });
    try {
      // 调用 Tauri Command
      const result = await invoke('open_document', { path });
      set({ currentDoc: result, isLoading: false });
    } catch (error) {
      set({ isLoading: false, error: String(error) });
    }
  },

  closeDocument: () => {
    set({ currentDoc: null, content: null });
  },

  setZoom: (zoom: number) => {
    set((state) => ({
      currentDoc: state.currentDoc ? { ...state.currentDoc, zoom } : null,
    }));
  },
}));

// 3. 在组件中使用
// const { currentDoc, openDocument } = useReaderStore();
```

**规则：**
- 一个 store 管理一个业务域的状态
- 避免一个 store 管理跨域状态
- 操作实现中使用 `get()` 获取当前状态
- 复杂逻辑抽离到 actions 中

### 4.4 Tauri Command 编写指南

```rust
// src-tauri/src/commands/document.rs

use tauri::State;
use crate::plugins::registry::PluginRegistry;
use crate::plugins::*;

/// 打开文档
/// 
/// # 参数
/// * `path` - 文件绝对路径
/// * `registry` - 插件注册器（通过 Tauri State 注入）
/// 
/// # 返回
/// * `Ok(DocumentMetadata)` - 文档元数据
/// * `Err(String)` - 错误信息
#[tauri::command]
pub async fn open_document(
    path: String,
    registry: State<'_, PluginRegistry>,
) -> Result<DocumentMetadata, String> {
    let path = std::path::Path::new(&path);

    // 1. 获取对应插件
    let plugin = registry
        .get_plugin_for_file(path)
        .ok_or("Unsupported file format")?;

    // 2. 检测格式
    plugin.detect_format(path).await
        .map_err(|e| format!("Format detection failed: {}", e))?;

    // 3. 获取元数据
    plugin.get_metadata(path).await
        .map_err(|e| format!("Metadata extraction failed: {}", e))
}
```

**规则：**
- 每个 Command 是一个 `async fn`
- 返回类型统一为 `Result<T, String>`
- 错误信息使用 `format!` 包装，避免暴露内部细节
- 通过 `State` 注入共享资源（如插件注册器）
- Command 中不做复杂计算，委托给 Service 层

### 4.5 插件开发指南

#### 实现新格式插件的步骤

1. **在 `plugins/` 下创建新文件**

```rust
// src-tauri/src/plugins/new_format.rs

use crate::plugins::{FormatPlugin, PluginError, RenderedContent, RenderOptions, ContentType};
use std::path::Path;

pub struct NewFormatPlugin;

#[async_trait::async_trait]
impl FormatPlugin for NewFormatPlugin {
    fn format_name(&self) -> &str {
        "new_format"
    }

    fn supported_extensions(&self) -> &[&str] {
        &[".ext1", ".ext2"]
    }

    async fn detect_format(&self, path: &Path) -> Result<bool, PluginError> {
        // 实现格式检测逻辑
        Ok(true)
    }

    async fn get_metadata(&self, path: &Path) -> Result<DocumentMetadata, PluginError> {
        // 实现元数据提取
        todo!()
    }

    async fn render_page(
        &self,
        path: &Path,
        page: usize,
        options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError> {
        // 实现页面渲染
        todo!()
    }

    async fn page_count(&self, path: &Path) -> Result<usize, PluginError> {
        // 返回总页数
        todo!()
    }

    async fn extract_text(&self, path: &Path) -> Result<String, PluginError> {
        // 提取文本
        todo!()
    }

    async fn get_toc(&self, path: &Path) -> Result<Vec<TocEntry>, PluginError> {
        // 获取目录
        todo!()
    }
}
```

2. **在 `Cargo.toml` 中添加依赖**

```toml
[dependencies]
# 添加新格式所需的 Rust crate
new-format-crate = "1.0"
```

3. **在 `plugins/mod.rs` 中导出**

```rust
mod new_format;
pub use new_format::NewFormatPlugin;
```

4. **在 `main.rs` 中注册**

```rust
registry.register(Box::new(NewFormatPlugin));
```

5. **实现前端查看器组件**

```tsx
// src/components/Reader/NewFormatViewer.tsx

import React from 'react';

export const NewFormatViewer = ({ content }: { content: string | null }) => {
  return (
    <div>
      {/* 渲染 content */}
    </div>
  );
};
```

6. **在 `ReaderView.tsx` 中添加路由**

```tsx
switch (currentDoc.format) {
  case 'new_format':
    return <NewFormatViewer content={content} document={currentDoc} />;
  // ...
}
```

---

## 五、代码规范

### 5.1 Rust 代码规范

| 规则 | 说明 | 检查工具 |
|------|------|----------|
| `cargo fmt` | 统一代码格式 | rustfmt |
| `cargo clippy -- -D warnings` | 代码质量检查 | clippy |
| 错误处理 | 使用 `Result<T, E>` 而非 `unwrap()` | clippy |
| 命名 | 函数/变量 snake_case，类型 PascalCase | clippy |
| 文档 | 公共 API 需 `///` 注释 | rustdoc |
| 可见性 | 最小化 `pub` 范围 | clippy |

**示例：**

```rust
/// 文档元数据
/// 
/// 包含文档的基本信息，由 `FormatPlugin::get_metadata` 返回。
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct DocumentMetadata {
    /// 文档标题
    pub title: Option<String>,
    /// 作者
    pub author: Option<String>,
    /// 总页数
    pub page_count: usize,
}
```

### 5.2 TypeScript/React 代码规范

| 规则 | 说明 | 检查工具 |
|------|------|----------|
| ESLint | 遵循项目 `.eslintrc` 配置 | eslint |
| Prettier | 统一代码格式 | prettier |
| TypeScript strict mode | 禁止 `any`（除非必要） | tsc |
| 组件 | 使用函数式组件 + Hooks | eslint |
| 命名 | 组件 PascalCase，变量/函数 camelCase | eslint |
| Props | 使用 interface 定义 Props 类型 | tsc |

**示例：**

```tsx
import React from 'react';

/** 文档元数据接口 */
export interface DocumentMetadata {
  /** 文档标题 */
  title: string;
  /** 作者 */
  author?: string;
  /** 总页数 */
  pageCount: number;
}

/** 文档信息卡片组件 */
interface DocCardProps {
  metadata: DocumentMetadata;
  onRead: () => void;
}

export const DocCard: React.FC<DocCardProps> = ({ metadata, onRead }) => {
  return (
    <div className="rounded-lg shadow p-4 bg-white dark:bg-gray-800">
      <h3 className="text-lg font-semibold">{metadata.title}</h3>
      {metadata.author && (
        <p className="text-sm text-gray-500">{metadata.author}</p>
      )}
      <button
        onClick={onRead}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        阅读
      </button>
    </div>
  );
};
```

### 5.3 提交信息规范

采用 Conventional Commits 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Type 列表：**

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(pdf): add rotation support` |
| `fix` | Bug 修复 | `fix(epub): fix chapter parsing error` |
| `docs` | 文档 | `docs: add development guide` |
| `style` | 代码格式 | `style: run cargo fmt on all files` |
| `refactor` | 重构 | `refactor(plugins): extract common render logic` |
| `perf` | 性能优化 | `perf(pdf): implement page preloading` |
| `test` | 测试 | `test(pdf): add unit tests for PdfPlugin` |
| `chore` | 构建/工具 | `chore: update dependencies` |

---

## 六、调试指南

### 6.1 前端调试

```bash
# 开发模式下打开 DevTools
# Tauri 窗口右键 → "Inspect Element"
```

**常用调试技巧：**
- 使用 `console.log` 输出状态变化
- 使用 React DevTools 查看组件树和 Props
- 使用 Network 面板查看 IPC 通信

### 6.2 Rust 后端调试

```rust
// 使用 log crate 输出日志
use log::{info, warn, error, debug};

#[tauri::command]
pub async fn open_document(path: String) -> Result<DocumentMetadata, String> {
    info!("Opening document: {}", path);
    debug!("Loading file from: {:?}", path);
    // ...
}
```

**查看日志：**
```bash
# 开发模式日志会输出到终端
pnpm tauri dev 2>&1 | grep -E "INFO|WARN|ERROR"

# 生产模式日志位置
# Linux: ~/.local/share/willread/logs/
# macOS: ~/Library/Logs/willread/
# Windows: %APPDATA%\willread\logs\
```

### 6.3 常见问题排查

| 问题 | 排查方法 |
|------|----------|
| 前端白屏 | 检查 DevTools Console 是否有 JS 错误 |
| Rust 编译失败 | `cargo clean && cargo build` |
| Tauri 启动失败 | `pnpm tauri info` 检查环境 |
| 文件打不开 | 检查路径是否为绝对路径，文件是否存在 |
| PDF 渲染失败 | 检查 PDFium 是否正确加载 |
| 内存泄漏 | 使用 `cargo flamegraph` 分析 |

---

## 七、协作流程

### 7.1 Git 分支管理

```
main ──────────────────────────────────────── v1.0
  ╲
develop ──────────────────────────────────────
  ╲       ╱            ╲
feat/pdf ────────────────╲
                           ╲
feat/epub ──────────────────╲
                              ╲
fix/render-bug ───────────────╱
```

**分支规则：**

| 分支 | 用途 | 保护 |
|------|------|------|
| `main` | 发布版本 | 禁止直接推送，仅接受 release PR |
| `develop` | 开发主分支 | 禁止直接推送，仅接受 PR |
| `feat/*` | 功能开发 | 完成后 PR 到 develop |
| `fix/*` | Bug 修复 | 完成后 PR 到 develop |
| `hotfix/*` | 紧急修复 | 完成后 PR 到 main + develop |
| `release/*` | 发布准备 | 从 develop 拉出，测试后合并到 main + develop |

### 7.2 Pull Request 流程

1. **从 develop 创建功能分支**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feat/my-feature
   ```

2. **开发并提交**
   ```bash
   # 开发...
   git add .
   git commit -m "feat(scope): add new feature"
   ```

3. **推送并创建 PR**
   ```bash
   git push origin feat/my-feature
   # 在 GitHub 上创建 PR，目标分支 develop
   ```

4. **PR 要求**
   - 填写 PR 描述
   - 关联相关 Issue
   - CI 检查全部通过
   - 至少 1 人 Code Review

5. **合并后删除分支**

### 7.3 Code Review 清单

| 检查项 | 说明 |
|--------|------|
| 功能正确性 | 是否满足需求 |
| 代码质量 | 是否遵循规范 |
| 性能 | 是否有明显性能问题 |
| 测试 | 是否有充分测试 |
| 文档 | 是否更新了文档 |
| 安全 | 是否有安全隐患 |

---

## 八、故障排除

### 8.1 常见错误

#### Rust 编译错误

```
error: could not compile `willread` due to previous error
```

**解决：**
```bash
cargo clean
cargo build
```

#### Tauri 启动失败

```
error: failed to run tauri
```

**解决：**
```bash
pnpm tauri info  # 检查环境
# 确认系统依赖已安装（WebView2、gtk、webkit2gtk 等）
```

#### 前端热重载不生效

**解决：**
```bash
# 检查 vite.config.ts 中的 hmr 配置
# 确保没有多个进程监听同一端口
```

### 8.2 性能调试

```bash
# Rust 性能分析
cargo install flamegraph
sudo cargo flamegraph --bin willread

# 内存分析
cargo install cargo-machete  # 检查未使用依赖
cargo bloat  # 分析二进制大小
```

---

## 九、附录

### 9.1 关键依赖文档链接

| 依赖 | 文档 |
|------|------|
| Tauri v2 | https://v2.tauri.app |
| Rust | https://doc.rust-lang.org/book/ |
| pdfium-render | https://docs.rs/pdfium-render |
| comrak | https://docs.rs/comrak |
| Zustand | https://docs.pmnd.rs/zustand |
| React | https://react.dev |

### 9.2 术语表

| 术语 | 说明 |
|------|------|
| Tauri | 跨平台桌面应用框架 |
| IPC | 进程间通信（前端与后端通信） |
| Plugin Trait | Rust 中的接口定义 |
| Command | Tauri 中暴露给前端的函数 |
| CBZ/CBR | 漫画格式（ZIP/RAR 打包） |
| EPUB | 电子书标准格式 |
| LRU | 最近最少使用缓存算法 |

### 9.3 联系方式

| 渠道 | 地址 |
|------|------|
| GitHub | https://github.com/your-org/willread |
| Issues | https://github.com/your-org/willread/issues |
| Discussions | https://github.com/your-org/willread/discussions |

---

*WillRead 开发环境与方法指导 v1.0*
