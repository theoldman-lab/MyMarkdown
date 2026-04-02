#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
from pathlib import Path

class MarkdownMerger:
    def __init__(self, verbose=False):
        self.verbose = verbose
        # 定义包含指令的正则模式：!include path/to/file.md
        self.include_pattern = re.compile(r'^!include\s+(.+?)\s*$', re.MULTILINE)
        # 定义 YAML Front Matter 模式：---\n...\n---
        self.front_matter_pattern = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)

    def log(self, message):
        if self.verbose:
            print(f"[INFO] {message}")

    def strip_front_matter(self, content):
        """
        移除文件顶部的 YAML Front Matter，避免合并后出现多个元数据块。
        """
        return self.front_matter_pattern.sub('', content, count=1)

    def resolve_path(self, current_file_path, include_path):
        """
        基于当前文件路径解析被包含文件的绝对路径。
        """
        current_dir = Path(current_file_path).parent
        resolved_path = (current_dir / include_path).resolve()
        return resolved_path

    def merge_file(self, file_path, visited=None, is_root=True):
        """
        递归合并文件内容。
        :param file_path: 当前文件路径
        :param visited: 已访问文件集合，防止循环引用
        :param is_root: 是否为主文件（主文件保留 Front Matter，子文件移除）
        """
        if visited is None:
            visited = set()

        abs_path = Path(file_path).resolve()

        if abs_path in visited:
            raise RecursionError(f"检测到循环引用：{abs_path}")
        visited.add(abs_path)

        self.log(f"正在处理：{abs_path}")

        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"无法找到文件：{abs_path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"文件编码错误，请确保为 UTF-8：{abs_path}")

        # 若非主文件，移除其 YAML Front Matter
        if not is_root:
            content = self.strip_front_matter(content)

        merged_content = []
        last_end = 0

        # 查找所有包含指令
        for match in self.include_pattern.finditer(content):
            # 添加指令之前的内容
            merged_content.append(content[last_end:match.start()])

            include_file_rel = match.group(1).strip()
            include_file_abs = self.resolve_path(abs_path, include_file_rel)

            if not include_file_abs.exists():
                raise FileNotFoundError(f"包含指令指向的文件不存在：{include_file_abs}")

            # 递归合并被包含文件
            sub_content = self.merge_file(include_file_abs, visited, is_root=False)
            merged_content.append(sub_content)

            last_end = match.end()

        # 添加剩余内容
        merged_content.append(content[last_end:])

        return ''.join(merged_content)

def main():
    parser = argparse.ArgumentParser(description="Markdown 模块化合并工具")
    parser.add_argument("input", help="主文件路径 (例如：main_source.md)")
    parser.add_argument("output", help="输出文件路径 (例如：main.md)")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细处理日志")

    args = parser.parse_args()

    merger = MarkdownMerger(verbose=args.verbose)

    try:
        final_content = merger.merge_file(args.input)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"成功：已合并至 {args.output}")

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
