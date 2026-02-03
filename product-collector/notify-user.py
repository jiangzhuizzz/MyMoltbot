#!/usr/bin/env python3
"""
通知用户系统
通过 WhatsApp 发送产品库更新通知
"""

import json
import sys
from pathlib import Path

def send_notification(event_type, data=None):
    """发送通知"""
    
    # 通知消息模板
    messages = {
        'pr_created': {
            'title': '📦 产品库 PR 已创建',
            'message': f'''GitHub Pull Request 已创建！

分支: `{data}`

请访问以下链接审核并合并:
https://github.com/jiangzhuizzz/MyMoltbot/pull/new/{data}

审核清单:
- [ ] 利率信息是否准确
- [ ] 申请条件是否完整
- [ ] 产品标签是否合适
- [ ] 数据来源是否注明

合并后产品库将自动更新！'''
        },
        
        'review_needed': {
            'title': '⚠️ 需要审核',
            'message': '''产品库有新的更新需要审核。

请查看 GitHub 上的 Pull Request。

审核通过后，数据会自动同步到产品库。'''
        },
        
        'data_updated': {
            'title': '✅ 产品数据已更新',
            'message': '''产品库已更新！

更新内容:
- 新增产品信息
- 更新利率数据
- 完善产品描述

详情请查看产品库文档。'''
        },
        
        'discussion': {
            'title': '💬 产品库完善讨论',
            'message': '''以下是一些产品库完善建议：

1. 📊 数据完整度
   - 当前有 XX 个产品，建议补充到 20+ 个

2. 🔄 数据更新
   - 上次更新：X天前
   - 建议检查最新利率

3. 🏦 合作银行
   - 是否需要添加新的银行？

请回复「讨论」获取详细建议。'''
        }
    }
    
    if event_type not in messages:
        print(f"❌ 未知事件类型: {event_type}")
        return False
    
    msg = messages[event_type]
    
    # 打印消息（实际发送由外部脚本处理）
    print(f"\n{'='*50}")
    print(f"{msg['title']}")
    print(f"{'='*50}")
    print(msg['message'])
    print(f"{'='*50}\n")
    
    # 标记事件（可以保存到文件供后续使用）
    state_file = Path("/home/codespace/clawd/product-collector/data/notification-state.json")
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text())
    
    state[event_type] = {
        'time': strftime('%Y-%m-%d %H:%M:%S'),
        'sent': True,
        'data': data
    }
    
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    
    return True

def strftime(format):
    from datetime import datetime
    return datetime.now().strftime(format)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: notify-user.py <事件类型> [数据]")
        print("事件类型: pr_created, review_needed, data_updated, discussion")
        sys.exit(1)
    
    event_type = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) > 2 else None
    
    send_notification(event_type, data)
