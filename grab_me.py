import os
import sys
from sys import builtin_module_names
from tkinter import *
import datetime

from bcncita import CustomerProfile, DocType, Office, OperationType, Province, try_cita

root = Tk()
root.geometry("400x500")
root.title("Formulario Citas")

def switch_tipo_operacion(index):
    switcher = {
        "SOLICITUD DE ASILO": OperationType.SOLICITUD_ASILO,
        "SOLICITUD DE ASILO BARCELONA/ALICANTE": OperationType.SOLICITUD_ASILO_BARCELONA,
        "NUEVA NORMALIDAD": OperationType.NUEVA_NORMALIDAD,
        "CERTIFICADOS DE RESIDENCIA": OperationType.CERTIFICADOS_RESIDENCIA,
        "TOMA DE HUELLAS": OperationType.TOMA_HUELLAS,
        "ASIGNACIÓN DE NIE": OperationType.ASIGNACION_DE_NIE,
        "AUTORIZACIÓN DE RESIDENCIA TEMPORAL POR ARRAIGO": OperationType.AUTORIZACIÓN_DE_RESIDENCIA_TEMPORAL_ARRAIGO,
    }
    return switcher[index]

def switch_provincia(index):
    switcher = {
        "Madrid": Province.MADRID,
        "Barcelona": Province.BARCELONA,
        "Alicante": Province.ALICANTE,
    }
    return switcher[index]

def enviar_datos():
    customer.name = (input_nombre.get()).upper()
    customer.phone = input_telefono.get()
    customer.email = input_email.get()
    customer.doc_value = input_documento.get()
    customer.doc_type = DocType.PASSPORT if click_tipo_documento.get() == "Pasaporte" else DocType.NIE
    customer.province = switch_provincia(click_provincia.get())
    customer.offices = [] if click_provincia.get() == "Madrid" or click_provincia.get() == "Alicante" else [Office.BARCELONA, Office.MATARO]
    customer.operation_code = switch_tipo_operacion(click_tipo_operacion.get())
    customer.card_expire_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    customer.country = input_pais.get()
    customer.year_of_birth = input_fecha_nacimiento.get()
    
    # myLabel1 = Label(root, text=customer.name +" "+ customer.phone +" "+ customer.email +" "+ customer.doc_type +" "+ customer.doc_value +" "+ customer.province +" "+ customer.operation_code)
    # myLabel1.pack()
    if "--autofill" not in sys.argv:
        try_cita(context=customer, cycles=1000)  # Try 1000 times
    else:
        from mako.template import Template

        tpl = Template(
            filename=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "bcncita/template/autofill.mako"
            )
        )
        print(tpl.render(ctx=customer))  # Autofill for Chrome

if __name__ == "__main__":

    customer = CustomerProfile(
        # Anti-captcha API Key (auto_captcha=False to disable it)
        anticaptcha_api_key="b8489c76a88a05c44ce1036b75769d5c",
        #sms_webhook_token = "ea8a0124-0fdc-4e2f-a20d-a3f41b254f27",
        # Enable anti-captcha plugin (if False, you have to solve reCaptcha manually and press ENTER in the Terminal)
        auto_captcha=False,
        auto_office=True,
        chrome_driver_path="C:/Users/jasil/AppData/Local/Programs/Python/Python38/chromedriver",
        save_artifacts=False,  # Record available offices / take available slots screenshot
        province=Province.MADRID,
        operation_code=OperationType.TOMA_HUELLAS,
        doc_type=DocType.PASSPORT,  # DocType.NIE or DocType.PASSPORT   Y6932918L
        doc_value="157436549",  # NIE or Passport number, no spaces.
        country="ESPAÑA",
        name="DIEGO GIL",  # Your Name
        phone="641382759",  # Phone number (use this format, please)
        email="cuentarecuperacion211@gmail.com",  # Email
        year_of_birth = "2000",
        # Offices in order of preference
        # This selects specified offices one by one or a random one if not found.
        # For recogida only the first specified office will be attempted or none
        offices=[],
    )

    #   NOMBRE
    label_nombre = Label(root, text="Ingrese el nombre:")
    label_nombre.pack()
    input_nombre = Entry(root, width=50)
    input_nombre.pack(ipady=3)

    #   NÚMERO DE TELÉFONO
    label_telefono = Label(root, text="Ingrese el número de teléfono")
    label_telefono.pack()
    input_telefono = Entry(root, width=50)
    input_telefono.insert(0, "641382759")
    input_telefono.pack(ipady=3)

    #   CORREO ELÉCTRONICO
    label_email = Label(root, text="Ingrese la dirección de correo eléctronico")
    label_email.pack()
    input_email = Entry(root, width=50)
    input_email.insert(0, "cuentarecuperacion211@gmail.com")
    input_email.pack(ipady=3)

     #   PAÍS
    label_pais = Label(root, text="Ingrese el país")
    label_pais.pack()
    input_pais = Entry(root, width=50)
    input_pais.insert(0, "ESPAÑA")
    input_pais.pack(ipady=3)

    #   PAÍS
    label_fecha_nacimiento = Label(root, text="Año de nacimiento")
    label_fecha_nacimiento.pack()
    input_fecha_nacimiento = Entry(root, width=50)
    input_fecha_nacimiento.insert(0, "1990")
    input_fecha_nacimiento.pack(ipady=3)

    #   TIPO DE DOCUMENTO
    click_tipo_documento = StringVar()
    click_tipo_documento.set("Pasaporte")
    label_tipo_documento = Label(root, text="Elija el tipo de documento")
    label_tipo_documento.pack()
    input_tipo_documento = OptionMenu(root, click_tipo_documento, "Pasaporte", "NIE")
    input_tipo_documento.pack()

    #   NÚMERO DE DOCUMENTO
    label_documento = Label(root, text="Ingrese el número de documento")
    label_documento.pack()
    input_documento = Entry(root, width=50)
    input_documento.pack(ipady=3)

    #   PROVINCIA
    opciones_provincia = ["Madrid", "Barcelona", "Alicante"]
    click_provincia = StringVar()
    click_provincia.set(opciones_provincia[0])
    label_provincia = Label(root, text="Elija la provincia")
    label_provincia.pack()
    input_provincia = OptionMenu(root, click_provincia, *opciones_provincia)
    input_provincia.pack()

    #   TIPO DE OPERACIÓN
    opciones_tipo_operacion = ["SOLICITUD DE ASILO",
                                "SOLICITUD DE ASILO BARCELONA/ALICANTE",
                                "NUEVA NORMALIDAD",
                                "CERTIFICADOS DE RESIDENCIA",
                                "TOMA DE HUELLAS",
                                "ASIGNACIÓN DE NIE",
                                "AUTORIZACIÓN DE RESIDENCIA TEMPORAL POR ARRAIGO",
                                ]
    click_tipo_operacion = StringVar()
    click_tipo_operacion.set(opciones_tipo_operacion[0])
    label_tipo_operacion = Label(root, text="Elija el tipo de operación")
    label_tipo_operacion.pack()
    input_tipo_operacion = OptionMenu(root, click_tipo_operacion, *opciones_tipo_operacion)
    input_tipo_operacion.pack()

    myButton = Button(root, text="Buscar Cita", command=enviar_datos, fg="black", bg="cyan")
    myButton.pack(pady=10)

    # if "--autofill" not in sys.argv:
    #     try_cita(context=customer, cycles=200)  # Try 200 times
    # else:
    #     from mako.template import Template

    #     tpl = Template(
    #         filename=os.path.join(
    #             os.path.dirname(os.path.abspath(__file__)), "bcncita/template/autofill.mako"
    #         )
    #     )
    #     print(tpl.render(ctx=customer))  # Autofill for Chrome

root.mainloop()

# In Terminal run:
#   python3 example1.py
# or:
#   python3 example1.py --autofill
