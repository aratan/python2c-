import gradio as gr
import ollama

client = ollama.Client(host='http://localhost:11434')
# client.pull("aratan/phi4-o1:latest")  # Uncomment if you need to pull the model


# Assuming you have a function to load the model and generate responses
def load_model(model_name):
    # Placeholder for model loading logic
    # Replace with actual ollama model loading if needed
    return Model(model_name)


class Model:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate(self, prompt):
        # Placeholder for model generation logic
        # This should be replaced with actual model inference code
        # Example: Use ollama to generate response
        # response = client.generate(model=self.model_name, prompt=prompt)
        # return Response(response['response'])
        return Response(f"Converted C++ code for {prompt}, ayuda me a convertirlo a C++ no pongas comentarios")


class Response:
    def __init__(self, text):
        self.text = text


# Initialize the model
model = load_model("aratan/phi4-o1:latest")


def convert_python_to_cpp(python_code):
    # Create a prompt for conversion
    prompt = f"""
    Convert the following Python code to C++:

    ```python
    {python_code}
    ```

    Provide only the C++ code with no surrounding text or comments. Do not include any explanations before or after the code. The output should be pure C++ code ready to compile.
    """
    # Get the response from the *Ollama* model (correct call to client)
    response = client.generate(model="aratan/phi4-o1:latest", prompt=prompt)

    # This response is from ollama. We need to get the text
    cpp_code = response['response']

    # Remove triple backticks from start and end
    cpp_code = cpp_code.strip("```")

    return cpp_code


# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Convert Python to C++")

    with gr.Row():
        python_code_input = gr.Textbox(label="Python Code", lines=10, placeholder="Enter your Python code here...")
        cpp_code_output = gr.Textbox(label="C++ Code", lines=10, placeholder="Converted C++ code will appear here...")

    convert_button = gr.Button("Convert")

    convert_button.click(convert_python_to_cpp, inputs=python_code_input, outputs=cpp_code_output)

# Launch the application
demo.launch()
