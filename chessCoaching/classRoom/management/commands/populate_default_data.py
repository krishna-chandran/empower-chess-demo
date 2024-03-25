from django.core.management.base import BaseCommand
from django.db import IntegrityError
from classRoom.models import Role, Feature, Permission
from django.contrib.auth.models import User

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
            'View Userassignments', 'View Userassignment', 'Add Userassignment', 'Edit Userassignment', 'Delete Userassignment',
            'View Packages', 'View Package', 'Add Package', 'Edit Package', 'Delete Package',
            'View Package Options', 'View Package Option', 'Add Package Option', 'Edit Package Option', 'Delete Package Option',    
            'View Settings', 'View Setting' , 'Add Setting', 'Edit Setting', 'Delete Setting',
            'Learn Courses', 
        ]
        
        permission_sql_statements = [
            ('26', '1'), ('27', '1'), ('28', '1'), ('29', '1'), ('30', '1'),
            ('31', '1'), ('32', '1'), ('33', '1'), ('34', '1'), ('35', '1'),
            ('36', '1'), ('37', '1'), ('38', '1'), ('39', '1'), ('40', '1'),
            ('41', '1'), ('42', '1'), ('43', '1'), ('44', '1'), ('45', '1'),
            ('26', '2'), ('27', '2'), ('36', '2'), ('37', '2'),
            ('1', '3'), ('2', '3'), ('3', '3'), ('4', '3'), ('5', '3'),
            ('6', '3'), ('7', '3'), ('8', '3'), ('9', '3'), ('10', '3'),
            ('11', '3'), ('12', '3'), ('13', '3'), ('14', '3'), ('15', '3'),
            ('16', '3'), ('17', '3'), ('18', '3'), ('19', '3'), ('20', '3'),
            ('21', '3'), ('22', '3'), ('23', '3'), ('24', '3'), ('25', '3'),
            ('26', '3'), ('27', '3'), ('28', '3'), ('29', '3'), ('30', '3'),
            ('31', '3'), ('32', '3'), ('33', '3'), ('34', '3'), ('35', '3'),
            ('36', '3'), ('37', '3'), ('38', '3'), ('39', '3'), ('40', '3'),
            ('41', '3'), ('42', '3'), ('43', '3'), ('44', '3'), ('45', '3'),
            ('46', '3'), ('47', '3'), ('48', '3'), ('49', '3'), ('50', '3'),
            ('51', '3'), ('52', '3'), ('53', '3'), ('54', '3'), ('55', '3'),
            ('56', '3'), ('57', '3'), ('58', '3'), ('59', '3'), ('60', '3'),
            ('61', '2'),
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

        # Create a default superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            admin_username = 'admin'
            admin_email = 'admin@example.com'
            admin_password = '1234'
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            self.stdout.write(self.style.SUCCESS('Default superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Default superuser already exists'))