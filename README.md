# 🧩 Sistema de Administración de Empleados con Generación de Códigos QR

> Proyecto desarrollado en **Python** con **PyQt5**, **Qt Designer** y **MySQL**, que permite registrar, buscar, actualizar y eliminar empleados, generando automáticamente **códigos QR personalizados** con su información.  
> Ideal para empresas que requieren un control interno de empleados y acceso mediante códigos QR.

---

## 🧠 Descripción general

Este sistema proporciona un **control administrativo completo de empleados**. Permite:

- Registrar nuevos empleados con **ID automático**.
- Buscar empleados por su ID y visualizar toda su información.
- Actualizar campos específicos: correo, número de celular y rol.
- Eliminar empleados con confirmación.
- Generar **códigos QR** que contienen información clave (correo, celular y rol), guardándolos como imágenes en carpetas específicas.

El proyecto utiliza **Faker** para generar datos de ejemplo aleatorios y mostrar el funcionamiento completo del sistema.  
Se trata de una aplicación pensada con **enfoque empresarial**, que simula control de accesos y gestión interna de personal.

---

## 🚀 Funcionalidades principales

### 🧾 CRUD de empleados
- **Registrar empleados**: ID autoincremental, nombre completo, correo, celular, rol.
- **Buscar empleados**: mediante ID y visualización de todos los datos.
- **Actualizar empleados**: solo correo, celular y rol.
- **Eliminar empleados**: con ventana de confirmación para seguridad.

### 🧩 Generación automática de QR
- Códigos QR que incluyen: correo, celular y puesto.
- Guardado automático de la imagen QR en carpeta correspondiente.
- Compatible con ajustes futuros de control de acceso según rol.

### 🧠 Validaciones
- Todos los campos son obligatorios.
- Validación de correo electrónico (formato correcto).
- Validación de número celular (10 dígitos exactos).
- Mensajes claros de error o confirmación.

### 🔢 CURP automático (opcional)
- Estructura de CURP planeada: iniciales de apellidos y nombre + año de nacimiento.
- Método comentado para futura implementación profesional.

---

## 🧰 Tecnologías utilizadas

| Tecnología | Descripción |
|------------|------------|
| **Python 3.x** | Lenguaje principal |
| **PyQt5 / Qt Designer** | Desarrollo de interfaz gráfica |
| **MySQL / MySQL Workbench** | Gestión de base de datos relacional |
| **Faker** | Generación de datos de prueba aleatorios |
| **qrcode** | Creación de códigos QR |
| **re / random / string** | Validaciones y generación aleatoria |

---

## 🧱 Estructura del proyecto
