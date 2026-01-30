import gradio as gr
import torch
import re
from transformers import pipeline, AutoTokenizer
from huggingface_hub import login
import dotenv
import os

# =====================================================
# 1. CONFIGURACIÓN GENERAL
# =====================================================
# Token personal de Hugging Face (necesario para cargar el modelo)
dotenv.load_dotenv()
token = os.getenv('TOKEN')
login(token)

print("\n🚀 Iniciando Agente IA de Negociación – Proyecto Meta Thinkers")

# Modelo liviano pero potente para conversación
modelo_id = "Qwen/Qwen2.5-1.5B-Instruct"

# Tokenizador y pipeline de generación de texto
tokenizer = AutoTokenizer.from_pretrained(modelo_id)
pipe = pipeline(
    "text-generation",
    model=modelo_id,
    device="cpu",          # CPU para evitar problemas de compatibilidad
    torch_dtype=torch.float32
)

# =====================================================
# 2. HERRAMIENTAS DE APOYO
# =====================================================
class Herramientas:
    """
    Funciones auxiliares que ayudan al agente a:
    - leer información externa
    - detectar emociones
    - analizar perfil del usuario
    - calcular planes de pago
    """

    @staticmethod
    def leer_precios_del_txt():
        # Lee los planes de internet desde un archivo externo
        try:
            with open("conocimiento.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Archivo conocimiento.txt no encontrado."

    @staticmethod
    def analizar_sentimiento(texto):
        # Palabras clave para detectar vulnerabilidad emocional
        palabras_vulnerables = [
            "triste", "lloro", "despedido", "sin trabajo", "no tengo ingresos",
            "crisis", "familia", "accidente", "enfermo", "ayuda"
        ]
        if any(p in texto.lower() for p in palabras_vulnerables):
            return "ESTADO EMOCIONAL: VULNERABLE"
        return "ESTADO EMOCIONAL: NORMAL"

    @staticmethod
    def detectar_perfil(texto):
        # Clasificación básica del perfil socioeconómico
        texto = texto.lower()
        if any(p in texto for p in ["sin trabajo", "desempleado", "no tengo ingresos", "crisis"]):
            return "PERFIL SOCIOECONÓMICO: ALTA VULNERABILIDAD"
        if any(p in texto for p in ["estudiante", "medio tiempo", "ingreso bajo"]):
            return "PERFIL SOCIOECONÓMICO: VULNERABILIDAD MEDIA"
        return "PERFIL SOCIOECONÓMICO: ESTABLE"

    @staticmethod
    def calcular_logica_completa(deuda_total, oferta_usuario=None):
        # Lógica matemática simple para planes de pago
        if deuda_total <= 0:
            return ""

        c6 = round(deuda_total / 6, 2)
        c12 = round(deuda_total / 12, 2)

        if oferta_usuario and oferta_usuario > 0:
            if oferta_usuario < 1:
                oferta_usuario = 1
            meses = round(deuda_total / oferta_usuario, 1)

            return f"""
🚨 CÁLCULO DE PAGO 🚨
Deuda total: ${deuda_total}
Pago mensual propuesto: ${oferta_usuario}

${deuda_total} / ${oferta_usuario} = {meses} meses

INSTRUCCIÓN:
- Informar el tiempo total de pago.
- No realizar preguntas adicionales.
"""

        return f"""
[OPCIONES DE CONVENIO]
- Deuda total: ${deuda_total}
- Plan 6 meses: ${c6} mensuales
- Plan 12 meses: ${c12} mensuales
"""

# =====================================================
# 3. AGENTE PRINCIPAL
# =====================================================
class Agente:
    """
    Agente conversacional que gestiona:
    - cobranzas
    - negociación de pagos
    - consulta de planes
    """

    def __init__(self):
        self.deuda_detectada = 0.0  # memoria simple de la deuda

    def responder(self, mensaje, historial):
        mensaje_min = mensaje.lower()
        numeros = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', mensaje)]
        oferta_actual = None

        # Detección básica de intención
        es_cobranza = any(p in mensaje_min for p in ["deuda", "debo", "pagar", "factura", "atraso"])
        quiere_planes = any(p in mensaje_min for p in ["plan", "internet", "megas", "precio", "contratar"])

        # -------- MEMORIA DE DEUDA --------
        if es_cobranza and numeros:
            posible = max(numeros)
            palabras_deuda = ["deuda", "debo", "factura", "total"]

            if any(p in mensaje_min for p in palabras_deuda) and posible > 5:
                self.deuda_detectada = posible
            elif self.deuda_detectada > 0 and posible < self.deuda_detectada:
                oferta_actual = posible

        # -------- PROMPT DINÁMICO --------
        if quiere_planes:
            info_txt = Herramientas.leer_precios_del_txt()
            system_prompt = f"""
Eres asesor comercial de Netlife.

Información disponible:
{info_txt}

Reglas:
- Mostrar planes cuando el usuario lo solicite.
- Si elige uno, responder:
  "¡Excelente elección! Un asesor se comunicará contigo."
"""

        elif self.deuda_detectada > 0:
            info_math = Herramientas.calcular_logica_completa(self.deuda_detectada, oferta_actual)
            estado = Herramientas.analizar_sentimiento(mensaje)
            perfil = Herramientas.detectar_perfil(mensaje)

            system_prompt = f"""
Eres un agente de cobranzas empático.

{estado}
{perfil}

Cálculo automático:
{info_math}

Reglas:
- Si el usuario ofrece un pago mensual, no hacer preguntas.
- Explicar claramente el tiempo total de pago.
- Mantener tono respetuoso y humano.
"""

        else:
            system_prompt = """
Eres un asistente de Netlife.
Saluda y ofrece ayuda con planes o pagos pendientes.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensaje}
        ]

        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        output = pipe(
            prompt,
            max_new_tokens=220,
            temperature=0.1,
            do_sample=True
        )

        return output[0]["generated_text"] \
            .split("<|im_start|>assistant")[-1] \
            .replace("<|im_end|>", "") \
            .strip()

# =====================================================
# 4. INTERFAZ GRÁFICA
# =====================================================
agente = Agente()

def chatear(msg, hist):
    return agente.responder(msg, hist)

interfaz = gr.ChatInterface(
    fn=chatear,
    title="🤖 Agente IA de Negociación – Meta Thinkers",
    description="Simulación de negociación de deudas y consulta de planes.",
    examples=[
        "Debo 150 dólares",
        "Estoy sin trabajo",
        "Solo puedo pagar 10 dólares al mes",
        "Qué planes de internet tienen"
    ]
)

interfaz.launch()
