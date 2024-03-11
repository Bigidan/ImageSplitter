import os

def CountPagesNumb(chapter_path, path="tmp"):
        count_file=0
        for path in os.scandir(f"{chapter_path}/{path}/"):
            if path.is_file():
                count_file += 1
        return count_file