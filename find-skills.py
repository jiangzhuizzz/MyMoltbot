#!/usr/bin/env python3
"""
技能发现和推荐系统
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置
SKILLS_DIR = Path("/usr/local/share/nvm/versions/node/v24.11.1/lib/node_modules/clawdbot/skills")
RECOMMENDATIONS_DIR = Path("/home/codespace/clawd/skill-recommendations")

class SkillFinder:
    """技能发现器"""
    
    def __init__(self):
        self.skills = self.load_all_skills()
        self.load_preferences()
    
    def load_all_skills(self):
        """加载所有技能"""
        skills = {}
        
        for skill_path in SKILLS_DIR.iterdir():
            if skill_path.is_dir():
                skill_file = skill_path / "SKILL.md"
                if skill_file.exists():
                    skill_info = self.parse_skill_file(skill_file)
                    skill_info['path'] = str(skill_path)
                    skill_info['name'] = skill_path.name
                    skills[skill_path.name] = skill_info
        
        return skills
    
    def parse_skill_file(self, file_path):
        """解析 SKILL.md 文件"""
        content = file_path.read_text(encoding='utf-8')
        
        # 提取 frontmatter
        import re
        frontmatter = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        
        info = {
            'name': '',
            'description': '',
            'emoji': '📦',
            'installed': True
        }
        
        if frontmatter:
            yaml_content = frontmatter.group(1)
            
            # 提取 name
            name_match = re.search(r'name:\s*(\S+)', yaml_content)
            if name_match:
                info['name'] = name_match.group(1)
            
            # 提取 description
            desc_match = re.search(r'description:\s*(.+)', yaml_content)
            if desc_match:
                info['description'] = desc_match.group(1).strip()
            
            # 提取 emoji
            emoji_match = re.search(r'emoji:\s*(\S+)', yaml_content)
            if emoji_match:
                info['emoji'] = emoji_match.group(1)
        
        # 提取 homepage
        homepage_match = re.search(r'homepage:\s*(.+)', content)
        if homepage_match:
            info['homepage'] = homepage_match.group(1).strip()
        
        return info
    
    def load_preferences(self):
        """加载用户偏好"""
        pref_file = RECOMMENDATIONS_DIR / "preferences.json"
        if pref_file.exists():
            self.preferences = json.loads(pref_file.read_text(encoding='utf-8'))
        else:
            self.preferences = {
                'job': '贷款中介',
                'location': '武汉',
                'interests': [],
                'installed_skills': [],
                'recommended_skills': []
            }
            self.save_preferences()
    
    def save_preferences(self):
        """保存用户偏好"""
        pref_file = RECOMMENDATIONS_DIR / "preferences.json"
        pref_file.write_text(
            json.dumps(self.preferences, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def list_skills(self, detailed=False, by_category=False):
        """列出所有技能"""
        print(f"\n{'='*60}")
        print("    🔍 Clawdbot 技能列表")
        print(f"{'='*60}\n")
        
        if by_category:
            # 按分类显示
            categories = {}
            for name, skill in self.skills.items():
                category = skill.get('category', '其他')
                if category not in categories:
                    categories[category] = []
                categories[category].append(skill)
            
            for category, skills_list in categories.items():
                print(f"\n📁 {category}")
                print("-" * 40)
                for skill in skills_list:
                    self.print_skill_brief(skill)
        else:
            for name, skill in self.skills.items():
                if detailed:
                    self.print_skill_detailed(name, skill)
                else:
                    self.print_skill_brief(skill)
        
        print(f"\n总计: {len(self.skills)} 个技能\n")
    
    def print_skill_brief(self, skill):
        """打印简要技能信息"""
        emoji = skill.get('emoji', '📦')
        name = skill.get('name', '')
        description = skill.get('description', '')[:50]
        
        print(f"  {emoji} {name}")
        print(f"     {description}...")
        print()
    
    def print_skill_detailed(self, name, skill):
        """打印详细技能信息"""
        emoji = skill.get('emoji', '📦')
        
        print(f"{'='*60}")
        print(f"  {emoji} {name}")
        print(f"{'='*60}\n")
        print(f"描述: {skill.get('description', '无')}")
        print(f"路径: {skill.get('path', '未知')}")
        print(f"主页: {skill.get('homepage', '无')}")
        print()
    
    def search_skills(self, keywords):
        """搜索技能"""
        print(f"\n{'='*60}")
        print(f"    🔍 搜索关键词: {' '.join(keywords)}")
        print(f"{'='*60}\n")
        
        results = []
        
        for name, skill in self.skills.items():
            # 检查名称
            name_match = any(kw.lower() in name.lower() for kw in keywords)
            
            # 检查描述
            desc = skill.get('description', '').lower()
            desc_match = any(kw.lower() in desc for kw in keywords)
            
            if name_match or desc_match:
                results.append(skill)
        
        if results:
            print(f"找到 {len(results)} 个相关技能:\n")
            for skill in results:
                self.print_skill_brief(skill)
        else:
            print("未找到相关技能")
            print("\n建议:")
            print("  - 检查关键词拼写")
            print("  - 使用更通用的关键词")
            print("  - 浏览所有技能: clawdbot skill list")
        print()
    
    def recommend_skills(self, job=None, need=None, refresh=False):
        """推荐技能"""
        if job is None:
            job = self.preferences.get('job', '贷款中介')
        
        print(f"\n{'='*60}")
        print(f"    💡 为 {job} 推荐的技能")
        print(f"{'='*60}\n")
        
        # 评分系统
        scores = {}
        
        # 关键词匹配
        keywords = {
            '贷款中介': ['daily-report', 'product-collector', 'wechat-collector', 'social-trends'],
            '自媒体运营': ['daily-report', 'social-trends', 'agent-browser'],
            '产品经理': ['product-collector', 'agent-browser', 'data-analysis'],
            '销售': ['daily-report', 'product-collector', 'client-tracker']
        }
        
        if job in keywords:
            for skill_name in keywords[job]:
                if skill_name in self.skills:
                    scores[skill_name] = 90
        
        # 检查已安装的技能
        installed = self.preferences.get('installed_skills', [])
        for skill in installed:
            if skill in self.skills and skill not in scores:
                scores[skill] = 70
        
        # 排序
        sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_skills:
            print("推荐技能（按匹配度排序）:\n")
            
            for i, (skill_name, score) in enumerate(sorted_skills[:10], 1):
                skill = self.skills.get(skill_name)
                if skill:
                    emoji = skill.get('emoji', '📦')
                    print(f"  {i}. {emoji} {skill_name}")
                    print(f"     匹配度: {'⭐' * (score // 20)} ({score}%)")
                    print(f"     {skill.get('description', '')[:60]}...")
                    print()
        else:
            print("未找到匹配的技能")
            print("\n建议尝试:")
            print("  - clawdbot skill list 查看所有技能")
            print("  - clawdbot skill search <关键词> 搜索特定技能")
        print()
    
    def show_skill(self, name, full=False, examples=False):
        """显示技能详情"""
        if name not in self.skills:
            print(f"\n❌ 技能不存在: {name}")
            print(f"\n可用技能: {', '.join(self.skills.keys())}\n")
            return
        
        skill = self.skills[name]
        
        print(f"\n{'='*60}")
        print(f"  {skill.get('emoji', '📦')} {name}")
        print(f"{'='*60}\n")
        print(f"描述: {skill.get('description', '无')}")
        print(f"路径: {skill.get('path', '未知')}")
        
        if full:
            print(f"主页: {skill.get('homepage', '无')}")
            print()
            
            # 显示使用示例
            skill_file = Path(skill.get('path', '')) / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text(encoding='utf-8')
                
                # 查找使用示例
                import re
                examples_section = re.search(r'## 使用方法\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
                if examples_section:
                    print("使用方法:")
                    print("-" * 40)
                    print(examples_section.group(1))
        print()
    
    def update_preferences(self, **kwargs):
        """更新用户偏好"""
        for key, value in kwargs.items():
            if key in self.preferences:
                self.preferences[key] = value
        
        self.save_preferences()
        print(f"\n✅ 偏好已更新: {kwargs}\n")


def main():
    """主函数"""
    finder = SkillFinder()
    
    # 解析参数
    if len(sys.argv) < 2:
        # 默认显示推荐
        finder.recommend_skills()
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        detailed = '--detailed' in sys.argv or '-d' in sys.argv
        by_category = '--by-category' in sys.argv or '-c' in sys.argv
        finder.list_skills(detailed=detailed, by_category=by_category)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("\n❌ 请指定搜索关键词")
            print("用法: clawdbot skill search <关键词>\n")
            return
        keywords = sys.argv[2:]
        finder.search_skills(keywords)
    
    elif command == 'recommend':
        job = None
        need = None
        refresh = '--refresh' in sys.argv or '-r' in sys.argv
        
        # 解析参数
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == '--job' and i + 1 < len(sys.argv):
                job = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == '--need' and i + 1 < len(sys.argv):
                need = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        finder.recommend_skills(job=job, need=need, refresh=refresh)
    
    elif command == 'show':
        if len(sys.argv) < 3:
            print("\n❌ 请指定技能名称")
            print("用法: clawdbot skill show <技能名>\n")
            return
        name = sys.argv[2]
        full = '--full' in sys.argv
        examples = '--examples' in sys.argv
        finder.show_skill(name, full=full, examples=examples)
    
    elif command == 'preferences':
        if len(sys.argv) < 3:
            print("\n❌ 请指定操作")
            print("用法: clawdbot skill preferences --update --job <工作>\n")
            return
        
        kwargs = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == '--job' and i + 1 < len(sys.argv):
                kwargs['job'] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == '--location' and i + 1 < len(sys.argv):
                kwargs['location'] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == '--update':
                i += 1
            else:
                i += 1
        
        if kwargs:
            finder.update_preferences(**kwargs)
    
    elif command == 'help':
        print("""
🔍 Clawdbot 技能管理命令

用法:
  clawdbot skill <命令> [选项]

命令:
  list                  列出所有技能
  list --detailed       显示详细信息
  list --by-category    按分类显示
  
  search <关键词>       搜索技能
  search loan wechat    搜索多个关键词
  
  recommend             获取推荐
  recommend --job 贷款中介   指定工作类型
  
  show <技能名>         显示技能详情
  show daily-report --full   显示完整文档
  
  preferences           管理用户偏好
  preferences --job 贷款中介   更新偏好

示例:
  clawdbot skill list
  clawdbot skill search loan
  clawdbot skill recommend --job 贷款中介
  clawdbot skill show daily-report --full
""")
    
    else:
        print(f"\n❌ 未知命令: {command}")
        print("用法: clawdbot skill help\n")


if __name__ == '__main__':
    main()
