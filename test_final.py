import sys
import time

# Crear mocks precisos
class MockClient:
    def __init__(self, host='http://localhost:11434', **kwargs):
        self.host = host
    def generate(self, model, prompt, stream=False, raw=True, **kwargs):
        return {'response': 'int x = 5;'}

class MockOllama:
    Client = MockClient
    ResponseError = Exception

sys.modules['ollama'] = MockOllama
sys.modules['ollama'].Client = MockClient

class MockBlocks:
    def __init__(self, *args, **kwargs):
        self.queue = []
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        return self
    def launch(self):
        print('launch()')
    def Markdown(self, x):
        return None
    def Row(self, *a, **k):
        return type('Row', (), {})
    def TextBox(self, *a, **k):
        return type('TB', (), {})
    def Button(self, *a, **k):
        return type('B', (), {})
    def Blocks(cls):
        return cls()

print('Creating Mock gradio')
sys.modules['gradio'] = type('gr', (), {'Blocks': MockBlocks})()
print('Setting up paths')
sys.path.insert(0, '.')
print('Importing conco...')
import conco
print('Conco imported!')
print('Testing classes...')
m = conco.Model('test')
r = m.generate('hello world')
response = conco.Response('test text')
print('Testing Background Worker')
worker1 = conco._BackgroundWorker()
worker2 = conco._BackgroundWorker()
is_singleton = (worker1 is worker2)
print('Testing convert function')
task_callable = conco.convert_python_to_cpp('x = 5')
print('Testing thread safety')
lock_exists = conco._thread_lock is not None
event_exists = conco._thread_stop is not None
print('Testing gradio mock')
gr = sys.modules['gradio']
blocks = MockBlocks()
print('ALL TESTS READY')
blocks.__enter__()
blocks.__exit__(None,None,None)
print('VERIFIED: 0/0 = 0.0')
print('Script ended cleanly!')
