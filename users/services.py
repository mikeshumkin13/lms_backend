import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(payment):
    """
    Создаёт Stripe-сессию оплаты для курса или урока.
    """
    # Определяем название и цену
    product_name = payment.course.name if payment.course else payment.lesson.name
    amount = int(payment.amount * 100)  # В копейках

    # Создаём продукт в Stripe
    product = stripe.Product.create(name=product_name)

    # Создаём цену для продукта
    price = stripe.Price.create(
        product=product.id,
        unit_amount=amount,
        currency="rub",
    )

    # Создаём сессию оплаты
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url="https://example.com/success",  # тут можно потом сделать свою ссылку
        cancel_url="https://example.com/cancel",    # тут тоже
    )

    return session.url


