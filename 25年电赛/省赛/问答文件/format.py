import sys

def add_blank_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line.rstrip('\n'))
        # 判断本行是否为答：开头
        if line.strip().startswith('答：') or line.strip().startswith('    答：') or line.strip().startswith('   答：'):
            # 如果下一行不是空行且不是文件结尾，则插入空行
            if i + 1 < len(lines) and lines[i+1].strip() != '':
                new_lines.append('')

    # 写回文件（可自行修改为写入新文件）
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python add_blank_line.py 文件路径')
    else:
        add_blank_lines(sys.argv[1])
        print('处理完成！')