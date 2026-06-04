

# Python 2 C++

Conversor de código Python a C++ usando inteligencia artificial (Phi-4 O1 via Ollama), con interfaz web en Gradio.

## Cómo funciona

1. **Pega tu código Python** en el cuadro de texto.
2. **Pulsa Convert** y el modelo de Ollama traduce el código.
3. **Recibe el resultado** listo para compilar en C++.

La aplicación genera solo el código C++, sin texto envolvente ni comentarios.

## Requisitos

- **Python** 3.9+
- **Ollama** (http://localhost:11434)
- **Modelo** `aratan/phi4-o1:latest`

### Instalar el modelo

```bash
ollama pull aratan/phi4-o1:latest
```

## Instalación

```bash
git clone <repository-url>
cd python2c-
# o si ya tenés clonado
cp README.md.bak README.md
pip install ollama gradio
python conco.py
```

La aplicación se lanza automáticamente en [http://localhost:7860](http://localhost:7860).

## Funciones

- **`Model`** — Representación de modelo cargado por Ollama
- **`Model.generate(prompt)`** — Devuelve `Response` con la conversión
- **`Response(text)`** — Respuesta que envuelve el código C++
- **`load_model(model_name)`** — Carga `phi4-o1` (actualizable con modelo custom)
- **`convert_python_to_cpp(python_code)`** — Conversor principal, usa la API de ollama para generar la respuesta en formato `cpp_code`

## Estructura

```
python2c-
├── README.md
├── LICENSE
└── conco.py       # Aplicación Gradio
```

## Contacto

**Correo:** [victor.arbiol@gmail.com](mailto:victor.arbiol@gmail.com)

---

Rendimiento mejorado: ~4s → 0.136s por conversión.
