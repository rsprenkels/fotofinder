import os


def want_this(file) -> bool:
    filename, file_extension = os.path.splitext(file)
    # print(f"checking {file} of parts {filename} {file_extension}")
    return file_extension[1:].lower() in ["jpg"]


def main():
    starting_dir = "c:\\Users\\RonSprenkels\\IdeaProjects\\"
    for root, dirs, files in os.walk(starting_dir):
        path = root.split(os.sep)
        # print(f"root:{root}  path:{path}  dirs:{dirs}  files:{files}")
        # print((len(path) - 1) * "---", os.path.basename(root))
        for file in files:
            if want_this(file):
                print(f"{root}\\{file}")


if __name__ == "__main__"
    main()
