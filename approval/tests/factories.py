"""Collection of factory classes for approval models"""
import factory
import functools
from decimal import Decimal

from approval.basemodel import Tenant
from approval.models import (
    Template,
    Workflow,
    Request,
    Action,
)

def default_tenant():
    current = Tenant.current()
    if current == None:
        current = Tenant.objects.create(external_tenant="default")
    return current


class TenantFactory(factory.django.DjangoModelFactory):
    """Tenant factory class"""

    class Meta:
        model = Tenant

    external_tenant = factory.Sequence(lambda n: f"external{n}")


class TemplateFactory(factory.django.DjangoModelFactory):
    """Template factory class"""

    class Meta:
        model = Template

    tenant = factory.LazyAttribute(lambda _: default_tenant())
    title = factory.Sequence(lambda n: f"title{n}")
    description = factory.Sequence(lambda n: f"title{n}_description")


class WorkflowFactory(factory.django.DjangoModelFactory):
    """Workflow factory class"""

    class Meta:
        model = Workflow

    tenant = factory.LazyAttribute(lambda _: default_tenant())
    template = factory.SubFactory(TemplateFactory)
    name = factory.Sequence(lambda n: f"workflow{n}")
    description = factory.Sequence(lambda n: f"workflow{n}_description")
    internal_sequence = factory.Sequence(lambda n: Decimal(n))


class RequestFactory(factory.django.DjangoModelFactory):
    """Request factory class"""

    class Meta:
        model = Request
    
    tenant = factory.LazyAttribute(lambda _: default_tenant())
    workflow = factory.SubFactory(WorkflowFactory)


class ActionFactory(factory.django.DjangoModelFactory):
    """Action factory class"""

    class Meta:
        model = Action
    
    tenant = factory.LazyAttribute(lambda _: default_tenant())
    request = factory.SubFactory(RequestFactory)
