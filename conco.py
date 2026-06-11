import gradio as gr
import ollama
from ollama import ResponseError
import requests
import concurrent.futures
import threading
import json

# Global state
client = ollama.Client(host='http://localhost:11434')
ollama_url = 'http://localhost:11434'
_thread_lock = threading.Lock()
_thread_stop = threading.Event()
_background_worker = None
_thread_running = False


def load_model(model_name):
    return Model(model_name)


class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self._cached_response = None

    def _generate_with_ollama(self, prompt):
        try:
            response = client.generate(
                model=self.model_name, 
                prompt=prompt, 
                stream=False, 
                raw=True,
                options={"temperature": 0.1, "num_predict": 512}
            )
            return response
        except (ConnectionError, ollama.ResponseError, TimeoutError) as e:
            print(f"Ollama error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def generate(self, prompt):
        if prompt.strip() and prompt.split()[-1] in ('```python', 'python '):
            return self._generate_with_ollama(prompt)
        
        return Response(f"Placeholder response for: {prompt}")


class Response:
    def __init__(self, text):
        self.text = text


def stop_background_thread():
    """Termina el hilo de fondo de conversion"""
    _thread_stop.set()
    if _thread and hasattr(_thread, 'is_alive()') and _thread.is_alive():
        _thread.join(timeout=2)


def start_background_thread():
    """Hilo de fondo para conversión asíncrona"""
    global _thread_running, _thread_stop, _thread
    if not _thread_running:
        _thread_running = True
        _thread_stop.clear()

    def run_loop():
        _thread = threading.current_thread()
        while not _thread_stop.is_set():
            try:
                for item in list(gr.Blocks.queue):
                    stop_background_thread()
            except:
                pass
            timeout = 5 if not _thread_stop.is_set() else 0.1
            if not _thread_stop.wait(timeout):
                pass

    t = threading.Thread(target=run_loop, daemon=True)
    t.start()
    return t


def get_or_create_thread():
    """Obtiene o crea el hilo actual"""
    global _thread
    if _thread is None:
        _thread = threading.current_thread()
    return _thread


class _BackgroundWorker:
    """Trabajador de fondo singleton para manejar conversiones"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._create()
        return cls._instance

    def _create(self):
        """Crea o reinicia el worker"""
        pass

    def add_task(self, fn, *args, **kwargs):
        """Agrega y ejecuta una tarea"""
        _thread_stop.clear()
        if not _thread_stop.is_set():
            start_background_thread()
        
        def wrapper():
            try:
                result = fn(*args, **kwargs)
                return result
            except Exception as e:
                print(f'Worker error: {e}')
                return None
        
        return wrapper()

    def process_queue(self):
        """Procesa la cola de tareas"""
        pass


def convert_python_to_cpp(python_code):
    worker = _BackgroundWorker()
    
    prompt = f"""Convert the following Python code to C++:

```python
{python_code}
```

Provide only the C++ code with no surrounding text or comments. Do not include any explanations before or after the code. The output should be pure C++ code ready to compile."""
    
    def conversion_task():
        response = client.generate(model="aratan/qwen3.5-uncensored:9b", prompt=prompt)
        if response:
            cpp_code = response['response'].strip("` ``")
            print(f'Conversion result: {cpp_code}')
            return cpp_code
        return 'int x = 5;\nint y = 10;'

    return worker.add_task(conversion_task)


# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Convert Python to C++")

    with gr.Row():
        python_code_input = gr.Textbox(
            label="Python Code", 
            lines=10, 
            placeholder="Enter your Python code here..."
        )
        cpp_code_output = gr.Textbox(
            label="C++ Code", 
            lines=10, 
            placeholder="Converted C++ code will appear here..."
        )

    convert_button = gr.Button("Convert")

    convert_button.click(convert_python_to_cpp, 
                        inputs=python_code_input, 
                        outputs=cpp_code_output)

# Launch the application
demo.launch()