import factory
from accounts.models import User, Merchant, Product, Service, Promotion, Category, Hashtag, Keyword


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
        skip_postgeneration_save = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            self.categories.add(*CategoryFactory.create_batch(3))

    @factory.post_generation
    def hashtags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for hashtag in extracted:
                self.hashtags.add(hashtag)
        else:
            self.hashtags.add(*HashtagFactory.create_batch(3))

    @factory.post_generation
    def keywords(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for keyword in extracted:
                self.keywords.add(keyword)
        else:
            self.keywords.add(*KeywordFactory.create_batch(3))


class ServiceFactory(factory.django.DjangoModelFactory):
    merchant = factory.SubFactory(MerchantFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Service
        skip_postgeneration_save = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            self.categories.add(*CategoryFactory.create_batch(3))

    @factory.post_generation
    def hashtags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for hashtag in extracted:
                self.hashtags.add(hashtag)
        else:
            self.hashtags.add(*HashtagFactory.create_batch(3))

    @factory.post_generation
    def keywords(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for keyword in extracted:
                self.keywords.add(keyword)
        else:
            self.keywords.add(*KeywordFactory.create_batch(3))


class PromotionFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    service = factory.SubFactory(ServiceFactory)
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Promotion
        skip_postgeneration_save = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            self.categories.add(*CategoryFactory.create_batch(3))

    @factory.post_generation
    def hashtags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for hashtag in extracted:
                self.hashtags.add(hashtag)
        else:
            self.hashtags.add(*HashtagFactory.create_batch(3))

    @factory.post_generation
    def keywords(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for keyword in extracted:
                self.keywords.add(keyword)
        else:
            self.keywords.add(*KeywordFactory.create_batch(3))


class CategoryFactory(factory.django.DjangoModelFactory):
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Category


class HashtagFactory(factory.django.DjangoModelFactory):
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Hashtag


class KeywordFactory(factory.django.DjangoModelFactory):
    pk = factory.Sequence(lambda n: n)
    name = factory.Faker("name")

    class Meta:
        model = Keyword
