import factory
from accounts.models import User, Merchant, Product, Service, Promotion


class UserFactory(factory.django.DjangoModelFactory):
    pk = factory.Sequence(lambda n: n)
    email = factory.Faker("email")
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")

    class Meta:
        model = User
        skip_postgeneration_save = True

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("testpassword")

        if create:
            self.save()


class MerchantFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Merchant


class ProductFactory(factory.django.DjangoModelFactory):
    merchant = factory.SubFactory(MerchantFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Product


class ServiceFactory(factory.django.DjangoModelFactory):
    merchant = factory.SubFactory(MerchantFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Service


class PromotionFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    service = factory.SubFactory(ServiceFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Promotion
