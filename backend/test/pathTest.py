import os
from backend import Config  # 替换为你的 Config 类的实际导入路径

def write_file_to_upload_dir(filename, content):
    # 获取文件上传目录
    upload_dir = Config.FILE_UPLOAD_DIR


    # 构造文件完整路径
    file_path = os.path.join(upload_dir, filename)

    # 写入文件
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"File '{filename}' written to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

# 示例：写入一个文件
if __name__ == '__main__':
    # 示例内容（可以是任何你想要写入的数据）
    file_content = b"Hello, this is a test file content."

    # 示例文件名
    file_name = "example.txt"

    # 调用函数写入文件
    success = write_file_to_upload_dir(file_name, file_content)
    if success:
        print("File written successfully!")
    else:
        print("Failed to write file.")