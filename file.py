import os
import shutil


def clean_brats20_dataset(root_dir, keep_extensions=None, keep_filenames=None):
    if keep_extensions is None:
        keep_extensions = ['_flair_text.txt', '_flair_text.npy']  # 只保留这些后缀
    if keep_filenames is None:
        keep_filenames = []  # 可以指定完整文件名，不含扩展名

    for sample_folder in os.listdir(root_dir):
        sample_path = os.path.join(root_dir, sample_folder)
        if os.path.isdir(sample_path):
            for file in os.listdir(sample_path):
                file_path = os.path.join(sample_path, file)
                file_ext = os.path.splitext(file)[-1]
                file_name = os.path.splitext(file)[0]

                if not any(file.endswith(ext) for ext in keep_extensions) and file_name not in keep_filenames:
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                else:
                    # 重命名指定的两个文件
                    if file.endswith('_flair_en_temp_machine.txt'):
                        new_file_path = os.path.join(sample_path,
                                                     file.replace('_flair_en_temp_machine.txt', '_flair_text.txt'))
                        os.rename(file_path, new_file_path)
                        print(f"Renamed: {file_path} -> {new_file_path}")
                    elif file.endswith('_flair_biobert_temp_machine.npy'):
                        new_file_path = os.path.join(sample_path,
                                                     file.replace('_flair_biobert_temp_machine.npy', '_flair_text.npy'))
                        os.rename(file_path, new_file_path)
                        print(f"Renamed: {file_path} -> {new_file_path}")
    print("Cleanup completed!")


# 示例：清理BraTS20数据集文件夹
brats20_root = "./data/TextBraTSData"  # 修改为实际路径
keep_files = []# 只保留这些文件名（不含扩展名）
clean_brats20_dataset(brats20_root, keep_filenames=keep_files)
