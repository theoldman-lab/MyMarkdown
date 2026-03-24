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


def split_by_heading(content, heading_level, front_matter, max_depth=2):
    """
    递归按标题层级拆分内容
    
    Args:
        content: 要拆分的 Markdown 内容
        heading_level: 当前标题级别（1-6）
        front_matter: YAML Front Matter
        max_depth: 最大拆分深度（即拆分到第几级标题）
    
    Returns:
        list: [(title, content, sub_items), ...] 其中 sub_items 是下一级拆分结果
    """
    if heading_level > 6 or heading_level > max_depth:
        return []
    
    # 构建当前级别的标题正则
    hashes = '#' * heading_level
    pattern = re.compile(rf'^{hashes}\s+(.+?)\s*$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    
    if not matches:
        return []
    
    sections = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_content = content[start:end].strip()
        
        # 递归处理下一级标题
        sub_items = split_by_heading(section_content, heading_level + 1, front_matter, max_depth)
        sections.append((title, section_content, sub_items))
    
    return sections


def write_split_files(sections, output_path, front_matter, path_prefix, heading_level, max_depth, main_includes, indent=0):
    """
    递归写入拆分后的文件
    
    Args:
        sections: [(title, content, sub_items), ...]
        output_path: 输出目录路径
        front_matter: YAML Front Matter
        path_prefix: 当前路径前缀（用于 include 指令）
        heading_level: 当前标题级别
        max_depth: 最大拆分深度
        main_includes: 主文件包含指令列表
        indent: 当前层级缩进
    """
    indent_str = "  " * indent
    
    for title, content, sub_items in sections:
        safe_title = sanitize_filename(title)
        
        # 判断是否还有下一级拆分
        has_sub_items = len(sub_items) > 0
        is_last_level = heading_level >= max_depth
        
        if has_sub_items and not is_last_level:
            # 创建子文件夹
            sub_dir = output_path / safe_title
            sub_dir.mkdir(parents=True, exist_ok=True)
            print(f"{indent_str}  创建文件夹：{safe_title}/")
            
            # 递归处理下一级
            sub_path_prefix = f"{path_prefix}{safe_title}/" if path_prefix else f"{safe_title}/"
            write_split_files(sub_items, sub_dir, front_matter, sub_path_prefix, 
                            heading_level + 1, max_depth, main_includes, indent + 1)
        else:
            # 创建文件
            if heading_level == 1:
                filename = safe_title + '.md'
                filepath = output_path / filename
                file_path_prefix = f"{path_prefix}{filename}"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    if front_matter:
                        f.write(front_matter)
                        f.write('\n')
                    f.write(f"# {title}\n\n")
                    f.write(content)
            else:
                # 对于更深层级，需要构建完整的标题链
                filename = safe_title + '.md'
                filepath = output_path / filename
                file_path_prefix = f"{path_prefix}{filename}"
                
                # 构建标题前缀链
                heading_prefix = "# " * (heading_level - 1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    if front_matter:
                        f.write(front_matter)
                        f.write('\n')
                    # 添加上级标题链（从 path_prefix 推导）
                    if path_prefix:
                        parts = path_prefix.rstrip('/').split('/')
                        for idx, part in enumerate(parts):
                            hash_count = idx + 1
                            f.write(f"{'#' * hash_count} {part}\n\n")
                    f.write(f"{'#' * heading_level} {title}\n\n")
                    f.write(content)
            
            main_includes.append(f"{indent_str}!include {file_path_prefix}")
            print(f"{indent_str}    - {filename}")


def split_markdown(input_file, output_dir, max_depth=2, verbose=False):
    """
    拆分 Markdown 文件
    按一级标题拆分文件夹，并可指定向下拆分的标题层级深度
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录路径
        max_depth: 最大拆分深度（1-6），即拆分到第几级标题
                   1 = 只按一级标题拆分
                   2 = 按一级标题拆分文件夹，按二级标题拆分文件（默认）
                   3 = 继续按三级标题拆分子文件夹
                   以此类推...
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
        
        # 递归处理下一级标题
        sub_items = split_by_heading(section_content, 2, front_matter, max_depth)
        sections.append((title, section_content, sub_items))

    print(f"找到 {len(sections)} 个一级标题，最大拆分深度：{max_depth}")

    # 主文件的包含指令列表
    main_includes = []

    for h1_title, h1_content, sub_items in sections:
        h1_dirname = sanitize_filename(h1_title)
        
        # 判断是否需要创建子文件夹
        has_sub_items = len(sub_items) > 0
        need_subdir = max_depth >= 2 and has_sub_items
        
        if need_subdir:
            # 创建一级标题对应的文件夹
            h1_dir = output_path / h1_dirname
            h1_dir.mkdir(parents=True, exist_ok=True)
            print(f"  创建文件夹：{h1_dirname}/")
            
            # 递归写入文件
            sub_path_prefix = f"{h1_dirname}/"
            write_split_files(sub_items, h1_dir, front_matter, sub_path_prefix, 
                            2, max_depth, main_includes, 1)
        else:
            # 没有子拆分或不需要子拆分，直接创建文件
            filename = sanitize_filename(h1_title) + '.md'
            filepath = output_path / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                if front_matter:
                    f.write(front_matter)
                    f.write('\n')
                f.write(f"# {h1_title}\n\n")
                f.write(h1_content)

            main_includes.append(f"!include {filename}")
            print(f"    - {filename}")

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
    parser.add_argument("-d", "--depth", type=int, default=2, 
                        help="最大拆分深度（1-6），即拆分到第几级标题。默认值为 2（按二级标题拆分）")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细处理日志")

    args = parser.parse_args()

    if args.depth < 1 or args.depth > 6:
        print("错误：拆分深度必须在 1-6 之间")
        sys.exit(1)

    try:
        split_markdown(args.input, args.output, max_depth=args.depth, verbose=args.verbose)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
