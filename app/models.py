from marshmallow import Schema, fields, validate, ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError("Must be a positive number.")

class OrderSchema(Schema):
    order_id = fields.String(required=True)
    user_id = fields.Integer(required=True)
    item_ids = fields.List(fields.Integer(), required=True)
    total_amount = fields.Float(required=True, validate=validate.Range(min=0))
    status = fields.String(
        required=False, 
        validate=validate.OneOf(["Pending", "Processing", "Completed"]),
        default="Pending"
    )


class OrderStatusResponseSchema(Schema):
    order_id = fields.Str(required=True)
    status = fields.Str(required=True)