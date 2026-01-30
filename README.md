# **Agente Negociador para Sectores Vulnerables**

## **Integrantes**
-
-
-
-
-

**Link del vídeo**

https

## **Descripción del proyecto**

El Agente Negociador para Sectores Vulnerables es un asistente inteligente basado en IA generativa, desarrollado con el modelo Qwen/Qwen2.5-1.5B-Instruct. Su función principal es actuar como un negociador empático y eficiente para clientes con dificultades económicas, ayudando a gestionar servicios de internet de forma accesible y personalizada, evitando presionar al usuario y promoviendo soluciones viables.

Este agente está diseñado para sectores vulnerables y adapta las políticas corporativas a la situación económica de cada usuario, priorizando convenios de pago justos y planes accesibles.

## **Qué hace el agente**

El agente puede:

- Informar sobre planes de internet disponibles, con características y precios:
  - Plan Solidario: 20 Mbps por $15.00 (ideal para estudiantes y hogares con presupuesto ajustado).
  - Plan Hogar: 100 Mbps por $25.00 (ideal para teletrabajo y familias).
  - Plan Gamer: 300 Mbps por $45.00 (ideal para streaming y gaming intensivo).

- Aplicar políticas de cobranza sensibles:
  - Prioriza la cuota más baja en casos de vulnerabilidad económica.
  - Ofrece convenios de 6 y 12 meses sin intereses.
  - Evita la acumulación de deuda y facilita la reactivación del servicio.
  - Acompaña al cliente sin ejercer presión indebida.

- Interactuar a través de una interfaz gráfica sencilla, desarrollada con Gradio, permitiendo que usuarios sin experiencia técnica puedan consultar planes y convenios.

## **Tecnologías y librerías utilizadas**

- Gradio: para la interfaz gráfica interactiva.
- Torch: backend para ejecución del modelo de IA.
- Transformers: para cargar y manejar el modelo Qwen/Qwen2.5-1.5B-Instruct.
- Hugging Face Hub: para autenticación y descarga del modelo.
- dotenv: para manejo seguro de credenciales mediante un archivo .env.
- os y re: utilidades estándar de Python para manejo de entorno y procesamiento de texto.

## **Configuración y uso**

1. Clona el repositorio:

```
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

2. Instala las dependencias:

```
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto con la siguiente variable:

```
TOKEN=tu_token_de_huggingface
```

> ⚠️ Importante: Por seguridad, no compartas tu token de Hugging Face. Cada usuario debe crear su propio `.env`.

4. Ejecuta la aplicación:

```
python app.py
```

5. Accede a la interfaz de Gradio desde tu navegador, interactúa con el agente y consulta planes y convenios de forma segura y sencilla.

## **Seguridad**

- Todas las credenciales se manejan de forma local y segura mediante `.env`.
- No se almacena información sensible del cliente en el sistema.
- El agente se centra en brindar soluciones éticas y responsables según las políticas de vulnerabilidad económica.