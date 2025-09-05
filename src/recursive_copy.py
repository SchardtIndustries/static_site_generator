import os
import shutil
import logging

def copy_dir_clean(source_dir, dest_dir):
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    if os.path.exists(dest_dir):
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logging.info(f"Deleted directory: {item_path}")
                else:
                    os.remove(item_path)
                    logging.info(f"Deleted file: {item_path}")
            except Exception as e:
                logging.error(f"Error deleting {item_path}: {e}")
    else:
        os.makedirs(dest_dir)

    def copy_recursive(src, dst):
        for item in os.listdir(src):
            s_item = os.path.join(src, item)
            d_item = os.path.join(dst, item)
            if os.path.isdir(s_item):
                os.makedirs(d_item, exist_ok=True)
                logging.info(f"Created directory: {d_item}")
                copy_recursive(s_item, d_item)
            else:
                shutil.copy2(s_item, d_item)
                logging.info(f"Copied file: {s_item} -> {d_item}")


    copy_recursive(source_dir, dest_dir)

