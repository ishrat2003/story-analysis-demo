from display.gc import GC as GCDisplay

class Generator:
    
    def __init__(self, params, reader, writer):
        self.params = params
        self.reader = reader
        self.writer = writer
        return
    
    def process(self):
        processor = GCDisplay(self.params, self.reader)
        data = processor.get()
        self.writer.save(data, 'gc')
        print(processor.getUsedKeys())
        return data
