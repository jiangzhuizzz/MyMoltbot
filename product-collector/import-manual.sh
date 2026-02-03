#!/bin/bash
# 产品手册导入脚本
# 将PDF/Word/Excel格式的产品手册导入到产品库

MANUAL_DIR="/home/codespace/clawd/product-collector/manuals"
OUTPUT_DIR="/workspaces/MyMoltbot/obsidian-templates/产品库"
DATA_DIR="/home/codespace/clawd/product-collector/data"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 创建目录
mkdir -p "$MANUAL_DIR" "$OUTPUT_DIR/待审核" "$DATA_DIR"

log "📁 产品手册导入工具"
log ""
echo "支持的格式:"
echo "  - PDF (.pdf)"
echo "  - Word (.docx)"
echo "  - Excel (.xlsx, .xls)"
echo "  - Markdown (.md)"
echo "  - JSON (.json)"
echo "  - CSV (.csv)"
echo ""

# 检查文件
if [ $# -eq 0 ]; then
    echo "用法: $0 <文件路径>"
    echo ""
    echo "示例:"
    echo "  $0 ./产品手册.pdf"
    echo "  $0 ./bank_products.xlsx"
    echo "  $0 ./产品数据.json"
    echo ""
    echo "📂 手册存放目录: $MANUAL_DIR"
    echo "   将文件放入此目录，然后运行: $0 --dir"
    
    # 显示目录中的文件
    if [ "$(ls -A $MANUAL_DIR 2>/dev/null)" ]; then
        echo ""
        echo "发现以下手册文件:"
        ls -lh "$MANUAL_DIR"
    fi
    exit 0
fi

# 处理参数
if [ "$1" = "--dir" ]; then
    log "📂 处理目录中的所有文件..."
    FILES=$(find "$MANUAL_DIR" -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.xlsx" -o -name "*.xls" -o -name "*.md" -o -name "*.json" -o -name "*.csv" \) 2>/dev/null)
else
    FILES="$1"
fi

# 处理每个文件
for file in $FILES; do
    log "📄 处理文件: $file"
    
    EXT="${file##*.}"
    BASENAME=$(basename "$file" ".$EXT")
    
    case "$EXT" in
        pdf)
            log "  📄 PDF文件: $BASENAME.pdf"
            log "  💡 提示: PDF需要手动提取内容，或使用OCR工具"
            # 创建占位符，实际需要人工处理
            cat > "$OUTPUT_DIR/待审核/${BASENAME}_导入说明.md" << EOF
---
title: $BASENAME
type: 导入手册
status: 待处理
source: PDF手册
importDate: $(date '+%Y-%m-%d')
---

# $BASENAME

## 导入说明

此产品数据来自PDF手册：\`$file\`

### 待处理事项

- [ ] 提取产品信息
- [ ] 整理数据格式
- [ ] 转换为标准模板
- [ ] 审核并合并

### 原始文件

- 路径: $file
- 大小: $(ls -lh "$file" | awk '{print $5}')
- 导入时间: $(date '+%Y-%m-%d %H:%M')

---

请手动提取PDF内容并整理为标准格式。
EOF
            ;;
        
        docx)
            log "  📄 Word文件: $BASENAME.docx"
            # 需要 python-docx 库处理
            python3 -c "
import docx
doc = docx.Document('$file')
text = '\\n'.join([p.text for p in doc.paragraphs])
print('  内容预览:', text[:200])
" 2>/dev/null || log "  💡 需要安装 python-docx 库处理Word文件"
            ;;
        
        xlsx|xls)
            log "  📊 Excel文件: $BASENAME.$EXT"
            # 处理Excel
            python3 << PYEOF
import pandas as pd
try:
    df = pd.read_excel('$file')
    print(f'  找到 {len(df)} 行数据')
    print(f'  列名: {list(df.columns)}')
    
    # 保存为JSON
    output = df.to_dict('records')
    import json
    with open('$DATA_DIR/${BASENAME}.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f'  已保存到: $DATA_DIR/${BASENAME}.json')
except Exception as e:
    print(f'  处理失败: {e}')
PYEOF
            ;;
        
        csv)
            log "  📊 CSV文件: $BASENAME.csv"
            python3 << PYEOF
import pandas as pd
try:
    df = pd.read_csv('$file')
    print(f'  找到 {len(df)} 行数据')
    print(f'  列名: {list(df.columns)}')
except Exception as e:
    print(f'  处理失败: {e}')
PYEOF
            ;;
        
        md)
            log "  📝 Markdown文件: $BASENAME.md"
            # 直接复制到待审核
            cp "$file" "$OUTPUT_DIR/待审核/${BASENAME}.md"
            log "  ✅ 已复制到待审核目录"
            ;;
        
        json)
            log "  📋 JSON文件: $BASENAME.json"
            python3 << PYEOF
import json
with open('$file', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
if isinstance(data, list):
    print(f'  找到 {len(data)} 条记录')
    if len(data) > 0:
        print(f'  示例字段: {list(data[0].keys())[:5]}')
elif isinstance(data, dict):
    print(f'  包含字段: {list(data.keys())}')
EOF
            ;;
        
        *)
            log "  ⚠️ 不支持的格式: $EXT"
            continue
            ;;
    esac
    
    log "  ✅ 处理完成: $file"
done

log ""
log "📦 下一步操作："
log "  1. 检查待审核目录: $OUTPUT_DIR/待审核/"
log "  2. 审核并转换格式"
log "  3. 运行 git-workflow.sh 创建 PR"
