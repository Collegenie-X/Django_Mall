from django.core.exceptions import ValidationError


class ProblemValidators:
    @staticmethod
    def validate_price(instance):
        if not (1 <= instance.price <= 3000):
            raise ValidationError("Price must be between $5 and $100.")

    @staticmethod
    def validate_discounted_price(instance):
        if instance.discounted_price is not None:
            if not (0 <= instance.discounted_price < instance.price):
                raise ValidationError(
                    "Discounted price must be between $1 and less than the original price."
                )
