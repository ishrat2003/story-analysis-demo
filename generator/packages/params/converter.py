from .core import Core

class Converter(Core):

  def __init__(self):
    super().__init__()
    self.parser.add_argument('--total_files', default=0, help = "Total files to processs")
    return
