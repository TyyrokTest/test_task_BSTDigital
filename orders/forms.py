from django.forms import ModelForm, EmailField, CharField, Form
from orders.models import Order
from orders.validators import validate_serial

class OrderForm(Form):
    customer = EmailField(required=True, label="Email")
    robot_serial = CharField(required=True, 
                             max_length=5, 
                             min_length=5, 
                             label="Серийный номер робота",
                             validators=[validate_serial]
    )

    