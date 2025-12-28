import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Folderize: Organize your files into folders based on their extensions."
    )
    args = parser.parse_args()

    if args.name:
        print(f"Hello, {args.name}!")
    else:
        print("Hello!")
