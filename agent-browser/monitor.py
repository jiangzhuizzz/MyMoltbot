#!/usr/bin/env python3
"""
网页监控脚本
定期检查目标页面是否有更新
"""

import json
import time
from pathlib import Path
from datetime import datetime
from automate import BrowserAgent

# 配置
DATA_DIR = Path("/home/codespace/clawd/agent-browser/data")
LOG_DIR = Path("/home/codespace/clawd/agent-browser/logs")
CONFIG_DIR = Path("/home/codespace/clawd/agent-browser/config")

class PageMonitor:
    """页面监控器"""
    
    def __init__(self):
        self.agent = BrowserAgent()
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        config_file = CONFIG_DIR / "targets.json"
        if config_file.exists():
            self.config = json.loads(config_file.read_text(encoding='utf-8'))
        else:
            self.config = {"targets": []}
    
    def log(self, message):
        """日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        LOG_DIR.joinpath('monitor.log').write_text(
            LOG_DIR.joinpath('monitor.log').read_text() + log_line,
            encoding='utf-8'
        )
        print(message)
    
    def check_target(self, target):
        """检查单个目标"""
        name = target.get('name', '未命名')
        url = target.get('url')
        selectors = target.get('selectors', {})
        check_interval = target.get('check_interval', 3600)
        
        self.log(f"🔍 检查: {name} ({url})")
        
        try:
            # 启动浏览器
            self.agent.start(headless=True)
            
            # 访问页面
            self.agent.goto(url)
            
            # 提取数据
            data = self.agent.extract(selectors)
            self.log(f"📊 数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 保存快照
            snapshot_name = f"snapshot_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.agent.screenshot(snapshot_name)
            
            # 更新状态
            status_file = DATA_DIR / "status.json"
            status = {}
            if status_file.exists():
                status = json.loads(status_file.read_text(encoding='utf-8'))
            
            status[name] = {
                'url': url,
                'last_check': datetime.now().isoformat(),
                'data': data,
                'status': 'ok'
            }
            
            status_file.write_text(
                json.dumps(status, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            
            self.log(f"✅ {name} 检查完成")
            
        except Exception as e:
            self.log(f"❌ {name} 检查失败: {e}")
            
            # 更新错误状态
            status_file = DATA_DIR / "status.json"
            status = {}
            if status_file.exists():
                status = json.loads(status_file.read_text(encoding='utf-8'))
            
            status[name] = {
                'url': url,
                'last_check': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
            
            status_file.write_text(
                json.dumps(status, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        
        finally:
            self.agent.close()
        
        return data
    
    def check_all(self):
        """检查所有目标"""
        self.log("🚀 开始页面监控...")
        
        targets = self.config.get('targets', [])
        
        for target in targets:
            if target.get('enabled', True):
                self.check_target(target)
                time.sleep(2)  # 间隔2秒
        
        self.log(f"✅ 完成 {len(targets)} 个目标检查")
        
        # 显示状态
        status_file = DATA_DIR / "status.json"
        if status_file.exists():
            status = json.loads(status_file.read_text(encoding='utf-8'))
            print("\n📊 监控状态:")
            for name, info in status.items():
                status_icon = "✅" if info.get('status') == 'ok' else "❌"
                last_check = info.get('last_check', '未知')[:16]
                print(f"  {status_icon} {name}: {last_check}")
    
    def run_loop(self):
        """持续监控循环"""
        self.log("🔄 启动持续监控...")
        
        while True:
            self.check_all()
            self.log(f"💤 等待 1 小时后再次检查...")
            time.sleep(3600)  # 每小时检查一次


def main():
    """主函数"""
    import sys
    
    monitor = PageMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        # 持续监控
        monitor.run_loop()
    else:
        # 单次检查
        monitor.check_all()


if __name__ == '__main__':
    main()
