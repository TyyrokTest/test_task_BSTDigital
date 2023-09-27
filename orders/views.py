from django.shortcuts import render
from django.views import View
from orders.forms import OrderForm
from orders.models import Order
from robots.models import Robot
from customers.models import Customer

class AddOrderView(View):
    
    form_class = OrderForm
    template_name = 'add_order.html'
    
    MESSAGE_ALREADY_IN_STOCK = """У нас на складе имеется необходимый вам робот, 
                                  обратитесь в отдел продаж!"""
    MESSAGE_SUCCESS_ORDER = "Ваш заказ успешно создан! Ожидайте email при поступлении"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if not form.is_valid():  
            return render(request, self.template_name, {"form": form})
        
        robot_in_stock = Robot.objects.filter(serial=form.cleaned_data['robot_serial'])
        
        if len(robot_in_stock) > 0:
            form = self.form_class()
            return render(request, self.template_name, 
                          {"form": form, "success_message": self.MESSAGE_ALREADY_IN_STOCK})
            
        else:
            customer, status = Customer.objects.get_or_create(
                                 email=form.cleaned_data['customer']
            )
            Order.objects.create(customer=customer, 
                                 robot_serial=form.cleaned_data['robot_serial']
            )
            form = self.form_class()
            return render(request, self.template_name, 
                          {"form": form, "success_message": self.MESSAGE_SUCCESS_ORDER})