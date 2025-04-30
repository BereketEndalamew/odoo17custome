# -*- coding: utf-8 -*-

import base64
import io
from odoo import models


class PatientCardXlsx1(models.AbstractModel):
    _name = 'report.hospitalsystem.report_patient_id_card_xls'

    def generate_xlsx_report(self, workbook, data, patients):
        bold = workbook.add_format({'bold': True})

        for obj in patients:
            sheet = workbook.add_worksheet(obj.name or "Patient")
            row = 0
            col = 0
            sheet.set_column('A:A', 15)
            sheet.set_column('B:B', 25)

            row += 1
            sheet.merge_range(row, col, row, col + 1, 'ID Card', format_1)
            row += 1

            # Uncomment this block if you want to add the image
            # if obj.image:
            #     patient_image = io.BytesIO(base64.b64decode(obj.image))
            #     sheet.insert_image(row, col, "image.png", {
            #         'image_data': patient_image,
            #         'x_scale': 0.5,
            #         'y_scale': 0.5
            #     })
            #     row += 6

            sheet.write(row, col, 'Name', bold)
            sheet.write(row + 1, col, obj.name or '')
            col += 1

            sheet.write(row, col, 'Age', bold)
            sheet.write(row + 1, col, obj.age or '')
            col += 1

            sheet.write(row, col, 'Gender', bold)
            sheet.write(row + 1, col, obj.gender or '')
            col += 1

            sheet.write(row, col, 'Phone Number', bold)
            sheet.write(row + 1, col, obj.phone or '')
            col += 1

            sheet.write(row, col, 'Email', bold)
            sheet.write(row + 1, col, obj.email or '')
            col += 1

            sheet.write(row, col, 'Country', bold)
            sheet.write(row + 1, col, obj.country_id.name if obj.country_id else '')
            col += 1

            sheet.merge_range(row, col, row + 1, col + 1, '', format_1)
