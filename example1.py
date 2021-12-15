import os
import sys

from bcncita import CustomerProfile, DocType, Office, OperationType, Province, try_cita

if __name__ == "__main__":
    customer = CustomerProfile(
        anticaptcha_api_key="... your key here ...",  # Anti-captcha API Key (auto_captcha=False to disable it)
        auto_captcha=False,  # Enable anti-captcha plugin (if False, you have to solve reCaptcha manually and press ENTER in the Terminal)
        auto_office=True,
        chrome_driver_path="C:/Users/Usuario/AppData/Local/Programs/Python/Python38/chromedriver",
        save_artifacts=True,  # Record available offices / take available slots screenshot
        province=Province.MADRID,
        operation_code=OperationType.SOLICITUD_ASILO,
        doc_type=DocType.PASSPORT,  # DocType.NIE or DocType.PASSPORT
        doc_value="1111111",  # NIE or Passport number, no spaces.
        year_of_birth = "2000",
        country="RUSIA",
        name="BORIS JOHNSON",  # Your Name
        phone="600000000",  # Phone number (use this format, please)
        email="myemail@here.com",  # Email
        # Offices in order of preference
        # This selects specified offices one by one or a random one if not found.
        # For recogida only the first specified office will be attempted or none
        offices=[],
    )
    if "--autofill" not in sys.argv:
        try_cita(context=customer, cycles=200)  # Try 200 times
    else:
        from mako.template import Template

        tpl = Template(
            filename=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "bcncita/template/autofill.mako"
            )
        )
        print(tpl.render(ctx=customer))  # Autofill for Chrome


# In Terminal run:
#   python3 example1.py
# or:
#   python3 example1.py --autofill
