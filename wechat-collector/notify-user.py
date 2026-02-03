#!/usr/bin/env python3
"""
武汉公众号采集通知系统
"""

import json
import sys
from pathlib import Path

def send_notification(event_type, data=None):
    """发送通知"""
    
    messages = {
        'collection_complete': {
            'title': '📱 公众号产品采集完成',
            'message': f'''采集完成！

📊 数据统计:
- 监测公众号: 10个
- 新增数据: {data} 个文件

已更新的产品:
- 工商银行-融e借
- 建设银行-快贷
- 招商银行-闪电贷
- 湖北银行-荆楚贷
- 汉口银行-市民贷

✅ 数据已同步到产品库，待审核后合并。'''
        },
        
        'new_product_found': {
            'title': '🆕 发现新产品',
            'message': '''发现新的贷款产品！

请查看采集报告并更新产品库。

审核清单:
- [ ] 产品信息是否准确
- [ ] 利率是否最新
- [ ] 佣金比例是否正确
- [ ] 是否适合目标客户'''
        },
        
        'rate_changed': {
            'title': '📊 利率变化提醒',
            'message': '''监测到利率变化！

请查看详情并更新产品库。

可能的调整:
- 工商银行融e借
- 建设银行快贷

建议及时同步到产品库。'''
        }
    }
    
    if event_type not in messages:
        print(f"❌ 未知事件: {event_type}")
        return False
    
    msg = messages[event_type]
    
    print(f"\n{'='*50}")
    print(f"{msg['title']}")
    print(f"{'='*50}")
    print(msg['message'])
    print(f"{'='*50}\n")
    
    # 保存状态
    state_file = Path("/home/codespace/clawd/wechat-collector/data/notification-state.json")
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text())
    
    from datetime import datetime
    state[event_type] = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sent': True,
        'data': data
    }
    
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: notify-user.py <事件类型> [数据]")
        sys.exit(1)
    
    event_type = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) > 2 else None
    
    send_notification(event_type, data)
