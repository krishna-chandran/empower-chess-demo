from django.core.management.base import BaseCommand
from django.db import IntegrityError
from classRoom.models import Role, Feature, Permission

class Command(BaseCommand):
    help = 'Populate default roles, features, and permissions'

    def handle(self, *args, **options):
        # Define default roles
        default_roles = ['Teacher', 'Student','Admin']

        default_features = [
            'View Users', 'View User', 'Add User', 'Edit User', 'Delete User',
            'View Subscriptions', 'View Subscription', 'Add Subscription', 'Edit Subscription', 'Delete Subscription',
            'View Features', 'View Feature', 'Add Feature', 'Edit Feature', 'Delete Feature',
            'View Roles', 'View Role', 'Add Role', 'Edit Role', 'Delete Role',
            'View Permissions', 'View Permission', 'Add Permission', 'Edit Permission', 'Delete Permission',
            'View Courses', 'View Course', 'Add Course', 'Edit Course', 'Delete Course',
            'View Enrollments', 'View Enrollment', 'Add Enrollment', 'Edit Enrollment', 'Delete Enrollment',
            'View Assignments', 'View Assignment', 'Add Assignment', 'Edit Assignment', 'Delete Assignment',
            'View Userassignments', 'View Userassignment', 'Add Userassignment', 'Edit Userassignment', 'Delete Userassignment'
        ]
        
        permission_sql_statements = [
            ('26', '1'), ('27', '1'), ('28', '1'), ('29', '1'), ('30', '1'),
            ('31', '1'), ('32', '1'), ('33', '1'), ('34', '1'), ('35', '1'),
            ('36', '1'), ('37', '1'), ('38', '1'), ('39', '1'), ('40', '1'),
            ('41', '1'), ('42', '1'), ('43', '1'), ('44', '1'), ('45', '1'),
            ('26', '2'), ('27', '2'), ('36', '2'), ('37', '2')
        ]

        for role_name in default_roles:
            try:
                Role.objects.create(role_name=role_name)
                self.stdout.write(self.style.SUCCESS(f'Successfully created role: {role_name}'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Role already exists: {role_name}'))

        # Populate default features
        for feature_name in default_features:
            try:
                Feature.objects.create(feature_name=feature_name)
                self.stdout.write(self.style.SUCCESS(f'Successfully created feature: {feature_name}'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Feature already exists: {feature_name}'))

        for feature_id, role_id in permission_sql_statements:
            try:
                feature = Feature.objects.get(id=feature_id)
                role = Role.objects.get(id=role_id)
                permission, created = Permission.objects.get_or_create(role=role, feature=feature)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created permission for feature_id: {feature_id} and role_id: {role_id}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Permission already exists for feature_id: {feature_id} and role_id: {role_id}'))
            except Feature.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Feature with ID {feature_id} does not exist'))
            except Role.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Role with ID {role_id} does not exist'))
