import os
import json

# ================= 配置区 =================
DIR_A = "model_A_img"    # 模型 A 的文件夹名
DIR_B = "model_B_img"    # 模型 B 的文件夹名
DIR_REF = "ref_img"      # 参考图文件夹名 (如果没有参考图，保持原样即可)
OUTPUT_FILE = "config.json"
# ==========================================

def get_images_in_dir(directory):
    """获取目录下的所有图片，返回相对于根目录的路径（强制使用正斜杠 /）"""
    if not os.path.exists(directory):
        return []
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')
    images = []
    for file in os.listdir(directory):
        if file.lower().endswith(valid_exts):
            # 构建相对路径，并将 Windows 的 \ 替换为 Web 统一的 /
            path = os.path.join(directory, file).replace("\\", "/")
            images.append(path)
    return sorted(images)

def main():
    if not os.path.exists(DIR_A) or not os.path.exists(DIR_B):
        print(f"错误: 找不到 {DIR_A} 或 {DIR_B} 文件夹，请检查路径。")
        return

    # 获取 A 和 B 共有的子文件夹（组）
    subfolders_a = set(f for f in os.listdir(DIR_A) if os.path.isdir(os.path.join(DIR_A, f)))
    subfolders_b = set(f for f in os.listdir(DIR_B) if os.path.isdir(os.path.join(DIR_B, f)))
    common_folders = sorted(list(subfolders_a & subfolders_b))

    groups = []
    for folder in common_folders:
        path_a = os.path.join(DIR_A, folder)
        path_b = os.path.join(DIR_B, folder)
        path_ref = os.path.join(DIR_REF, folder)

        files_a = get_images_in_dir(path_a)
        files_b = get_images_in_dir(path_b)
        files_ref = get_images_in_dir(path_ref)

        groups.append({
            "folder": folder,
            "filesA": files_a,
            "filesB": files_b,
            "filesRef": files_ref
        })

    config = {"groups": groups}

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"成功！已将 {len(groups)} 组数据写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
