#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
from pathlib import Path


def sanitize_filename(name):
    """清理文件名，移除非法字符"""
    # 移除前后空白
    name = name.strip()
    # 替换非法字符
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '']
    for char in invalid_chars:
        name = name.replace(char, '')
    # 替换多个空格为单个空格
    name = re.sub(r'\s+', ' ', name)
    return name


def split_markdown(input_file, output_dir, verbose=False):
    """
    拆分 Markdown 文件
    按一级标题拆分文件夹，按二级标题拆分文件
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 YAML Front Matter（如果有）
    front_matter_match = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
    front_matter = front_matter_match.group(0) if front_matter_match else ''
    if front_matter:
        content = content[len(front_matter):]

    # 按一级标题分割
    h1_pattern = re.compile(r'^#\s+(.+?)\s*$', re.MULTILINE)
    
    # 找到所有一级标题的位置
    h1_matches = list(h1_pattern.finditer(content))
    
    if not h1_matches:
        print("错误：未找到一级标题 (#)")
        sys.exit(1)

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sections = []
    for i, match in enumerate(h1_matches):
        title = match.group(1).strip()
        start = match.end()
        end = h1_matches[i + 1].start() if i + 1 < len(h1_matches) else len(content)
        section_content = content[start:end].strip()
        sections.append((title, section_content))

    print(f"找到 {len(sections)} 个一级标题")

    # 主文件的包含指令列表
    main_includes = []

    for h1_title, h1_content in sections:
        # 创建一级标题对应的文件夹
        h1_dirname = sanitize_filename(h1_title)
        h1_dir = output_path / h1_dirname
        h1_dir.mkdir(parents=True, exist_ok=True)

        print(f"  创建文件夹：{h1_dirname}/")

        # 按二级标题分割
        h2_pattern = re.compile(r'^##\s+(.+?)\s*$', re.MULTILINE)
        h2_matches = list(h2_pattern.finditer(h1_content))

        if not h2_matches:
            # 如果没有二级标题，将整个章节保存为一个文件
            filename = sanitize_filename(h1_title) + '.md'
            filepath = h1_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                f.write(f"# {h1_title}\n\n")
                f.write(h1_content)
            
            main_includes.append(f"!include {h1_dirname}/{filename}")
            print(f"    - {filename}")
            continue

        # 有二级标题，按二级标题拆分
        h2_files = []
        for j, h2_match in enumerate(h2_matches):
            h2_title = h2_match.group(1).strip()
            h2_start = h2_match.end()
            h2_end = h2_matches[j + 1].start() if j + 1 < len(h2_matches) else len(h1_content)
            h2_content = h1_content[h2_start:h2_end].strip()

            # 生成文件名
            filename = sanitize_filename(h2_title) + '.md'
            filepath = h1_dir / filename

            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                f.write(f"# {h1_title}\n\n")
                f.write(f"## {h2_title}\n\n")
                f.write(h2_content)

            h2_files.append(filename)
            print(f"    - {filename}")

        # 添加该章节的包含指令
        main_includes.append(f"\n# {h1_title}")
        for filename in h2_files:
            main_includes.append(f"!include {h1_dirname}/{filename}")

    # 生成 main_source.md 文件（供 merge_md.py 使用）
    main_md_path = output_path / 'main_source.md'
    with open(main_md_path, 'w', encoding='utf-8') as f:
        if front_matter:
            f.write(front_matter)
            f.write('\n')
        f.write('# 合并文档\n\n')
        f.write('\n'.join(main_includes))
        f.write('\n')

    print(f"\n生成 main_source.md 文件")
    print(f"完成！输出目录：{output_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(description="Markdown 文件拆分工具")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("output", help="输出目录路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细处理日志")

    args = parser.parse_args()

    try:
        split_markdown(args.input, args.output, verbose=args.verbose)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
