# Autor: Carlos Palacios Betancourt
# Python  3.10.11

# pip install pyqt5 pymysql
import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import re
import random
import string

# --- Función para generar CURP ---
def generar_curp_fake():
    """Genera una CURP aleatoria de 18 caracteres tipo Faker."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=18))

class Usuarios(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar interfaz desde Qt Designer
        loadUi(r"RUTA DONDEGUARDASTE TUA RCHIVO .UI", self)
        self.txtCorreo.setEnabled(True)
        self.txtCorreo.setReadOnly(False)
        self.conexion()
        
        # Tomar el rol seleccionado
        rol = self.cbRol.currentText()  # 'cbRol' es el ComboBox que ya existe en la UI

        # Conectar botones
        self.btnRegistrar.clicked.connect(self.registrar)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnCancelar.clicked.connect(self.cancelar)

        # Validadores
        self.txtID.setValidator(QIntValidator(0, 99999))       # solo números, 5 dígitos
        self.txtCelular.setValidator(QIntValidator())          # solo números
        self.txtCURP.setMaxLength(18)                          # CURP 18 caracteres

    
    # -------------------------------------------------------
    # Conexión con la base de datos
    # -------------------------------------------------------
    def conexion(self):
        try:
            self.c = pymysql.connect(
                host="localhost",
                user="TU USUARIO",
                password="TU CONTRASEÑA",
                db="LA BASE DE DATOS QUE SE NECESITE"
            )
            self.cur = self.c.cursor()
            QMessageBox.information(self, "Conexión", "Conexión establecida con éxito")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error de conexión: {str(e)}")

    def closeEvent(self, evento):
        try:
            if hasattr(self, 'c') and self.c.open:
                self.c.close()
                if hasattr(self, 'cur'):
                    self.cur.close()
            print("Conexión cerrada correctamente desde closeEvent")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
            evento.accept()

    # -------------------------------------------------------
    # MÉTODO REGITRAR (Registrar Usuario)
    # -------------------------------------------------------
    def registrar(self):
        # --- Generar ID automáticamente ---
        try:
            self.cur.execute("SELECT MAX(idusuario) FROM Usuarios;")
            max_id = self.cur.fetchone()[0]
            id_user = str(max_id + 1 if max_id else 1)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo obtener el siguiente ID:\n{e}")
            return

        paterno = self.txtPaterno.text().strip().upper()
        materno = self.txtMaterno.text().strip().upper()
        nombre = self.txtNombre.text().strip().upper()
        correo = self.txtCorreo.text().strip()
        celular = self.txtCelular.text().strip()
        rol = self.cbRol.currentText()

        # Validar campos vacíos
        if not all([paterno, materno, nombre, correo, celular, rol]):
            QMessageBox.warning(self, "Atención", "Todos los campos son obligatorios.")
            return

        # Validar correo con regex
        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_correo, correo):
            QMessageBox.warning(self, "Error", "Ingrese un correo válido.")
            return

        # Validar celular
        if not celular.isdigit() or len(celular) != 10:
            QMessageBox.warning(self, "Error", "El celular debe tener exactamente 10 dígitos.")
            return
        curp = generar_curp_fake()

        # --- Generar CURP automáticamente (simplificado) ---
        # Formato: primeras 2 letras paterno + primera del materno + primera del nombre + 4 dígitos del año
        # Ajusta según tus reglas reales de CURP
        # año_nacimiento = self.txtAnoNacimiento.text().strip()  # Si tienes un campo para año
        # if not año_nacimiento.isdigit() or len(año_nacimiento) != 4:
            # QMessageBox.warning(self, "Error", "Ingrese un año válido de nacimiento (AAAA).")
            # return
        # curp = (paterno[:2] + materno[:1] + nombre[:1] + año_nacimiento).upper()

        # Inserción a la base de datos
        try:
            query = """
                INSERT INTO Usuarios (idusuario, paterno, materno, nombre, correo, celular, rol, curp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            datos = (id_user, paterno, materno, nombre, correo, celular, rol, curp)
            self.cur.execute(query, datos)
            self.c.commit()
            QMessageBox.information(self, "Registro", f"Usuario registrado correctamente con ID {id_user} y CURP {curp}.")
            self.limpiar()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo insertar el registro:\n{str(e)}")

    # -------------------------------------------------------
    # MÉTODOS CRUD PENDIENTES (por construir en clase)
    # -------------------------------------------------------
    def curp(self):
        pass
    
    def qr(self):
        pass 
    
    def buscar(self):
        # Capturar el ID ingresado
        id_usuario = self.txtID.text()

        # Validación básica: no dejar vacío
        if not id_usuario:
            QMessageBox.warning(self, "Error", "Por favor ingresa un ID")
            return

        try:
            # Consulta a la base de datos
            consulta = "SELECT * FROM Usuarios WHERE idusuario = %s"
            self.cur.execute(consulta, (id_usuario,))
            resultado = self.cur.fetchone()  # Trae un solo registro

            if resultado is None:
                QMessageBox.warning(self, "Error", f"No existe un usuario con ID {id_usuario}")
                return

            # Resultado de ejemplo:
            # resultado = (idusuario, paterno, materno, nombre, correo, celular, rol, curp, qr)
            self.txtPaterno.setText(resultado[1])
            self.txtMaterno.setText(resultado[2])
            self.txtNombre.setText(resultado[3])
            self.txtCorreo.setText(resultado[4])
            self.txtCelular.setText(resultado[5])
            self.cbRol.setCurrentText(resultado[6])
            self.txtCURP.setText(resultado[7])
            
            # Después de asignar los valores a los QLineEdit y QComboBox
            self.txtPaterno.setReadOnly(True)
            self.txtMaterno.setReadOnly(True)
            self.txtNombre.setReadOnly(True)
            self.txtCorreo.setReadOnly(True)
            self.txtCelular.setReadOnly(True)
            self.cbRol.setEnabled(False)
            self.txtCURP.setReadOnly(True)

            # Mensaje de confirmación
            QMessageBox.information(self, "Buscar", f"Usuario con ID {id_usuario} encontrado")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al buscar el usuario: {str(e)}")
            
    def actualizar(self):
        id_user = self.txtID.text().strip()
        if not id_user:
            QMessageBox.warning(self, "Atención", "Ingrese un ID primero.")
            return

        # Si los campos están deshabilitados, solo habilitarlos
        if self.txtCorreo.isReadOnly():
            resp = QMessageBox.question(
                self, "Actualizar datos",
                "¿Seguro que quieres actualizar los datos?",
                QMessageBox.Yes | QMessageBox.No
            )
            if resp == QMessageBox.Yes:
                # Habilitar campos
                self.txtCorreo.setEnabled(True)
                self.txtCorreo.setReadOnly(False)
                self.txtCelular.setEnabled(True)
                self.txtCelular.setReadOnly(False)
                self.cbRol.setEnabled(True)
            return

        # Si ya estaban habilitados, guardar los cambios
        correo_nuevo = self.txtCorreo.text().strip()
        celular_nuevo = self.txtCelular.text().strip()
        rol_nuevo = self.cbRol.currentText()

        # Validaciones
        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_correo, correo_nuevo):
            QMessageBox.warning(self, "Error", "Ingrese un correo válido.")
            return
        if not celular_nuevo.isdigit() or len(celular_nuevo) != 10:
            QMessageBox.warning(self, "Error", "El celular debe tener 10 dígitos.")
            return

        # Guardar en la base de datos
        try:
            query = "UPDATE Usuarios SET correo=%s, celular=%s, rol=%s WHERE idusuario=%s"
            self.cur.execute(query, (correo_nuevo, celular_nuevo, rol_nuevo, id_user))
            self.c.commit()
            QMessageBox.information(self, "Actualizar", "Datos actualizados correctamente.")

            # Volver a deshabilitar campos
            self.txtCorreo.setReadOnly(True)
            self.txtCorreo.setEnabled(False)
            self.txtCelular.setReadOnly(True)
            self.txtCelular.setEnabled(False)
            self.cbRol.setEnabled(False)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo actualizar:\n{str(e)}")
            return
            

    def eliminar(self):
        id_user = self.txtID.text().strip()
        if not id_user:
            QMessageBox.warning(self, "Atención", "Ingrese un ID para eliminar.")
            return

        # Confirmación
        resp = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Está seguro(a) de eliminar al usuario con ID {id_user}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resp == QMessageBox.Yes:
            try:
                query = "DELETE FROM Usuarios WHERE idusuario = %s"
                self.cur.execute(query, (id_user,))
                self.c.commit()  # <-- Aquí usas la conexión correcta
                QMessageBox.information(self, "Eliminar", "Usuario eliminado correctamente.")
                self.limpiar()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar el usuario:\n{str(e)}")

    # -------------------------------------------------------
    # UTILIDADES
    # -------------------------------------------------------
    def limpiar(self):
        """Limpia todos los campos."""
        self.txtID.clear()
        self.txtPaterno.clear()
        self.txtMaterno.clear()
        self.txtNombre.clear()
        self.txtCorreo.clear()
        self.txtCelular.clear()
        self.txtCURP.clear()
        self.txtQR.clear()
        self.cbRol.setCurrentIndex(0)

    def cancelar(self):
        """Cancela la operación actual."""
        self.limpiar()


# -------------------------------------------------------
# ESTRUCTURA DE ARRANQUE (NO MODIFICAR)
# -------------------------------------------------------
# Estructura de arranque
if __name__ == "__main__":
    app = QApplication(sys.argv)
    usuarios = Usuarios()
    usuarios.show()
    app.exec()