import os
from PIL import Image
import argparse

def split_bmp_image_overlap(input_path, output_dir, tile_width=512, tile_height=512, overlap=256):
    """
    将大尺寸BMP图片分割成指定大小的小图片，水平方向有重叠
    
    参数:
        input_path: 输入的BMP图片路径
        output_dir: 输出目录
        tile_width: 分割后每个小图片的宽度，默认512
        tile_height: 分割后每个小图片的高度，默认512
        overlap: 水平方向重叠像素数，默认256
    """
    
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开源图片
    with Image.open(input_path) as img:
        # 获取图片尺寸
        img_width, img_height = img.size
        print(f"源图片尺寸: {img_width} x {img_height}")
        
        # 验证图片尺寸是否符合预期
        expected_width = 15360
        expected_height = 8192
        if img_width != expected_width or img_height != expected_height:
            print(f"警告: 图片尺寸不是预期的 {expected_width} x {expected_height}")
        
        # 计算可以分割的行数和列数（考虑重叠）
        # 水平方向：每次移动 (tile_width - overlap) 像素
        step_x = tile_width - overlap
        cols = (img_width - overlap) // step_x
        rows = img_height // tile_height
        
        print(f"水平方向步长: {step_x} 像素")
        print(f"将分割成 {rows} 行 x {cols} 列 = {rows * cols} 张小图片")
        print(f"每张小图片尺寸: {tile_width} x {tile_height}")
        print(f"水平重叠: {overlap} 像素")
        
        # 获取文件名（不含扩展名）
        filename = os.path.splitext(os.path.basename(input_path))[0]
        
        # 开始分割图片
        count = 0
        for row in range(rows):
            for col in range(cols):
                # 计算当前切片的边界框
                left = col * step_x
                upper = row * tile_height
                right = left + tile_width
                lower = upper + tile_height
                
                # 确保不超出图片边界
                if right > img_width:
                    right = img_width
                    left = right - tile_width
                
                # 裁剪图片
                tile = img.crop((left, upper, right, lower))
                
                # 生成输出文件名
                output_filename = f"{filename}_row{row:02d}_col{col:02d}.bmp"
                output_path = os.path.join(output_dir, output_filename)
                
                # 保存图片
                tile.save(output_path, "BMP")
                count += 1
                
                # 打印进度
                if count % 50 == 0:
                    print(f"已处理 {count} 张图片...")
        
        print(f"分割完成！共生成 {count} 张图片，保存在目录: {output_dir}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='分割大尺寸BMP图片成多个512x512的小图片（水平重叠）')
    parser.add_argument('input_file', help='输入的BMP文件路径')
    parser.add_argument('-o', '--output', default='output_tiles_overlap', 
                       help='输出目录 (默认: output_tiles_overlap)')
    parser.add_argument('--width', type=int, default=512, 
                       help='分割宽度 (默认: 512)')
    parser.add_argument('--height', type=int, default=512, 
                       help='分割高度 (默认: 512)')
    parser.add_argument('--overlap', type=int, default=256,
                       help='水平重叠像素数 (默认: 256)')
    
    args = parser.parse_args()
    
    try:
        split_bmp_image_overlap(
            input_path=args.input_file,
            output_dir=args.output,
            tile_width=args.width,
            tile_height=args.height,
            overlap=args.overlap
        )
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    # 使用示例（如果直接运行而不使用命令行参数）
    # 取消下面的注释并修改路径即可使用
    
    # input_image = "your_image.bmp"  # 替换为你的BMP文件路径
    # output_directory = "split_images_overlap"
    # split_bmp_image_overlap(input_image, output_directory)
    
    # 使用命令行参数
    import sys
    if len(sys.argv) == 1:
        print("请使用命令行参数运行脚本，或修改脚本中的示例路径")
        print("示例: python script.py input.bmp -o output_dir")
        sys.exit(1)
    
    sys.exit(main())