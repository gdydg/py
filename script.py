# 文件名: script.py
import xxtea
import base64
import urllib.parse

print("🚀 正在启动云端解密引擎...")

# 你要解密的密文（后续如果有新的，直接在这里改）
target_id = "DXvG/5lQl2ZwU2rB7IC6nMvUY++TC2wraCZIWqxUzRkmpbk7bUaGsyFqYn+qI/fiSvFZC6kdBY71QV2IlGNPzIjid7gmc801qnOTZDHGw4KccS/VNCeTJD4snsQD68C+0PqaoEf30tb4LA1YUvNgV0rCHiw="

# 咱们扒出来的万能密钥
target_key = "ABCDEFGHIJKLMNOPQRSTUVWX"

try:
    # 1. URL解码 + Base64解码
    encrypted_bytes = base64.b64decode(urllib.parse.unquote(target_id))
    
    # 2. XXTEA解密
    decrypted_bytes = xxtea.decrypt(encrypted_bytes, target_key.encode('utf-8'))
    
    if decrypted_bytes:
        print("-" * 40)
        print("🎬 解密成功！真实结果如下：")
        print(decrypted_bytes.decode('utf-8'))
        print("-" * 40)
    else:
        print("❌ 解密失败，请检查密文或密钥是否完整。")

except Exception as e:
    print(f"❌ 运行报错了: {e}")
