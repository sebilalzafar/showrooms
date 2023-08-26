from django import forms
from .models import Product , Categories , Showrooms , Company_name,showroom_settings





class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["id", "showroom",'title', 'company_name',"category","product_number" ,"imported_or_local" , "unit_or_sqm", "old_price" ,"new_price",
                  "discount_price",  'description', 'image']
        exclude =["showroom","id"]
        labels = {
            "old_price": "Tag Price",
            "new_price": "Sale Price",
            # Add label changes for other fields here
        }
        
    def __init__(self, user  , *args, **kwargs ):
        super().__init__(*args, **kwargs)
        showroom = Showrooms.objects.get(id=user.id)
        self.fields['category'].queryset =     Categories.objects.filter(showroom_type=showroom.showroom_type)
        self.fields['company_name'].queryset = Company_name.objects.filter(showroom_type=showroom.showroom_type)

        
        
     
class SettingsForm(forms.ModelForm):
    class Meta :
        model = showroom_settings
        fields = "__all__"
        exclude =["showroom"]
        
        
        
        


  