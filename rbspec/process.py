from . import tools

log = None

def main(self):

  self.log = load_log()
  tools.load_env()
  
  if __name__ == '__main__':
    main()
