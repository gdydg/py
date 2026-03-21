import xxtea
import json
import base64
import urllib.parse
import urllib.request

print("🚀 开始从远程接口拉取密文并进行批量云端解密...\n")

# 1. 配置接口地址和万能密钥
api_url = "https://raw.githubusercontent.com/gdydg/py/refs/heads/main/ww.txt"
target_key = "ABCDEFGHIJKLMNOPQRSTUVWX"

try:
    # --- 第一步：从网络接口拉取加密数据 ---
    print(f"📡 正在请求接口: {api_url}")
    # 伪装成浏览器访问，防止被简单的反爬虫拦截
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        
    # 将拉取到的多行文本，按换行符劈开，存进列表（同时去掉空行）
    target_ids = [line.strip() for line in content.split('\n') if line.strip()]
    
    print(f"✅ 成功拉取到 {len(target_ids)} 条加密视频流！\n")
    print("-" * 60)

    # --- 第二步：遍历列表，挨个解密 ---
    for i, encrypted_id in enumerate(target_ids, 1):
        try:
            # URL解码
            decoded_id = urllib.parse.unquote(encrypted_id)
            
            # 补全 Base64 尾部的等号
            padding = 4 - (len(decoded_id) % 4)
            if padding != 4:
                decoded_id += "=" * padding

            # Base64解码 -> XXTEA解密
            encrypted_bytes = base64.b64decode(decoded_id)
            decrypted_bytes = xxtea.decrypt(encrypted_bytes, target_key.encode('utf-8'))
            
            if decrypted_bytes:
                # 转成字符串并解析 JSON
                json_str = decrypted_bytes.decode('utf-8')
                data = json.loads(json_str)
                
                # 提取干净的 url (json.loads 会自动把 \/ 变回 /)
                real_url = data.get('url', '未找到URL')
                
                print(f"✅ 视频 {i}: {real_url}")
            else:
                print(f"❌ 视频 {i}: 解密失败，密钥错误或密文损坏。")

        except Exception as e:
            print(f"⚠️ 视频 {i}: 解析出错 -> {e}")

    print("-" * 60)
    print("🎉 批量拉取与解密任务全部执行完毕！")

except Exception as e:
    print(f"💥 致命错误：无法访问接口或读取数据 -> {e}")
