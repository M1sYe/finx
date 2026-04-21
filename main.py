from cache_manager import CacheManager
from cli_interface import CLIInterface
from logger import log_execution, Logger

Logger._initialize_logger()
Logger.clear_logs()

@log_execution
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