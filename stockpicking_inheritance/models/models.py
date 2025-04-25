from odoo import models, fields
# import barcode
# from barcode.writer import ImageWriter
# from io import BytesIO
# import base64

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # def get_barcode_img(self):
    #     """Generate barcode image for the picking."""
    #     # Assuming 'name' or any field as the barcode value. Adjust accordingly.
    #     barcode_data = self.name
        
    #     # Generate barcode using python-barcode
    #     barcode_class = barcode.get_barcode_class('code128')  # or use a different type of barcode
    #     barcode_obj = barcode_class(barcode_data, writer=ImageWriter())
        
    #     # Save barcode image to memory
    #     img_io = BytesIO()
    #     barcode_obj.write(img_io)
    #     img_io.seek(0)

    #     # Convert image to base64
    #     img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    #     return img_base64
