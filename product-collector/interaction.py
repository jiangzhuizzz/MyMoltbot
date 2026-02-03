#!/usr/bin/env python3
"""
产品库互动讨论系统
定期与用户讨论产品库完善
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class ProductInteraction:
    """产品库互动系统"""
    
    def __init__(self):
        self.data_dir = Path("/home/codespace/clawd/product-collector/data")
        self.data_dir.mkdir(exist_ok=True)
        self.state_file = self.data_dir / "interaction-state.json"
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if self.state_file.exists():
            self.state = json.loads(self.state_file.read_text())
        else:
            self.state = {
                'last_discussion': None,
                'pending_topics': [],
                'completed_topics': [],
                'suggestions': []
            }
    
    def save_state(self):
        """保存状态"""
        self.state_file.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def generate_suggestions(self):
        """生成完善建议"""
        suggestions = []
        
        # 检查产品完整度
        products_dir = Path("/workspaces/MyMoltbot/obsidian-templates/产品库")
        
        if products_dir.exists():
            # 统计产品数量
            product_files = list(products_dir.rglob("*.md"))
            total_products = len([f for f in product_files if not f.name.startswith("TEMPLATE")])
            
            # 检查是否有待审核文件
            pending_files = list(products_dir.rglob("*.new.md"))
            
            suggestions.append({
                'type': 'review',
                'title': '📦 待审核更新',
                'message': f'发现 {len(pending_files)} 个待审核的产品更新，请查看 PR',
                'priority': 'high',
                'action': 'review_pr'
            })
            
            suggestions.append({
                'type': 'completeness',
                'title': '📊 产品库完整度',
                'message': f'当前有 {total_products} 个产品，建议补充到 20+ 个主流产品',
                'priority': 'medium',
                'action': 'add_products'
            })
            
            # 检查数据新鲜度
            suggestions.append({
                'type': 'freshness',
                'title': '🔄 数据更新',
                'message': '建议每周检查一次产品利率变化',
                'priority': 'low',
                'action': 'update_rates'
            })
        
        return suggestions
    
    def get_discussion_topics(self):
        """获取讨论话题"""
        topics = []
        
        # 添加建议
        topics.extend(self.generate_suggestions())
        
        # 添加主动建议
        topics.extend([
            {
                'type': 'feature',
                'title': '🏦 新银行合作',
                'message': '是否需要添加新的合作银行？武汉地区可以关注：湖北银行、汉口银行等本地银行',
                'priority': 'medium',
                'action': 'discuss_bank'
            },
            {
                'type': 'feature',
                'title': '📱 公众号数据',
                'message': '可以定期从武汉本地贷款类公众号获取最新产品信息，是否需要设置自动采集？',
                'priority': 'medium',
                'action': 'discuss_wechat'
            },
            {
                'type': 'workflow',
                'title': '⚡ 自动化频率',
                'message': '当前每24小时检查一次更新，是否需要调整频率？',
                'priority': 'low',
                'action': 'discuss_frequency'
            }
        ])
        
        return topics
    
    def format_discussion_message(self):
        """格式化讨论消息"""
        topics = self.get_discussion_topics()
        
        message = "💬 **产品库完善讨论**\n\n"
        message += "以下是一些需要讨论或处理的事项：\n\n"
        
        for i, topic in enumerate(topics, 1):
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(topic.get('priority', 'low'), '⚪')
            
            message += f"{priority_emoji} **{topic['title']}**\n"
            message += f"   {topic['message']}\n\n"
        
        message += "---\n"
        message += "请回复对应的数字或标题，我会帮你处理：\n"
        message += "例如：回复「1」或「待审核更新」查看详情"
        
        return message
    
    def mark_discussed(self, topic_type):
        """标记已讨论"""
        if topic_type not in self.state['completed_topics']:
            self.state['completed_topics'].append(topic_type)
            self.state['last_discussion'] = datetime.now().isoformat()
            self.save_state()
    
    def should_remind(self):
        """是否需要提醒"""
        if not self.state['last_discussion']:
            return True
        
        last = datetime.fromisoformat(self.state['last_discussion'])
        # 每3天提醒一次
        return (datetime.now() - last).days >= 3

def main():
    interaction = ProductInteraction()
    
    if interaction.should_remind():
        message = interaction.format_discussion_message()
        print(message)
    else:
        print("⏭️ 距离上次讨论不足3天，暂不提醒")

if __name__ == '__main__':
    main()
