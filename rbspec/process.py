from . import tools

log = None

def main():
  global log
  log = load_log()
  tools.load_env()
  
  if __name__ == '__main__':
    main()
