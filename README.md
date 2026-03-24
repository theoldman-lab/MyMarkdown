# Markdown 文档拆分与合并工具

一套用于 Markdown 文档模块化处理的工具集，支持按标题层级拆分文档，以及将模块化文档合并为完整文档。

## 工具概览

| 工具 | 功能 |
|------|------|
| `split_md.py` | 将大型 Markdown 文档按标题层级拆分为多个文件 |
| `merge_md.py` | 将拆分后的 Markdown 文件合并为完整文档 |

---

## split_md.py - 文档拆分工具

按标题层级将 Markdown 文档拆分为文件夹和文件结构。

### 用法

```bash
python3 split_md.py <输入文件> <输出目录> [选项]
```

### 参数

| 参数 | 说明 |
|------|------|
| `input` | 输入的 Markdown 文件路径 |
| `output` | 输出目录路径 |
| `-d, --depth` | 最大拆分深度（1-6），默认为 2 |
| `-v, --verbose` | 显示详细处理日志 |

### 拆分深度说明

| 深度值 | 行为 |
|--------|------|
| `1` | 只按一级标题（`#`）拆分 |
| `2` | 按一级标题创建文件夹，按二级标题（`##`）拆分文件（默认） |
| `3` | 继续按三级标题（`###`）创建子文件夹 |
| `4-6` | 依此类推，支持更深层次的拆分 |

### 示例

```bash
# 默认拆分（一级标题为文件夹，二级标题为文件）
python3 split_md.py document.md output/

# 按三级标题继续拆分子文件夹
python3 split_md.py document.md output/ -d 3

# 只按一级标题拆分
python3 split_md.py document.md output/ -d 1

# 显示详细日志
python3 split_md.py document.md output/ -v
```

### 输出结构示例

假设输入文件 `book.md` 内容如下：

```markdown
# 第一章

## 第一节
内容...

## 第二节
内容...

# 第二章

## 第一节
内容...
```

运行 `python3 split_md.py book.md output/` 后生成：

```
output/
├── main_source.md          # 合并指令文件
├── 第一章/
│   ├── 第一节.md
│   └── 第二节.md
└── 第二章/
    └── 第一节.md
```

---

## merge_md.py - 文档合并工具

将模块化的 Markdown 文件合并为单个完整文档。

### 用法

```bash
python3 merge_md.py <主文件> <输出文件> [选项]
```

### 参数

| 参数 | 说明 |
|------|------|
| `input` | 主文件路径（通常是 `main_source.md`） |
| `output` | 输出文件路径 |
| `-v, --verbose` | 显示详细处理日志 |

### 包含指令语法

在主文件中使用以下指令包含其他文件：

```markdown
!include path/to/file.md
```

### 示例

```bash
# 合并文档
python3 merge_md.py main_source.md merged.md

# 显示详细日志
python3 merge_md.py main_source.md merged.md -v
```

### 主文件示例

`main_source.md` 内容：

```markdown
---
title: 合并后的文档
---

# 合并文档

!include 第一章/第一节.md
!include 第一章/第二节.md
!include 第二章/第一节.md
```

---

## 典型工作流

### 1. 拆分大型文档

```bash
# 将大型文档按章节拆分
python3 split_md.py large-document.md chapters/
```

### 2. 编辑模块化文件

在生成的目录结构中编辑各个章节文件。

### 3. 合并为完整文档

```bash
# 使用生成的 main_source.md 合并所有文件
python3 merge_md.py chapters/main_source.md final-document.md
```

---

## 注意事项

1. **文件编码**：确保所有 Markdown 文件使用 UTF-8 编码
2. **循环引用**：工具会检测并防止文件循环引用
3. **YAML Front Matter**：合并时只保留主文件的 Front Matter
4. **标题层级**：拆分深度最大支持 6 级（对应 Markdown 的 `######`）

---

## 许可证

MIT License
