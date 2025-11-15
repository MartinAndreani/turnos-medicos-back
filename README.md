    # Comandos base de datos

- **Crear migración:**

```bash
alembic revision --autogenerate -m "<mensaje_migracion>"
```

- **Correr una migración:**

```bash
alembic upgrade heads
```

- **Volver atrás una migración:**

```bash
alembic downgrade -1
```
 
- **Revertir todas las migraciones:**

```bash
alembic downgrade base
```

- **Mostrar el historial de migraciones:**

```bash
alembic history
```

- **Ver el estado actual de las migraciones:**

```bash
alembic current
```

- **Revisar diferencias entre los modelos y la base de datos:**

```bash
alembic check --autogenerate
```

- **Crear una migración vacía:**

```bash
alembic revision -m "<mensaje_migracion>"
```

- **Listar los encabezados de las migraciones actuales:**

```bash
alembic heads
```

- **Realizar el merge entre las migraciones para resolver inconsistencias:**

```bash
alembic merge -m "<mensaje_migracion>" <id_encabezado_1> <id_encabezado_2>
```

Con los comandos mencionados anteriormente se pueden realizar las totalidad de las acciones necesarias en la base de datos propiamente dicha.

# Proceso de poder ejecutar los microservicios desde un principio

**1.** Clonar el repositorio.

## CAMBIAR LA URL DEL REPOSITORIO

```bash
   git clone https://git.dtec.cordoba.gov.ar/licencias/licencias-api.git
```

**2.** Pararse dentro del directorio principal (ya teniendo _python_ instalado) y ejecutar el siguiente comando para crear un entorno virtual:

```bash
   python -m venv .venv | python3 -m venv .venv
```

**3.** Luego de haber creado el entorno virtual buscar la localizacion del archivo activate dentro de la carpeta .venv y ejecutar el siguiente comando:

```bash
   source <path hacia el archivo activate>
```

**4.** Luego ejecutar el siguiente comando para instalar las dependencias necesarias:

```bash
   pip install -r requirements.txt
```

**5.** Luego correr el comando para actualizar la estructura de la base de datos parado en el directorio base del proyecto:

```bash
   alembic upgrade heads
```

**6.** Por último levantar los procesos ejectuando el script llamado _start_services_ con el siguiente comando:

```bash
   ./start_services.sh
```
