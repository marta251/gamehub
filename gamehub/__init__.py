from . import gamehub

def main() -> None:
    gamehub_instance = gamehub.GameHub()
    gamehub_instance.run()

if __name__ == "__main__":
    main()