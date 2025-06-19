import os
import re
from pathlib import Path

PROJECT_TITLE = "# 🤖 Brotherhood of Artificial Intelligence\n\n" \
"""<p align="center">
  <a href="https://github.com/ZPJ-LEFT">
    <img src="https://github.com/ZPJ-LEFT.png?size=120" width="120" alt="Pengjie Zhang">
  </a>
</p>

<p align="center">
  <strong>「研究论文千千万，<a href="https://github.com/ZPJ-LEFT">Zhang Pengjie</a> 帮你筛出精华款。」</strong>
</p>

---

## ✨ 项目简介

这是由我们队内 **学术特工** 每周精选多模态 & AI 领域 **高质量论文** 的分享仓库。  
让你在茫茫论文海中 **少走弯路、节省时间、聚焦精华**。

## 论文索引

"""

def extract_paper_titles(week_readme_path):
    """从每周 README.md 中提取论文名称和 PDF 链接"""
    papers = []
    if not os.path.exists(week_readme_path):
        return papers
    with open(week_readme_path, encoding="utf-8") as f:
        content = f.read()
    # 匹配形如 ## [论文名](xxx.pdf)
    for match in re.finditer(r'## \[([^\]]+)\]\(([^)]+\.pdf)\)', content):
        title, pdf_link = match.group(1), match.group(2)
        papers.append((title, pdf_link))
    return papers

def main():
    weekly_dir = Path("Weekly_upload")
    weeks = sorted([d for d in weekly_dir.iterdir() if d.is_dir()],
                   key=lambda x: int(re.search(r'Week_(\d+)', x.name).group(1)) if re.search(r'Week_(\d+)', x.name) else 0)
    readme_lines = [PROJECT_TITLE]

    for week in weeks:
        week_num = re.search(r'Week_(\d+)', week.name)
        week_title = f"### {week.name.replace('_', ' ')}" if week_num else f"### {week.name}"
        week_readme_rel = f"{week}/README.md"
        readme_lines.append(f"{week_title}\n")
        readme_lines.append(f"- 📄 [本周论文详情]({week_readme_rel})")
        papers = extract_paper_titles(week_readme_rel)
        for title, pdf_link in papers:
            readme_lines.append(f"  - [{title}]({week}/{pdf_link})")
        readme_lines.append("")  # 空行

    with open("README.md", "w", encoding="utf-8") as f:
        f.write('\n'.join(readme_lines))

    print("✅ 项目总 README.md 已自动更新。")

if __name__ == "__main__":
    main()