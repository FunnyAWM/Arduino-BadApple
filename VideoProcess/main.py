import sys

import cv2 as cv


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)
    target = cv.VideoCapture(sys.argv[1])
    if not target.isOpened():
        print("Could not open video file")
        sys.exit(1)
    fps = target.get(cv.CAP_PROP_FPS)
    delay_time = int(1000 // fps)
    with open("video_arr.txt", "w") as f_out:  # 初始化时清空旧文件
        while True:
            ret, frame = target.read()
            if not ret:
                break
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = cv.resize(frame, (12, 8))

            frame_matrix = []
            for i in range(8):
                for j in range(12):
                    pixel = frame[i, j]
                    bit = 1 if pixel > 127 else 0
                    frame_matrix.append(bit)
            frame_data = []
            for chunk in range(3):
                row_val = 0
                for bit in frame_matrix[chunk * 32: (chunk + 1) * 32]:
                    row_val = (row_val << 1) | bit
                frame_data.append(row_val & 0xFFFFFFFF)  # 确保是32位
            f_out.write("{ ")
            for val in frame_data:
                f_out.write(f"{val:#08x}, ")
            f_out.write(str(delay_time) + " }, \n")
        f_out.close()
    with open("video_arr.txt", "r+") as f_out:
        content = f_out.read()
        if content.endswith(', \n'):
            content = content[:-3] + '\n'
        f_out.seek(0)
        f_out.write(content)
        f_out.truncate()


if __name__ == "__main__":
    main()
