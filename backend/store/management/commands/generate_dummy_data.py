import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Problem, UnitType, SectionType, PreviewImage
from faker import Faker
from decimal import Decimal

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generates dummy data for store app"

    def create_dummy_user(self):
        email = fake.email()
        password = "test12345"
        user, created = User.objects.get_or_create(
            email=email, defaults={"username": fake.user_name(), "is_active": True}
        )
        if created:
            user.set_password(password)
            user.save()
        return user

    def create_unit_types(self):
        subjects = ["Math", "Science", "Liberal Arts", "English", "STEM", "SAT"]
        unit_types = []
        for subject in subjects:
            for _ in range(3):
                name = f"{subject} Unit {fake.word().capitalize()}"
                unit_type, _ = UnitType.objects.get_or_create(
                    name=name, subject=subject
                )
                unit_types.append(unit_type)
        return unit_types

    def create_section_types(self):
        subjects = ["Math", "Science", "Liberal Arts", "English", "STEM", "SAT"]
        section_types = []
        for subject in subjects:
            for _ in range(3):
                name = f"{subject} Section {fake.word().capitalize()}"
                section_type, _ = SectionType.objects.get_or_create(
                    name=name, subject=subject
                )
                section_types.append(section_type)
        return section_types

    def create_dummy_problem(self, user, unit_types, section_types):
        problem = Problem.objects.create(
            user=user,
            subject=random.choice(
                ["Math", "Science", "Liberal Arts", "English", "STEM", "SAT"]
            ),
            problem_type=random.choice(["Normal", "Premium", "Best"]),
            type=random.choice(
                ["Multiple Choice", "Short Answer", "Mathematical Modeling"]
            ),
            grade=random.choice(
                [
                    "Kindergarten",
                    "USA grade 1",
                    "USA grade 2",
                    "USA grade 3",
                    "USA grade 4",
                    "USA grade 5",
                    "Algebra 1",
                    "Geometry",
                ]
            ),
            difficulty=random.choice([1, 2, 3]),
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            price=Decimal(str(random.uniform(5.0, 100.0))),
            discounted_price=Decimal(str(random.uniform(1.0, 4.99))),
            is_free=random.choice([True, False]),
            is_view=random.choice([True, False]),
            pages=random.randint(1, 50),
            problems=random.randint(1, 20),
        )

        # Add random unit types and section types
        problem.unit.set(random.sample(unit_types, random.randint(1, 3)))
        problem.detailed_section.set(random.sample(section_types, random.randint(1, 3)))

        return problem

    def create_preview_image(self, problem):
        PreviewImage.objects.create(problem=problem, image_url=fake.image_url())

    def handle(self, *args, **options):
        self.stdout.write("Creating dummy data...")

        # Create dummy users
        users = [self.create_dummy_user() for _ in range(10)]

        # Create unit types and section types
        unit_types = self.create_unit_types()
        section_types = self.create_section_types()

        # Create problems with preview images
        for _ in range(400):
            user = random.choice(users)
            problem = self.create_dummy_problem(user, unit_types, section_types)

            # Create 1-3 preview images for each problem
            for _ in range(random.randint(1, 3)):
                self.create_preview_image(problem)

        self.stdout.write(self.style.SUCCESS("Successfully created dummy data"))
