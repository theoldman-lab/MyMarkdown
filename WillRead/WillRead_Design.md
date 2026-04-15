# WillRead 本地阅读器设计方案

## 一、项目概述

**WillRead** 是一款跨平台本地阅读器软件，旨在为用户提供统一、流畅的文档阅读体验。支持 PDF、Markdown、电子书（EPUB/MOBI/AZW3）和电子漫画（CBZ/CBR）等多种格式，采用模块化插件架构，便于扩展和维护。

### 1.1 核心目标

- **多格式统一支持**：一个应用阅读多种文档格式
- **模块化架构**：格式解析插件化，易于扩展新格式
- **跨平台一致体验**：Windows、macOS、Linux 统一 UI/UX
- **轻量高性能**：快速启动、低内存占用、流畅渲染

---

## 二、技术栈选型

### 2.1 整体架构

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 框架 | **Tauri v2** | Rust 后端 + Web 前端，轻量安全 |
| 后端语言 | **Rust** | 高性能、内存安全、并发友好 |
| 前端框架 | **React + TypeScript** | 成熟生态、组件化开发 |
| 状态管理 | **Zustand** | 轻量、Hook 友好 |
| 样式方案 | **TailwindCSS** | 原子化 CSS、快速开发 |

### 2.2 为什么选择 Tauri？

| 维度 | Tauri | Electron | Flutter | Qt |
|------|-------|----------|---------|----|
| 打包体积 | 3-15MB | 80-150MB | 15-30MB | 20-50MB |
| 内存占用 | ~50-150MB | ~200-500MB | ~150-250MB | ~80-200MB |
| 插件化 | Rust 原生支持 | Node.js 模块 | 困难 | 动态库 |
| 开发效率 | 高 | 极高 | 高 | 中等 |
| 适合阅读器 | ✅ 最佳 | 过重 | 生态弱 | UI 现代化成本 |

---

## 三、系统架构

### 3.1 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        WillRead 前端 (React)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ 
│  │ Reader      │  │ Library     │  │ Settings    │  │ Toolbar │ │
│  │ Component   │  │ View        │  │ Panel       │  │         │ │
│  └─────────────┘  └─────────────┘  
└─────────────┘  └─────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐ │
│  │ PDF Viewer  │  │ MD Viewer   │  │ Comic/EPUB Viewer        │ │
│  └─────────────┘  └─────────────┘  └──────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Tauri IPC Bridge (Commands)                   │
├─────────────────────────────────────────────────────────────────┤
│                      Rust Backend Core                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Format Router                            │  │
│  │         (根据文件扩展名/内容路由到对应插件)                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │ PDF      │ │ Markdown │ │ EPUB     │ │ MOBI/    │ │ Comic │ │
│  │ Plugin   │ │ Plugin   │ │ Plugin   │ │ AZW3     │ │Plugin │ │
│  │          │ │          │ │          │ │ Plugin   │ │       │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────┘ │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────────┐ │
│  │ File      │  │ Cache     │  │ Bookmark  │  │ Config       │ │
│  │ Service   │  │ Service   │  │ Service   │  │ Service      │ │
│  └───────────┘  └───────────┘  └───────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                     Native Libraries                             │
│  ┌──────────┐  ┌───────────┐  ┌───────────┐  ┌──────────────┐ │
│  │ PDFium     │  │ libunrar  │  │ libarchive│  │ System Fonts │ │
│  └───────────┘  └───────────┘  └───────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 项目目录结构

```
willread/
├── src-tauri/                          # Rust 后端
│   ├── src/
│   │   ├── main.rs                     # Tauri 入口
│   │   ├── lib.rs                      # 核心逻辑
│   │   ├── plugins/                    # 格式插件模块
│   │   │   ├── mod.rs                  # FormatPlugin Trait 定义
│   │   │   ├── registry.rs             # 插件注册与路由
│   │   │   ├── pdf.rs                  # PDF 插件 (pdfium-render)
│   │   │   ├── markdown.rs             # Markdown 插件 (comrak)
│   │   │   ├── epub.rs                 # EPUB 插件
│   │   │   ├── mobi.rs                 # MOBI/AZW3 插件
│   │   │   └── comic.rs                # CBZ/CBR 漫画插件
│   │   ├── services/                   # 核心服务
│   │   │   ├── mod.rs
│   │   │   ├── cache.rs                # LRU 缓存管理
│   │   │   ├── bookmark.rs             # 书签持久化
│   │   │   └── config.rs               # 配置管理
│   │   └── commands/                   # Tauri Commands
│   │       ├── mod.rs
│   │       ├── document.rs             # 文档操作（打开、关闭）
│   │       ├── reader.rs               # 阅读器控制（翻页、缩放）
│   │       └── settings.rs             # 设置管理
│   ├── Cargo.toml
│   ├── build.rs
│   └── tauri.conf.json
├── src/                                # React 前端
│   ├── components/
│   │   ├── Reader/                     # 阅读器组件
│   │   │   ├── PdfViewer.tsx
│   │   │   ├── MarkdownViewer.tsx
│   │   │   ├── EpubViewer.tsx
│   │   │   ├── ComicViewer.tsx
│   │   │   ├── PageNavigator.tsx
│   │   │   ├── ZoomControls.tsx
│   │   │   └── VirtualScroller.tsx
│   │   ├── Library/                    # 书架/库视图
│   │   │   ├── LibraryGrid.tsx
│   │   │   ├── BookCard.tsx
│   │   │   └── BookDetail.tsx
│   │   ├── Sidebar/                    # 侧边栏
│   │   │   ├── TocPanel.tsx            # 目录面板
│   │   │   ├── BookmarkPanel.tsx       # 书签面板
│   │   │   └── SearchPanel.tsx         # 搜索面板
│   │   ├── Toolbar/                    # 顶部工具栏
│   │   │   ├── MainToolbar.tsx
│   │   │   └── ViewModeSwitch.tsx
│   │   └── Settings/                   # 设置面板
│   │       ├── GeneralSettings.tsx
│   │       ├── AppearanceSettings.tsx
│   │       └── PluginSettings.tsx
│   ├── store/                          # Zustand 状态管理
│   │   ├── readerStore.ts
│   │   ├── libraryStore.ts
│   │   ├── settingsStore.ts
│   │   └── uiStore.ts
│   ├── hooks/                          # 自定义 Hooks
│   │   ├── useDocument.ts
│   │   ├── useKeyboard.ts
│   │   └── useTheme.ts
│   ├── styles/
│   │   ├── global.css
│   │   └── themes.css
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 四、格式支持详细设计

### 4.1 核心插件接口（Rust Trait）

```rust
// src-tauri/src/plugins/mod.rs

use std::path::Path;
use serde::{Serialize, Deserialize};

/// 文档元数据
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct DocumentMetadata {
    pub title: Option<String>,
    pub author: Option<String>,
    pub publisher: Option<String>,
    pub created: Option<String>,
    pub page_count: usize,
    pub file_size: u64,
}

/// 目录项
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TocEntry {
    pub title: String,
    pub page: usize,
    pub children: Vec<TocEntry>,
}

/// 书签
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Bookmark {
    pub page: usize,
    pub title: String,
    pub created_at: i64,
}

/// 渲染内容（传递给前端）
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct RenderedContent {
    pub data: String,           // Base64 图片或 HTML 内容
    pub width: u32,
    pub height: u32,
    pub content_type: ContentType,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum ContentType {
    ImagePng,
    ImageJpeg,
    Html,
    Text,
    Svg,
}

/// 错误类型
#[derive(Debug)]
pub enum PluginError {
    IoError(String),
    ParseError(String),
    RenderError(String),
    UnsupportedFormat(String),
}

/// 核心插件 Trait - 所有格式插件必须实现此接口
#[async_trait]
pub trait FormatPlugin: Send + Sync {
    /// 格式名称标识
    fn format_name(&self) -> &str;

    /// 支持的文件扩展名
    fn supported_extensions(&self) -> &[&str];

    /// 检测文件格式
    async fn detect_format(&self, path: &Path) -> Result<bool, PluginError>;

    /// 获取文档元数据
    async fn get_metadata(&self, path: &Path) -> Result<DocumentMetadata, PluginError>;

    /// 渲染指定页/内容
    async fn render_page(
        &self,
        path: &Path,
        page: usize,
        options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError>;

    /// 获取总页数
    async fn page_count(&self, path: &Path) -> Result<usize, PluginError>;

    /// 提取文本（用于全文搜索）
    async fn extract_text(&self, path: &Path) -> Result<String, PluginError>;

    /// 获取目录
    async fn get_toc(&self, path: &Path) -> Result<Vec<TocEntry>, PluginError>;
}

/// 渲染选项
#[derive(Clone, Debug)]
pub struct RenderOptions {
    pub dpi: f32,
    pub width: u32,
    pub height: u32,
    pub grayscale: bool,
}
```

### 4.2 插件注册与路由

```rust
// src-tauri/src/plugins/registry.rs

use std::collections::HashMap;
use std::path::Path;

pub struct PluginRegistry {
    plugins: HashMap<String, Box<dyn FormatPlugin>>,
    extension_map: HashMap<String, String>, // ".pdf" -> "pdf"
}

impl PluginRegistry {
    pub fn new() -> Self {
        Self {
            plugins: HashMap::new(),
            extension_map: HashMap::new(),
        }
    }

    /// 注册插件
    pub fn register(&mut self, plugin: Box<dyn FormatPlugin>) {
        let name = plugin.format_name().to_string();
        for ext in plugin.supported_extensions() {
            self.extension_map
                .insert(ext.to_lowercase(), name.clone());
        }
        self.plugins.insert(name, plugin);
        log::info!("Registered plugin: {}", plugin.format_name());
    }

    /// 根据文件路径获取对应插件
    pub fn get_plugin_for_file(&self, path: &Path) -> Option<&dyn FormatPlugin> {
        if let Some(ext) = path.extension() {
            let ext_str = format!(".{}", ext.to_string_lossy().to_lowercase());
            if let Some(plugin_name) = self.extension_map.get(&ext_str) {
                return self.plugins.get(plugin_name).map(|p| p.as_ref());
            }
        }
        None
    }

    /// 获取所有已注册格式
    pub fn supported_formats(&self) -> Vec<&str> {
        self.plugins.values().map(|p| p.format_name()).collect()
    }
}
```

### 4.3 各格式插件实现要点

#### 4.3.1 PDF 插件

```rust
// src-tauri/src/plugins/pdf.rs
// 依赖：pdfium-render

use pdfium_render::prelude::*;

pub struct PdfPlugin {
    pdfium: Pdfium,
}

impl PdfPlugin {
    pub fn new() -> Self {
        let pdfium = Pdfium::new(
            Pdfium::bind_to_library(
                Pdfium::pdfium_platform_library_name_at_path("./libpdfium.so")
            ).expect("Failed to load PDFium")
        );
        Self { pdfium }
    }
}

#[async_trait]
impl FormatPlugin for PdfPlugin {
    fn format_name(&self) -> &str { "pdf" }
    fn supported_extensions(&self) -> &[&str] { &[".pdf"] }

    async fn render_page(
        &self,
        path: &Path,
        page: usize,
        options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError> {
        let doc = self.pdfium.load_pdf_from_file(path, None)
            .map_err(|e| PluginError::IoError(e.to_string()))?;
        let page = doc.pages().get(page)
            .map_err(|e| PluginError::ParseError(e.to_string()))?;

        let render = page.render()
            .with_scale(options.dpi / 72.0)
            .render();

        let image_data = render.as_png()
            .map_err(|e| PluginError::RenderError(e.to_string()))?;

        Ok(RenderedContent {
            data: base64::encode(&image_data),
            width: render.width() as u32,
            height: render.height() as u32,
            content_type: ContentType::ImagePng,
        })
    }
    // ... 其他方法实现
}
```

#### 4.3.2 Markdown 插件

```rust
// src-tauri/src/plugins/markdown.rs
// 依赖：comrak, frontmatter

use comrak::{markdown_to_html, ComrakOptions};

pub struct MarkdownPlugin;

#[async_trait]
impl FormatPlugin for MarkdownPlugin {
    fn format_name(&self) -> &str { "markdown" }
    fn supported_extensions(&self) -> &[&str] { &[".md", ".markdown", ".mdx"] }

    async fn render_page(
        &self,
        path: &Path,
        _page: usize,
        _options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError> {
        let content = tokio::fs::read_to_string(path)
            .await
            .map_err(|e| PluginError::IoError(e.to_string()))?;

        // 解析 frontmatter
        let (body, _frontmatter) = parse_frontmatter(&content);

        let mut options = ComrakOptions::default();
        options.extension.table = true;
        options.extension.strikethrough = true;
        options.extension.tasklist = true;
        options.extension.footnotes = true;

        let html = markdown_to_html(&body, &options);

        Ok(RenderedContent {
            data: html,
            width: 0,
            height: 0,
            content_type: ContentType::Html,
        })
    }

    // Markdown 视为单页文档
    async fn page_count(&self, _path: &Path) -> Result<usize, PluginError> {
        Ok(1)
    }
}
```

#### 4.3.3 EPUB 插件

```rust
// src-tauri/src/plugins/epub.rs
// 依赖：epub, zip

pub struct EpubPlugin;

#[async_trait]
impl FormatPlugin for EpubPlugin {
    fn format_name(&self) -> &str { "epub" }
    fn supported_extensions(&self) -> &[&str] { &[".epub"] }

    async fn render_page(
        &self,
        path: &Path,
        page: usize,
        _options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError> {
        // 1. 解压 EPUB（ZIP 格式）
        // 2. 解析 OPF 获取 spine（阅读顺序）
        // 3. 获取第 page 个章节的 HTML 内容
        // 4. 内联 CSS 并返回 HTML 内容
        // ...
    }

    async fn get_toc(&self, path: &Path) -> Result<Vec<TocEntry>, PluginError> {
        // 解析 NCX 或 nav.xhtml 获取目录
        // ...
    }
}
```

#### 4.3.4 漫画插件（CBZ/CBR）

```rust
// src-tauri/src/plugins/comic.rs
// 依赖：zip, unrar, image

pub struct ComicPlugin;

#[async_trait]
impl FormatPlugin for ComicPlugin {
    fn format_name(&self) -> &str { "comic" }
    fn supported_extensions(&self) -> &[&str] { &[".cbz", ".cbr"] }

    async fn render_page(
        &self,
        path: &Path,
        page: usize,
        options: &RenderOptions,
    ) -> Result<RenderedContent, PluginError> {
        // 1. 根据扩展名选择解压方式
        let ext = path.extension().unwrap().to_string_lossy();

        let images = match ext.as_ref() {
            "cbz" => extract_cbz(path)?,
            "cbr" => extract_cbr(path)?,
            _ => return Err(PluginError::Unsupported_format(ext.to_string())),
        };

        // 2. 按文件名排序（自然排序）
        let mut sorted: Vec<_> = images.into_iter().collect();
        sorted.sort_by(|a, b| natural_sort(&a.name, &b.name));

        // 3. 获取指定页图片
        let img_data = &sorted[page].data;

        // 4. 可选：缩放/优化
        let img = image::load_from_memory(img_data)
            .map_err(|e| PluginError::RenderError(e.to_string()))?;

        let resized = img.resize(
            options.width,
            options.height,
            image::imageops::FilterType::Lanczos3,
        );

        let mut output = Vec::new();
        resized.write_to(&mut std::io::Cursor::new(&mut output), image::ImageOutputFormat::Png)
            .map_err(|e| PluginError::RenderError(e.to_string()))?;

        Ok(RenderedContent {
            data: base64::encode(&output),
            width: options.width,
            height: options.height,
            content_type: ContentType::ImagePng,
        })
    }
}
```

---

## 五、前端设计

### 5.1 状态管理（Zustand）

```typescript
// src/store/readerStore.ts

import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';

export interface Document {
  id: string;
  path: string;
  format: string;
  title: string;
  author?: string;
  currentPage: number;
  totalPages: number;
  zoom: number;
  rotation: number;
}

interface ReaderState {
  currentDoc: Document | null;
  content: string | null;       // Base64 或 HTML
  contentWidth: number;
  contentHeight: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  openDocument: (path: string) => Promise<void>;
  goToPage: (page: number) => Promise<void>;
  nextPage: () => void;
  prevPage: () => void;
  setZoom: (zoom: number) => void;
  setRotation: (rotation: number) => void;
  closeDocument: () => void;
}

export const useReaderStore = create<ReaderState>((set, get) => ({
  currentDoc: null,
  content: null,
  contentWidth: 0,
  contentHeight: 0,
  isLoading: false,
  error: null,

  openDocument: async (path: string) => {
    set({ isLoading: true, error: null });
    try {
      const metadata = await invoke('get_document_metadata', { path });
      const content = await invoke('render_page', { path, page: 0 });

      set({
        currentDoc: {
          id: crypto.randomUUID(),
          path,
          format: metadata.format,
          title: metadata.title || path.split('/').pop()!,
          author: metadata.author,
          currentPage: 0,
          totalPages: metadata.page_count,
          zoom: 100,
          rotation: 0,
        },
        content: content.data,
        contentWidth: content.width,
        contentHeight: content.height,
        isLoading: false,
      });
    } catch (e) {
      set({ error: String(e), isLoading: false });
    }
  },

  goToPage: async (page: number) => {
    const { currentDoc } = get();
    if (!currentDoc) return;

    const content = await invoke('render_page', {
      path: currentDoc.path,
      page,
    });

    set({
      currentDoc: { ...currentDoc, currentPage: page },
      content: content.data,
      contentWidth: content.width,
      contentHeight: content.height,
    });

    // 保存阅读进度
    await invoke('save_progress', {
      docId: currentDoc.id,
      page,
    });
  },

  nextPage: () => {
    const { currentDoc } = get();
    if (currentDoc && currentDoc.currentPage < currentDoc.totalPages - 1) {
      get().goToPage(currentDoc.currentPage + 1);
    }
  },

  prevPage: () => {
    const { currentDoc } = get();
    if (currentDoc && currentDoc.currentPage > 0) {
      get().goToPage(currentDoc.currentPage - 1);
    }
  },

  setZoom: (zoom: number) => {
    set((state) => ({
      currentDoc: state.currentDoc ? { ...state.currentDoc, zoom } : null,
    }));
  },

  setRotation: (rotation: number) => {
    set((state) => ({
      currentDoc: state.currentDoc ? { ...state.currentDoc, rotation } : null,
    }));
  },

  closeDocument: () => {
    set({ currentDoc: null, content: null, error: null });
  },
}));
```

### 5.2 核心阅读器组件

```tsx
// src/components/Reader/ReaderView.tsx

import React from 'react';
import { useReaderStore } from '../../store/readerStore';
import { PdfViewer } from './PdfViewer';
import { MarkdownViewer } from './MarkdownViewer';
import { ComicViewer } from './ComicViewer';
import { EpubViewer } from './EpubViewer';
import { Toolbar } from '../Toolbar/MainToolbar';
import { TocPanel } from '../Sidebar/TocPanel';
import { VirtualScroller } from './VirtualScroller';

export const ReaderView: React.FC = () => {
  const { currentDoc, content, isLoading, error } = useReaderStore();

  if (!currentDoc) {
    return <EmptyState />;
  }

  const renderViewer = () => {
    const props = { content, document: currentDoc };

    switch (currentDoc.format) {
      case 'pdf':
        return <PdfViewer {...props} />;
      case 'markdown':
        return <MarkdownViewer {...props} />;
      case 'epub':
        return <EpubViewer {...props} />;
      case 'comic':
        return <ComicViewer {...props} />;
      default:
        return <UnsupportedFormat />;
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <Toolbar />
      <div className="flex flex-1 overflow-hidden">
        <TocPanel />
        <main className="flex-1 overflow-auto">
          {isLoading && <LoadingSpinner />}
          {error && <ErrorDisplay message={error} />}
          {!isLoading && !error && (
            <VirtualScroller>
              {renderViewer()}
            </VirtualScroller>
          )}
        </main>
      </div>
    </div>
  );
};
```

### 5.3 PDF 查看器

```tsx
// src/components/Reader/PdfViewer.tsx

import React from 'react';
import { useReaderStore } from '../../store/readerStore';

interface PdfViewerProps {
  content: string | null;
  document: Document;
}

export const PdfViewer: React.FC<PdfViewerProps> = ({ content, document }) => {
  const { setZoom, nextPage, prevPage } = useReaderStore();

  return (
    <div className="flex flex-col items-center p-4">
      <div
        className="bg-white shadow-lg"
        style={{
          transform: `scale(${document.zoom / 100}) rotate(${document.rotation}deg)`,
          transformOrigin: 'top center',
        }}
      >
        {content && (
          <img
            src={`data:image/png;base64,${content}`}
            alt={`Page ${document.currentPage + 1}`}
            className="max-w-full"
          />
        )}
      </div>

      {/* 键盘快捷键 */}
      <KeyboardHandler
        onNext={nextPage}
        onPrev={prevPage}
        onZoomIn={() => setZoom(document.zoom + 10)}
        onZoomOut={() => setZoom(document.zoom - 10)}
      />
    </div>
  );
};
```

### 5.4 Markdown 查看器

```tsx
// src/components/Reader/MarkdownViewer.tsx

import React, { useEffect, useRef } from 'react';

interface MarkdownViewerProps {
  content: string | null;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 加载 highlight.js 并应用语法高亮
    import('highlight.js').then((hljs) => {
      containerRef.current?.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block as HTMLElement);
      });
    });

    // 处理内部链接点击
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.tagName === 'A') {
        e.preventDefault();
        // 处理锚点跳转
        const href = (target as HTMLAnchorElement).getAttribute('href');
        if (href?.startsWith('#')) {
          const el = containerRef.current?.querySelector(href);
          el?.scrollIntoView();
        }
      }
    };

    containerRef.current?.addEventListener('click', handleClick);
    return () => containerRef.current?.removeEventListener('click', handleClick);
  }, [content]);

  return (
    <div className="max-w-4xl mx-auto p-8 prose prose-lg dark:prose-invert">
      <div
        ref={containerRef}
        dangerouslySetInnerHTML={{ __html: content || '' }}
      />
    </div>
  );
};
```

### 5.5 漫画查看器

```tsx
// src/components/Reader/ComicViewer.tsx

import React, { useState, useCallback } from 'react';
import { useReaderStore } from '../../store/readerStore';

interface ComicViewerProps {
  content: string | null;
  document: Document;
}

export const ComicViewer: React.FC<ComicViewerProps> = ({ content, document }) => {
  const [viewMode, setViewMode] = useState<'single' | 'double' | 'scroll'>('single');
  const { goToPage } = useReaderStore();

  // 预加载前后页
  const preloadPages = useCallback(() => {
    const pages = [];
    for (let i = -2; i <= 2; i++) {
      const p = document.currentPage + i;
      if (p >= 0 && p < document.totalPages) {
        pages.push(p);
      }
    }
    return pages;
  }, [document.currentPage, document.totalPages]);

  return (
    <div className="flex flex-col items-center bg-gray-900 min-h-full">
      <ViewModeSwitch mode={viewMode} onChange={setViewMode} />

      {viewMode === 'single' && (
        <div className="flex items-center justify-center flex-1 p-4">
          <img
            src={`data:image/png;base64,${content}`}
            alt={`Page ${document.currentPage + 1}`}
            className="max-h-full object-contain"
          />
        </div>
      )}

      {viewMode === 'double' && (
        <div className="flex items-center justify-center flex-1 p-4 gap-2">
          {/* 双页模式需要额外加载下一页 */}
        </div>
      )}

      {viewMode === 'scroll' && (
        <VirtualScroller
          onLoadMore={(direction) => {
            if (direction === 'down') goToPage(document.currentPage + 5);
            if (direction === 'up') goToPage(document.currentPage - 5);
          }}
        >
          {/* 长滚动模式 */}
        </VirtualScroller>
      )}
    </div>
  );
};
```

---

## 六、Tauri 命令（IPC API）

```rust
// src-tauri/src/commands/document.rs

use tauri::State;
use crate::plugins::registry::PluginRegistry;
use crate::plugins::*;

#[tauri::command]
pub async fn open_document(
    path: String,
    registry: State<'_, PluginRegistry>,
) -> Result<DocumentMetadata, String> {
    let path = std::path::Path::new(&path);
    let plugin = registry
        .get_plugin_for_file(path)
        .ok_or("Unsupported file format")?;

    plugin.detect_format(path).await
        .map_err(|e| e.to_string())?;

    plugin.get_metadata(path).await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn render_page(
    path: String,
    page: usize,
    registry: State<'_, PluginRegistry>,
) -> Result<RenderedContent, String> {
    let path = std::path::Path::new(&path);
    let plugin = registry
        .get_plugin_for_file(path)
        .ok_or("Unsupported file format")?;

    let options = RenderOptions {
        dpi: 150.0,
        width: 1200,
        height: 1600,
        grayscale: false,
    };

    plugin.render_page(path, page, &options).await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn get_toc(
    path: String,
    registry: State<'_, PluginRegistry>,
) -> Result<Vec<TocEntry>, String> {
    let path = std::path::Path::new(&path);
    let plugin = registry
        .get_plugin_for_file(path)
        .ok_or("Unsupported file format")?;

    plugin.get_toc(path).await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn search_in_document(
    path: String,
    query: String,
    registry: State<'_, PluginRegistry>,
) -> Result<Vec<SearchResult>, String> {
    let path = std::path::Path::new(&path);
    let plugin = registry
        .get_plugin_for_file(path)
        .ok_or("Unsupported file format")?;

    let text = plugin.extract_text(path).await
        .map_err(|e| e.to_string())?;

    // 简单全文搜索，可扩展为模糊搜索/正则
    let results = text
        .lines()
        .enumerate()
        .filter(|(_, line)| line.to_lowercase().contains(&query.to_lowercase()))
        .map(|(i, line)| SearchResult {
            line: i,
            text: line.to_string(),
        })
        .collect();

    Ok(results)
}
```

---

## 七、配置与持久化

### 7.1 用户配置结构

```rust
// src-tauri/src/services/config.rs

use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct AppConfig {
    pub appearance: AppearanceConfig,
    pub reader: ReaderConfig,
    pub library: LibraryConfig,
    pub plugins: PluginConfig,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct AppearanceConfig {
    pub theme: ThemeMode,       // light, dark, system
    pub font_family: String,
    pub font_size: u16,
    pub line_height: f32,
    pub page_margin: u16,
    pub background_color: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum ThemeMode {
    Light,
    Dark,
    System,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ReaderConfig {
    pub default_zoom: u16,
    pub scroll_mode: bool,          // true = 连续滚动, false = 分页
    pub page_turn_animation: bool,
    pub preload_pages: u8,          // 预加载页数
    pub remember_last_position: bool,
    pub comic_view_mode: ComicViewMode,  // single, double, scroll
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum ComicViewMode {
    Single,
    Double,
    Scroll,
}
```

### 7.2 书签与阅读进度存储

```rust
// src-tauri/src/services/bookmark.rs

use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::path::PathBuf;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ReadingProgress {
    pub file_path: String,
    pub current_page: usize,
    pub scroll_position: f64,
    pub last_read_at: i64,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct UserBookmark {
    pub id: String,
    pub file_path: String,
    pub page: usize,
    pub title: String,
    pub note: Option<String>,
    pub created_at: i64,
}

pub struct BookmarkService {
    data_path: PathBuf,
}

impl BookmarkService {
    pub fn save_progress(&self, progress: ReadingProgress) -> Result<(), String> {
        // 写入 JSON 或 SQLite
    }

    pub fn get_progress(&self, file_path: &str) -> Option<ReadingProgress> {
        // 读取阅读进度
    }

    pub fn add_bookmark(&self, bookmark: UserBookmark) -> Result<(), String> {
        // 添加书签
    }

    pub fn get_bookmarks(&self, file_path: &str) -> Vec<UserBookmark> {
        // 获取文档的所有书签
    }

    pub fn delete_bookmark(&self, id: &str) -> Result<(), String> {
        // 删除书签
    }
}
```

---

## 八、性能优化策略

### 8.1 渲染优化

| 策略 | 说明 |
|------|------|
| **分页预加载** | 当前页前后各预加载 N 页（可配置） |
| **LRU 缓存** | 缓存最近渲染的 N 页，避免重复渲染 |
| **虚拟滚动** | 长文档/漫画只渲染可视区域内的内容 |
| **Web Worker** | 图片解码和缩放放在 Worker 线程 |
| **图片懒加载** | 仅加载视口内的页面图片 |

### 8.2 内存优化

| 策略 | 说明 |
|------|------|
| **页级缓存淘汰** | 缓存超过阈值时，LRU 淘汰最旧页面 |
| **大文件分块** | EPUB 等大文件按章节加载，而非全量加载 |
| **渲染尺寸限制** | 限制最大渲染分辨率，避免超大图片 |

### 8.3 启动优化

| 策略 | 说明 |
|------|------|
| **懒加载插件** | 只在需要时初始化对应格式插件 |
| **延迟加载重型库** | PDFium 等重型库延迟加载 |
| **骨架屏** | 启动时显示骨架屏提升感知速度 |

---

## 九、书架/图书馆功能

### 9.1 本地书架

```typescript
interface LibraryBook {
  id: string;
  title: string;
  author?: string;
  coverPath?: string;       // 封面图片路径
  filePath: string;         // 文件绝对路径
  format: string;
  fileSize: number;
  addedAt: Date;
  lastReadAt?: Date;
  currentPage: number;
  totalPages: number;
  progress: number;         // 0-100
}
```

### 9.2 书架视图功能

- **网格/列表切换**：两种展示模式
- **排序**：按名称、添加时间、最后阅读时间排序
- **筛选**：按格式筛选
- **搜索**：按书名/作者搜索
- **分组**：按格式或未读/在读/已读完分组
- **封面提取**：从文件内自动提取封面

---

## 十、键盘快捷键设计

| 快捷键 | 功能 |
|--------|------|
| `←` / `→` | 上一页 / 下一页 |
| `Home` / `End` | 第一页 / 最后一页 |
| `+` / `-` | 放大 / 缩小 |
| `0` | 适应宽度 |
| `Ctrl+O` | 打开文件 |
| `Ctrl+F` | 全文搜索 |
| `Ctrl+B` | 添加/移除书签 |
| `Ctrl+L` | 跳转到指定页 |
| `Ctrl+T` | 切换目录面板 |
| `Ctrl+Shift+S` | 切换侧边栏 |
| `F11` | 全屏 |
| `R` | 旋转（漫画/图片） |
| `M` | 切换漫画阅读模式 |

---

## 十一、构建与打包

### 11.1 Cargo.toml 核心依赖

```toml
[package]
name = "willread"
version = "0.1.0"
edition = "2021"

[dependencies]
tauri = { version = "2.0", features = [] }
tauri-plugin-dialog = "2.0"
tauri-plugin-fs = "2.0"
tauri-plugin-store = "2.0"

# 格式解析
pdfium-render = "0.8"
comrak = "0.24"
epub = "2.0"
zip = "0.6"
unrar = "0.5"
image = "0.25"

# 工具
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.0", features = ["full"] }
base64 = "0.21"
log = "0.4"
dirs = "5.0"
chrono = "0.4"
async-trait = "0.1"
libloading = "0.8"

[build-dependencies]
tauri-build = "2.0"
```

### 11.2 Tauri 配置

```json
{
  "productName": "WillRead",
  "version": "0.1.0",
  "identifier": "com.willread.app",
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "frontendDist": "../dist",
    "devUrl": "http://localhost:5173"
  },
  "app": {
    "windows": [
      {
        "title": "WillRead",
        "width": 1280,
        "height": 800,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": ["icons/32x32.png", "icons/128x128.png", "icons/icon.icns", "icons/icon.ico"],
    "resources": ["libpdfium.so", "libpdfium.dylib", "pdfium.dll"]
  }
}
```

---

## 十二、开发路线图

### Phase 1: 基础框架 (MVP)
- [ ] Tauri 项目搭建
- [ ] 基础 UI 框架
- [ ] PDF 格式支持（查看、翻页、缩放）
- [ ] 文件打开功能

### Phase 2: 多格式支持
- [ ] Markdown 渲染
- [ ] EPUB 基础支持
- [ ] CBZ 漫画查看
- [ ] 格式插件接口完善

### Phase 3: 阅读体验
- [ ] 书架功能
- [ ] 书签与阅读进度
- [ ] 目录导航
- [ ] 全文搜索
- [ ] 暗色模式

### Phase 4: 增强功能
- [ ] MOBI/AZW3 支持
- [ ] CBR 支持
- [ ] 键盘快捷键
- [ ] 高级排版选项
- [ ] 打印支持

### Phase 5: 优化与发布
- [ ] 性能调优
- [ ] 多语言/国际化
- [ ] 安装包打包
- [ ] 自动化测试

---

## 十三、风险与挑战

| 风险 | 影响 | 应对方案 |
|------|------|----------|
| **PDFium 分发** | 需要随应用分发 PDFium 二进制 | 使用 `pdfium-binaries` npm 包，或改用 `mupdf-sys` |
| **MOBI/AZW3 解析** | Rust 生态库不成熟 | 考虑集成 Python Calibre 子进程或 C 库 |
| **CBR RAR 专利** | unrar 许可证限制 | 默认只支持 CBZ，CBR 作为可选功能 |
| **WebView 差异** | 各平台 WebView 渲染不一致 | 做好降级处理，避免使用最新 Web API |
| **CJK 字体渲染** | Linux 上中文显示问题 | 预置字体或提示用户安装 |
| **大文件性能** | 超大 PDF/EPUB 加载慢 | 分块加载、流式解析、后台预加载 |

---

## 十四、未来扩展方向

1. **插件市场**：允许第三方开发格式插件
2. **注释/高亮**：PDF 和 EPUB 的批注功能
3. **OCR 支持**：图片型 PDF 的 OCR 文字识别
4. **同步功能**：通过 WebDAV 同步阅读进度和书签
5. **听书功能**：TTS 文字转语音
6. **翻译集成**：选词翻译功能
7. **笔记导出**：导出笔记为 Markdown

---

*WillRead — 一个应用，阅读万物。*
