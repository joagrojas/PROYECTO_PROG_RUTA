# RutaSegura
 Plataforma para registrar, consultar y analizar siniestros de tránsito en La Rioja, permitiendo a las autoridades tomar decisiones basadas en datos - Proyecto para catedra programación 2


uso: 
1. Crear y activar entorno virtual
   
# Navegar al directorio backend
cd C:/Users/Tincho/Documents/RutaSegura/backend

# Crear entorno virtual:

# Con venv (recomendado)
python -m venv venv

2. Activar el entorno virtual
.\venv\Scripts\activate.bat

3. Instalar todas las dependencias
 
# Con el entorno virtual ACTIVADO
pip install -r requirements.txt


#inicia el backend (en carpeta raiz):
cd backend: uvicorn main:app --reload

#inicia el frontend (en carpeta raiz):
cd frontend: npm run dev

