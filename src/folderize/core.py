import argparse


def main():
    parser = argparse.ArgumentParser(description="My CLI tool")
    parser.add_argument("--name", help="Your name")
    args = parser.parse_args()

    if args.name:
        print(f"Hello, {args.name}!")
    else:
        print("Hello!")
