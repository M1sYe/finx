from cache_manager import CacheManager
from cli_interface import CLIInterface

def main():
    cache = CacheManager()
    cli = CLIInterface(cache)
    
    while True:
        try:
            cli.run()
        except KeyboardInterrupt:
            print("\n\nработа завершена")
            break
        except Exception as e:
            print(f"непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()