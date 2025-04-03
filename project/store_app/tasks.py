import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Category, Product
from django.core.exceptions import ObjectDoesNotExist
import smtplib
from socket import gaierror

logger = logging.getLogger(__name__)

DEFAULT_RECIPIENT = getattr(settings, "ADMIN_EMAIL", "admin@example.com")


def _send_email(subject, plain_message, recipient, html_message=None):
    """Вспомогательная функция для отправки email с обработкой ошибок"""
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except smtplib.SMTPException as e:
        logger.error(f"SMTP ошибка при отправке email: {str(e)}")
        raise
    except gaierror as e:
        logger.error(f"Ошибка сети при отправке email: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке email: {str(e)}")
        raise


@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True)
def send_category_notification(self, action, category_id, recipient_email=None):
    """Отправляет уведомление об изменении категории"""
    try:
        category = Category.objects.get(id=category_id)
        recipient = recipient_email or DEFAULT_RECIPIENT
        subject = f"Категория '{category.name}' была {action}"

        context = {
            "action": action,
            "category": category,
            "subject": subject,
        }

        html_message = render_to_string("emails/category_notification.html", context)
        plain_message = strip_tags(html_message)

        if _send_email(subject, plain_message, recipient, html_message):
            logger.info(f"Уведомление о категории отправлено на {recipient}")
            return f"Category notification sent to {recipient}"

    except ObjectDoesNotExist as e:
        logger.error(f"Категория {category_id} не найдена: {str(e)}")
        raise self.retry(exc=e, countdown=120)
    except Exception as e:
        logger.error(f"Ошибка в задаче send_category_notification: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True)
def send_product_notification(self, action, product_id, recipient_email=None):
    """Отправляет уведомление об изменении товара"""
    try:
        product = Product.objects.get(id=product_id)
        recipient = recipient_email or DEFAULT_RECIPIENT
        subject = f"Товар '{product.name}' был {action}"

        context = {
            "action": action,
            "product": product,
            "subject": subject,
        }

        html_message = render_to_string("emails/product_notification.html", context)
        plain_message = strip_tags(html_message)

        if _send_email(subject, plain_message, recipient, html_message):
            logger.info(f"Уведомление о товаре отправлено на {recipient}")
            return f"Product notification sent to {recipient}"

    except ObjectDoesNotExist as e:
        logger.error(f"Товар {product_id} не найден: {str(e)}")
        raise self.retry(exc=e, countdown=120)
    except Exception as e:
        logger.error(f"Ошибка в задаче send_product_notification: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True)
def send_bulk_update_notification(self, updated_items):
    """Отправляет сводное уведомление о массовых изменениях"""
    if not updated_items:
        logger.warning("Пустой список изменений для уведомления")
        return "No updates to notify about"

    try:
        changes = {"products": [], "categories": []}

        for item in updated_items:
            try:
                if item["type"] == "product":
                    product = Product.objects.get(id=item["id"])
                    changes["products"].append(
                        {
                            "name": product.name,
                            "action": item["action"],
                            "id": product.id,
                        }
                    )
                elif item["type"] == "category":
                    category = Category.objects.get(id=item["id"])
                    changes["categories"].append(
                        {
                            "name": category.name,
                            "action": item["action"],
                            "id": category.id,
                        }
                    )
            except ObjectDoesNotExist:
                continue

        if not changes["products"] and not changes["categories"]:
            logger.warning("Нет действительных изменений для уведомления")
            return "No valid updates to notify"

        subject = "Сводка изменений в каталоге"
        context = {
            "changes": changes,
            "subject": subject,
        }

        html_message = render_to_string("emails/bulk_update_notification.html", context)
        plain_message = strip_tags(html_message)

        if _send_email(subject, plain_message, DEFAULT_RECIPIENT, html_message):
            logger.info(f"Сводное уведомление отправлено на {DEFAULT_RECIPIENT}")
            return f"Bulk update notification sent to {DEFAULT_RECIPIENT}"

    except Exception as e:
        logger.error(f"Ошибка в задаче send_bulk_update_notification: {str(e)}")
        raise self.retry(exc=e, countdown=60)
