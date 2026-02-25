import marshal
import zlib
import base64
from datetime import datetime
import os


print("=" * 30)
print("靓仔牛逼天下第一！")
print("=" * 30)


source_path = input("请输入要加密的Python脚本完整路径：").strip()


if not os.path.exists(source_path):
    print(f"❌ 错误：文件 '{source_path}' 不存在！")
    input("按回车键退出...")
    exit(1)


try:
    with open(source_path, "r", encoding="utf-8") as f:
        core_code = f.read()
except Exception as e:
    print(f"❌ 读取源文件失败：{str(e)}")
    input("按回车键退出...")
    exit(1)


try:
    code_obj = compile(core_code, "<string>", "exec")
    compressed = zlib.compress(marshal.dumps(code_obj))
    encoded = base64.b64encode(compressed).decode('utf-8')
except Exception as e:
    print(f"❌ 加密过程出错：{str(e)}")
    input("按回车键退出...")
    exit(1)


beijing_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

encoded_bytes = encoded.encode('utf-8')
final_script = f'''#!/usr/bin/env python3
#靓仔牛逼
#加密时间{beijing_time}
import marshal
import zlib
import base64

def decrypt(code):
    decoded = base64.b64decode(code)
    decompressed = zlib.decompress(decoded)
    return marshal.loads(decompressed)

data = decrypt({repr(encoded_bytes)})
exec(data)
'''


original_filename = os.path.basename(source_path)
name, ext = os.path.splitext(original_filename)
new_filename = f"{name}_已加密{ext}"
final_save_path = os.path.join(os.path.dirname(source_path), new_filename)


try:
    with open(final_save_path, "w", encoding="utf-8") as f:
        f.write(final_script)
    print(f"\n🎉 加密成功！")
    print(f"📂 可执行文件路径：{final_save_path}")
except Exception as e:
    print(f"❌ 保存文件失败：{str(e)}")

input("\n按回车键退出...")
