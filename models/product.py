from pydantic import BaseModel

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
    
    def to_dict(self):
       return {"product_title": self.product_title, "product_price": self.product_price, "path_to_image": self.path_to_image}