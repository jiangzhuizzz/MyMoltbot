#!/usr/bin/env python3
"""
浏览器自动化核心模块
基于 Playwright 实现浏览器控制和网页操作
"""

import json
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import pyautogui
import pyperclip

# 配置
DATA_DIR = Path("/home/codespace/clawd/agent-browser/data")
LOG_DIR = Path("/home/codespace/clawd/agent-browser/logs")
CONFIG_DIR = Path("/home/codespace/clawd/agent-browser/config")

class BrowserAgent:
    """浏览器自动化代理"""
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.history = []
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        config_file = CONFIG_DIR / "targets.json"
        if config_file.exists():
            self.config = json.loads(config_file.read_text(encoding='utf-8'))
        else:
            self.config = {
                "targets": [],
                "settings": {
                    "headless": True,
                    "timeout": 30000,
                    "screenshot_dir": str(DATA_DIR / "snapshots")
                }
            }
    
    def log(self, message):
        """日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        LOG_DIR.joinpath('automation.log').write_text(
            LOG_DIR.joinpath('automation.log').read_text() + log_line,
            encoding='utf-8'
        )
        print(message)
    
    def start(self, headless=True):
        """启动浏览器"""
        self.log("🚀 启动浏览器...")
        
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.get('settings', {}).get('timeout', 30000))
        
        self.log("✅ 浏览器启动成功")
        return self
    
    def goto(self, url, wait_until='networkidle'):
        """访问页面"""
        self.log(f"🌐 访问: {url}")
        self.page.goto(url, wait_until=wait_until)
        time.sleep(2)  # 等待加载
        return self
    
    def click(self, selector, timeout=10000):
        """点击元素"""
        self.log(f"🖱️ 点击: {selector}")
        self.page.click(selector, timeout=timeout)
        time.sleep(1)
        return self
    
    def fill(self, selector, text):
        """填写表单"""
        self.log(f"⌨️ 填写: {selector} = {text}")
        self.page.fill(selector, text)
        return self
    
    def type(self, selector, text, delay=100):
        """输入文本"""
        self.log(f"⌨️ 输入: {selector}")
        self.page.type(selector, text, delay=delay)
        return self
    
    def extract(self, selectors):
        """提取数据"""
        self.log("📊 提取数据...")
        
        result = {}
        for key, selector in selectors.items():
            try:
                element = self.page.query_selector(selector)
                if element:
                    result[key] = element.text_content().strip()
                else:
                    result[key] = None
            except Exception as e:
                self.log(f"  ⚠️ 提取失败 {key}: {e}")
                result[key] = None
        
        return result
    
    def extract_all(self, selector, fields):
        """批量提取列表数据"""
        self.log(f"📊 批量提取: {selector}")
        
        elements = self.page.query_selector_all(selector)
        results = []
        
        for i, elem in enumerate(elements):
            item = {}
            for field, field_selector in fields.items():
                try:
                    sub_elem = elem.query_selector(field_selector)
                    item[field] = sub_elem.text_content().strip() if sub_elem else None
                except:
                    item[field] = None
            results.append(item)
        
        return results
    
    def screenshot(self, name=None):
        """截图"""
        if name is None:
            name = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        screenshot_dir = Path(self.config.get('settings', {}).get('screenshot_dir', str(DATA_DIR / 'snapshots')))
        screenshot_dir.mkdir(exist_ok=True)
        
        filepath = screenshot_dir / f"{name}.png"
        self.page.screenshot(path=str(filepath))
        self.log(f"📸 截图: {filepath}")
        
        return str(filepath)
    
    def save_html(self, name=None):
        """保存HTML"""
        if name is None:
            name = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        html_dir = DATA_DIR / "html"
        html_dir.mkdir(exist_ok=True)
        
        filepath = html_dir / f"{name}.html"
        filepath.write_text(self.page.content(), encoding='utf-8')
        self.log(f"💾 HTML: {filepath}")
        
        return str(filepath)
    
    def scroll(self, direction='down', times=1):
        """滚动页面"""
        for _ in range(times):
            if direction == 'down':
                self.page.evaluate('window.scrollBy(0, 500)')
            else:
                self.page.evaluate('window.scrollBy(0, -500)')
            time.sleep(0.5)
        return self
    
    def wait(self, seconds):
        """等待"""
        time.sleep(seconds)
        return self
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            self.playwright.stop()
            self.log("👋 浏览器已关闭")
    
    def monitor_page(self, url, selectors, check_interval=3600):
        """监控页面变化"""
        self.log(f"🔍 开始监控: {url}")
        
        # 访问页面
        self.goto(url)
        
        # 获取初始内容
        initial_content = self.page.content()
        self.save_html(f"initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # 等待检查
        self.log(f"💤 等待 {check_interval} 秒后检查...")
        time.sleep(check_interval)
        
        # 重新访问
        self.goto(url)
        new_content = self.page.content()
        
        # 比较变化
        if initial_content != new_content:
            self.log("⚠️ 检测到页面变化！")
            self.screenshot(f"change_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.save_html(f"change_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # 提取新数据
            data = self.extract(selectors)
            self.log(f"📊 新数据: {data}")
            
            # 保存变更记录
            change_file = DATA_DIR / "changes" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            change_file.parent.mkdir(exist_ok=True)
            change_file.write_text(
                json.dumps({
                    'url': url,
                    'time': datetime.now().isoformat(),
                    'data': data
                }, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
        else:
            self.log("✅ 无变化")
        
        return self
    
    def run_task(self, task_config):
        """执行任务"""
        self.log(f"🎯 执行任务: {task_config.get('name', '未命名')}")
        
        try:
            # 启动浏览器
            self.start(headless=task_config.get('headless', True))
            
            # 执行步骤
            for step in task_config.get('steps', []):
                action = step.get('action')
                
                if action == 'goto':
                    self.goto(step.get('url'))
                elif action == 'click':
                    self.click(step.get('selector'))
                elif action == 'fill':
                    self.fill(step.get('selector'), step.get('text'))
                elif action == 'wait':
                    self.wait(step.get('seconds', 1))
                elif action == 'scroll':
                    self.scroll(step.get('direction', 'down'), step.get('times', 1))
                elif action == 'screenshot':
                    self.screenshot(step.get('name'))
                elif action == 'extract':
                    result = self.extract(step.get('selectors'))
                    self.log(f"📊 提取结果: {result}")
                    self.history.append({'action': 'extract', 'result': result})
            
            self.log("✅ 任务完成")
            
        except Exception as e:
            self.log(f"❌ 任务失败: {e}")
            self.screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        finally:
            self.close()
        
        return self.history


def main():
    """主函数 - 运行配置中的任务"""
    agent = BrowserAgent()
    
    # 加载配置
    config_file = CONFIG_DIR / "targets.json"
    if not config_file.exists():
        print("❌ 配置文件不存在: targets.json")
        return
    
    config = json.loads(config_file.read_text(encoding='utf-8'))
    
    # 运行每个目标
    for target in config.get('targets', []):
        if target.get('enabled', True):
            agent.run_task(target)


if __name__ == '__main__':
    main()
