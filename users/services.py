import stripe
from django.conf import settings
from materials.models import Course, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(course, lesson, amount):
    """
    Создаёт Stripe-сессию оплаты для курса или урока.
    """
    product_name = course.title if course else lesson.title
    stripe_amount = int(amount * 100)  # в копейках

    # создаём продукт и цену
    product = stripe.Product.create(name=product_name)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=stripe_amount,
        currency="rub",
    )

    # создаём сессию
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )

    return session.url


