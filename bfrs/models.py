#from django.db import models
from django.contrib.gis.db import models
from datetime import datetime, timedelta
from django.utils import timezone
#from pbs.prescription.models import (Prescription, Region, District)
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator
#from smart_selects.db_fields import ChainedForeignKey
from bfrs.base import Audit
from django.core.exceptions import (ValidationError)

import sys
import json

AUTH_TYPE_CHOICES = (
    (1, 'Initial'),
    (2, 'Final'),
)

def current_finyear():
	return datetime.now().year if datetime.now().month>7 else datetime.now().year-1


class Profile(models.Model):
    DEFAULT_GROUP = "Users"

    user = models.OneToOneField(User, related_name='profile')
    region = models.ForeignKey('Region', blank=True, null=True)
    district = ChainedForeignKey('District',
        chained_field="region", chained_model_field="region",
        show_all=False, auto_choose=True, blank=True, null=True)

    def __str__(self):
        return 'Profile of user: {} - {} - {}'.format(self.user.username, self.region, self.district)

    class Meta:
        default_permissions = ('add', 'change', 'view')


@python_2_unicode_compatible
class Prescription(models.Model):
    burn_id = models.CharField(max_length=7)

    class Meta:
        ordering = ['burn_id']

    def __str__(self):
        return self.burn_id


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class District(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=3)
    archive_date = models.DateField(
        null=True, blank=True, help_text="Archive this District (prevent from creating new ePFPs)"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


#class Bushfire(Audit):
#    # OriginFDGRID
#    COORD_TYPE_MGAZONE = 1
#    COORD_TYPE_LATLONG = 2
#    COORD_TYPE_FDGRID = 3
#    COORD_TYPE_CHOICES = (
#        (COORD_TYPE_MGAZONE, 'MGA'),
#        (COORD_TYPE_LATLONG, 'Lat/Long'),
#        (COORD_TYPE_FDGRID, 'FD Grid'),
#    )
#
#    CAUSE_CHOICES = (
#        (1, 'Known'),
#        (2, 'Possible'),
#    )
#
#    FIRE_LEVEL_CHOICES = (
#        (1, 1),
#        (2, 2),
#        (3, 3),
#    )
#
#    region = models.ForeignKey(Region)
##    district = models.ForeignKey(District)
#    district = ChainedForeignKey(
#        District, chained_field="region", chained_model_field="region",
#        show_all=False, auto_choose=True)
#
#    name = models.CharField(max_length=100, verbose_name="Fire Name")
#    incident_no = models.CharField(verbose_name="Fire Incident No.", max_length=10)
#    season = models.CharField(max_length=9)
#    dfes_incident_no = models.CharField(verbose_name="DFES Incident No.", max_length=10, null=True, blank=True)
#    job_code = models.CharField(verbose_name="Job Code", max_length=10, null=True, blank=True)
#    potential_fire_level = models.PositiveSmallIntegerField(choices=FIRE_LEVEL_CHOICES, null=True, blank=True)
#    field_officer = models.ForeignKey(User, verbose_name="Field Officer", null=True, blank=True, related_name='init_field_officer')
#    init_authorised_by = models.ForeignKey(User, verbose_name="Authorised By", blank=True, null=True, related_name='init_auth_by')
#    init_authorised_date = models.DateTimeField(verbose_name='Authorised Date', default=timezone.now, null=True, blank=True)
#
#    # Cause
#    cause = models.ForeignKey('Cause', null=True, blank=True)
#    known_possible = models.PositiveSmallIntegerField(choices=CAUSE_CHOICES, verbose_name="Known/Possible", null=True, blank=True)
#    other_cause = models.CharField(verbose_name='Other Cause', max_length=50, null=True, blank=True)
#    investigation_req = models.BooleanField(verbose_name="Invest'n Required", default=False)
#
#    # First Attack Agency (Part only)
#    first_attack = models.ForeignKey('Agency', verbose_name="First Attack Agency", null=True, blank=True, related_name='first_attack')
#    other_first_attack = models.CharField(verbose_name="Other First Attack Agency", max_length=50, null=True, blank=True)
#
#    # Point of Origin
#    coord_type = models.PositiveSmallIntegerField(choices=COORD_TYPE_CHOICES, verbose_name="Coordinate Type", null=True, blank=True)
#    fire_not_found = models.BooleanField(default=False)
#    # TODO number of dp
#    lat_decimal = models.DecimalField(verbose_name="Latitude (Decimal)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lat_degrees = models.DecimalField(verbose_name="Latitude (Degrees)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lat_minutes = models.DecimalField(verbose_name="Latitude (Minutes)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_decimal = models.DecimalField(verbose_name="Longitude (Decimal)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_degrees = models.DecimalField(verbose_name="Longitude (Degrees)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_minutes = models.DecimalField(verbose_name="Longitude (Minutes)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#
#    mga_zone = models.DecimalField(verbose_name="MGA Zone", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    mga_easting = models.DecimalField(verbose_name="MGA Easting", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    mga_northing = models.DecimalField(verbose_name="MGA Northing", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#
#    fd_letter = models.CharField(verbose_name="FD Letter", max_length=2, null=True, blank=True)
#    fd_number = models.PositiveSmallIntegerField(verbose_name="FD Number", null=True, blank=True)
#    fd_tenths = models.CharField(verbose_name="FD Tenths", max_length=2, null=True, blank=True)
#
#    # Activities - Formset
#    # Tenure and Vegetation Affected - Formset
#
#    # Location
#    distance = models.DecimalField(verbose_name="Distance (km)", max_digits=6, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    direction = models.ForeignKey('Direction', verbose_name="Direction", null=True, blank=True)
#    place = models.CharField(max_length=25, null=True, blank=True)
#    lot_no = models.CharField(verbose_name="Lot Number", max_length=10, null=True, blank=True)
#    street = models.CharField(max_length=25, null=True, blank=True)
#    town = models.CharField(max_length=25, null=True, blank=True)
#
#    # Forces in Attendance - Formset
#
#    # Operation Details
#    fuel = models.CharField(max_length=50, null=True, blank=True)
#    ros = models.CharField(verbose_name="Rate of Spread", max_length=50, null=True, blank=True)
#    flame_height = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
#    assistance_required = models.CharField(max_length=50, null=True, blank=True)
#    fire_contained = models.BooleanField(default=False)
#    containment_time = models.CharField(verbose_name="ET to Contain", max_length=50, null=True, blank=True)
#    ops_point = models.CharField(verbose_name="OPS Point (grid ref)", max_length=50, null=True, blank=True)
#    communications = models.CharField(verbose_name='Communication', max_length=50, null=True, blank=True)
#    weather = models.CharField(max_length=50, null=True, blank=True)
#
#    initial_snapshot = models.TextField(null=True, blank=True)
#
#    # FINAL Report Fields
#    authorised_by = models.ForeignKey(User, verbose_name="Authorised By", blank=True, null=True)
#    authorised_date = models.DateTimeField(verbose_name='Authorised Date', default=timezone.now, null=True, blank=True)
#
#    # Reporter
#    source = models.ForeignKey('Source', verbose_name="Reported By", null=True, blank=True)
#    arson_squad_notified = models.BooleanField(verbose_name="Arson Squad Notified", default=False)
#    #prescription = models.ForeignKey(Prescription, verbose_name="ePFP (if cause is Escape)", related_name='prescribed_burn', null=True, blank=True)
#    prescription = models.ForeignKey('Prescription', verbose_name="Pres Burn ID", null=True, blank=True)
#    offence_no = models.CharField(verbose_name="Offence No.", max_length=10, null=True, blank=True)
#
#
#    # Effect
#    frb_effect = models.ForeignKey('FrbEffect', verbose_name='Presence/Effect of FRB', null=True, blank=True)
#    fire_stopped = models.PositiveSmallIntegerField(verbose_name="Fuel Age - Fire Stopped (Yr)", null=True, blank=True)
#    waterbomb_effect = models.ForeignKey('WaterBombEffect', verbose_name='Presence/Effect of WaterBomb', null=True, blank=True)
#    last_burnt = models.PositiveSmallIntegerField(verbose_name="Fuel Age - Area Last Burnt (Yr)", null=True, blank=True)
#    arrival_area = models.DecimalField(verbose_name="Fire Area at Arrival (ha)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    fire_level = models.PositiveSmallIntegerField(verbose_name='Final Fire Level', choices=FIRE_LEVEL_CHOICES, null=True, blank=True)
#    rating = models.ForeignKey('PriorityRating', verbose_name="Area Priority Rating", null=True, blank=True)
#
#    # First Attack
#    hazard_mgt = models.ForeignKey('Agency', verbose_name="Hazard Management Agency", null=True, blank=True, related_name='hazard_mgt')
#    other_hazard_mgt = models.CharField(verbose_name="Other Hazard Mgt Agency", max_length=50, null=True, blank=True)
#    initial_control = models.ForeignKey('Agency', verbose_name="Initial Controlling Agency", null=True, blank=True, related_name='initial_control')
#    other_initial_ctrl = models.CharField(verbose_name="Other Initial Control Agency", max_length=50, null=True, blank=True)
#    final_control = models.ForeignKey('Agency', verbose_name="Final Controlling Agency", null=True, blank=True, related_name='final_control')
#    other_final_ctrl = models.CharField(verbose_name="Other Final Control Agency", max_length=50, null=True, blank=True)
#    #other_agency = models.CharField(verbose_name="Other Agency", max_length=50, null=True, blank=True)
#
#
#
##    def save(self, *args, **kwargs):
##        '''Overide save() to cleanse text input fields.
##        '''
##        self.name = unidecode(unicode(self.name))
##        if self.description:
##            self.description = unidecode(unicode(self.description))
##        super(Bushfire, self).save()
#
#    @property
#    def has_init_authorised(self):
#        return True if self.init_authorised_by and self.init_authorised_date else False
#
#    @property
#    def snapshot(self):
#        return json.loads(self.initial_snapshot) if self.has_init_authorised else None
#
#    def user_unicode_patch(self):
#        """ overwrite the User model's __unicode__() method """
#        if self.first_name or self.last_name:
#            return '%s %s' % (self.first_name, self.last_name)
#        return self.username
#    User.__unicode__ = user_unicode_patch
#
#    class Meta:
#        unique_together = ('district', 'incident_no', 'season')
#        default_permissions = ('add', 'change', 'delete', 'view')
#
#    def __str__(self):
#        return ', '.join([self.name, self.district.name, self.season, self.incident_no])


class Bushfire(Audit):
    # OriginFDGRID
    COORD_TYPE_MGAZONE = 1
    COORD_TYPE_LATLONG = 2
    COORD_TYPE_FDGRID = 3
    COORD_TYPE_CHOICES = (
        (COORD_TYPE_MGAZONE, 'MGA'),
        (COORD_TYPE_LATLONG, 'Lat/Long'),
        (COORD_TYPE_FDGRID, 'FD Grid'),
    )

    REPORT_STATUS_CHOICES = (
        (1, 'Initial'),
        (2, 'Final'), # Initial Authorised == Final Draft
        (3, 'Final Authorised'),
    )

#    CAUSE_CHOICES = (
#        (1, 'Known'),
#        (2, 'Possible'),
#    )

    PW_RESOURCE_CHOICES = (
        (1, 'No'),
        (2, 'Yes'),
        (3, 'Monitored Remotely'),
    )

    ALERT_LEVEL_CHOICES = (
        (1, 'Emergency/Watch'),
        (2, 'Act/Advice'),
    )

    FIRE_LEVEL_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )

    # Common Fields
    region = models.ForeignKey(Region)
    district = ChainedForeignKey(
        District, chained_field="region", chained_model_field="region",
        show_all=False, auto_choose=True)

    name = models.CharField(max_length=100, verbose_name="Fire Name")
    incident_no = models.PositiveIntegerField(verbose_name="Fire Number")
    year = models.PositiveIntegerField(verbose_name="Year", default=current_finyear(), validators=[MinValueValidator(current_finyear())])
    dfes_incident_no = models.PositiveIntegerField(verbose_name="DFES Fire Number", null=True, blank=True)
    job_code = models.PositiveIntegerField(verbose_name="job Code", null=True, blank=True)


    # Initial Fire Report
    potential_fire_level = models.PositiveSmallIntegerField(choices=FIRE_LEVEL_CHOICES, null=True, blank=True)
    alert_level = models.PositiveSmallIntegerField(verbose_name="Alert Level", choices=ALERT_LEVEL_CHOICES, null=True, blank=True)
    media_alert_req = models.BooleanField(verbose_name="Media Alert Required", default=False)
    fire_position = models.CharField(verbose_name="Position of Fire", max_length=100, null=True, blank=True)

    # Point of Origin
    origin_point = models.PointField(null=True, blank=True, editable=False, help_text='Optional.')
    fire_boundary = models.MultiPolygonField(srid=4326, null=True, blank=True, editable=False, help_text='Optional.')
    grid = models.CharField(verbose_name="Lat/Long, MGA, FD Grid", max_length=100, null=True, blank=True)
    arrival_area = models.DecimalField(verbose_name="Fire Area at Arrival (ha)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
    fire_not_found = models.BooleanField(default=False)

#    coord_type = models.PositiveSmallIntegerField(choices=COORD_TYPE_CHOICES, verbose_name="Coordinate Type", null=True, blank=True)
#    # TODO number of dp
#    lat_decimal = models.DecimalField(verbose_name="Latitude (Decimal)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lat_degrees = models.DecimalField(verbose_name="Latitude (Degrees)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lat_minutes = models.DecimalField(verbose_name="Latitude (Minutes)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_decimal = models.DecimalField(verbose_name="Longitude (Decimal)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_degrees = models.DecimalField(verbose_name="Longitude (Degrees)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    lon_minutes = models.DecimalField(verbose_name="Longitude (Minutes)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#
#    mga_zone = models.DecimalField(verbose_name="MGA Zone", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    mga_easting = models.DecimalField(verbose_name="MGA Easting", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#    mga_northing = models.DecimalField(verbose_name="MGA Northing", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
#
#    fd_letter = models.CharField(verbose_name="FD Letter", max_length=2, null=True, blank=True)
#    fd_number = models.PositiveSmallIntegerField(verbose_name="FD Number", null=True, blank=True)
#    fd_tenths = models.CharField(verbose_name="FD Tenths", max_length=2, null=True, blank=True)

    # FireBehaviour FS here
    #tenure = models.ForeignKey('Tenure', null=True, blank=True)
    #fuel = models.CharField(max_length=50, null=True, blank=True)
    assistance_req = models.BooleanField(default=False)
    communications = models.CharField(verbose_name='Communication', max_length=50, null=True, blank=True)
    other_info = models.CharField(verbose_name='Other Information', max_length=100, null=True, blank=True)
    cause = models.ForeignKey('Cause', null=True, blank=True)
    other_cause = models.CharField(verbose_name='Other Cause', max_length=50, null=True, blank=True)

    # TODO sperate days and hrs to control?
    #time_to_control = models.DateTimeField(verbose_name='Time to Control', null=True, blank=True)

    field_officer = models.ForeignKey(User, verbose_name="Field Officer", null=True, blank=True, related_name='init_field_officer')
    duty_officer = models.ForeignKey(User, verbose_name="Duty Officer", null=True, blank=True, related_name='init_duty_officer')
    init_authorised_by = models.ForeignKey(User, verbose_name="Authorised By", blank=True, null=True, related_name='init_auth_by')
    init_authorised_date = models.DateTimeField(verbose_name='Authorised Date', null=True, blank=True)

    # we serialise/snapshot the initial report when authorised
    initial_snapshot = models.TextField(null=True, blank=True)

    # below are in Activities FS
#    fire_detected_date = models.DateTimeField(verbose_name='Date Fire Detected', default=timezone.now, null=True, blank=True)
#    pw_resources_desp = models.PositiveSmallIntegerField(verbose_name="P&W Resources Despatched", choices=PW_RESOURCE_CHOICES, null=True, blank=True)
#    pw_resources_desp_date = models.DateTimeField(verbose_name='Date P&W Resources Despatched', default=timezone.now, null=True, blank=True)
#    aerial_support_desp = models.BooleanField(verbose_name="Aerial Support Despatched", default=False)
#    aerial_support_desp_date = models.DateTimeField(verbose_name='Date Aerial Support Despatched', default=timezone.now, null=True, blank=True)
#    time_to_control = models.DateTimeField(verbose_name='Time to Control', null=True, blank=True)
#    fire_contained_date = models.DateTimeField(verbose_name='Date Fire Contained', null=True, blank=True)
#    fire_controlled_date = models.DateTimeField(verbose_name='Date Fire Controlled', null=True, blank=True)
#    fire_safe_date = models.DateTimeField(verbose_name='Date Fire Safe', null=True, blank=True)

    # FINAL Fire Report Fields

    first_attack = models.ForeignKey('Agency', verbose_name="First Attack Agency", null=True, blank=True, related_name='first_attack')
    other_first_attack = models.CharField(verbose_name="Other First Attack Agency", max_length=50, null=True, blank=True)
    initial_control = models.ForeignKey('Agency', verbose_name="Initial Controlling Agency", null=True, blank=True, related_name='initial_control')
    other_initial_ctrl = models.CharField(verbose_name="Other Initial Control Agency", max_length=50, null=True, blank=True)
    final_control = models.ForeignKey('Agency', verbose_name="Final Controlling Agency", null=True, blank=True, related_name='final_control')
    other_final_ctrl = models.CharField(verbose_name="Other Final Control Agency", max_length=50, null=True, blank=True)

    max_fire_level = models.PositiveSmallIntegerField(choices=FIRE_LEVEL_CHOICES, null=True, blank=True)
    arson_squad_notified = models.BooleanField(verbose_name="Arson Squad Notified", default=False)
    offence_no = models.CharField(verbose_name="Police Offence No.", max_length=10, null=True, blank=True)
    final_area = models.DecimalField(verbose_name="Final Fire Area (ha)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)], null=True, blank=True)
    # Private Damage FS here
    # Public Damage FS here
    # Comments FS here

    authorised_by = models.ForeignKey(User, verbose_name="Authorised By", blank=True, null=True)
    authorised_date = models.DateTimeField(verbose_name='Authorised Date', default=timezone.now, null=True, blank=True)

    report_status = models.PositiveSmallIntegerField(choices=REPORT_STATUS_CHOICES, editable=False, default=1)
    sss_id = models.CharField(verbose_name="Spatial Support System ID", max_length=64, null=True, blank=True)

#    def save(self, *args, **kwargs):
#        '''Overide save() to cleanse text input fields.
#        '''
#        self.name = unidecode(unicode(self.name))
#        if self.description:
#            self.description = unidecode(unicode(self.description))
#        super(Bushfire, self).save()

    @property
    def has_init_authorised(self):
        return True if self.init_authorised_by and self.init_authorised_date else False

    @property
    def final_authorised(self):
        return True if self.authorised_by and self.authorised_date else False

    @property
    def snapshot(self):
        return json.loads(self.initial_snapshot) if self.has_init_authorised else None

    def user_unicode_patch(self):
        """ overwrite the User model's __unicode__() method """
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username
    User.__unicode__ = user_unicode_patch

    class Meta:
        #unique_together = ('district', 'incident_no', 'season')
        unique_together = ('year', 'district', 'incident_no')
        default_permissions = ('add', 'change', 'delete', 'view')

    def unique_id(self):
        return ''.join(['BF', self.district.code, str(self.year), str(self.incident_no)])

    def __str__(self):
        return ', '.join([self.name, self.district.name, self.year, self.incident_no])



@python_2_unicode_compatible
class Tenure(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class FuelType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Source(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Cause(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Direction(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=3)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class FrbEffect(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class WaterBombEffect(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PriorityRating(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Agency(models.Model):

    name = models.CharField(max_length=50, verbose_name="Agency Name")
    code = models.CharField(verbose_name="Agency Short Code", max_length=10)

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ResponseType(models.Model):

    name = models.CharField(max_length=50, verbose_name="Agency Name")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Organisation(models.Model):
    name = models.CharField(max_length=50, verbose_name="Organisation")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class InvestigationType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Investigation Type")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LegalResultType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Legal Result Type")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PublicDamageType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Public Damage Type")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PrivateDamageType(models.Model):
    name = models.CharField(max_length=25, verbose_name="Private Damage Type")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ActivityType(models.Model):
    name = models.CharField(max_length=25, verbose_name="Activity Type")

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name




@python_2_unicode_compatible
class Response(models.Model):
    bushfire = models.ForeignKey(Bushfire, related_name='responses')
    response = models.ForeignKey(ResponseType)
    #response = models.PositiveSmallIntegerField(choices=RESPONSE_CHOICES)

    def __str__(self):
        return self.response.name
        default_permissions = ('add', 'change', 'delete', 'view')

    class Meta:
        unique_together = ('bushfire', 'response',)
        default_permissions = ('add', 'change', 'delete', 'view')



"""
Area Burnt/Forces
"""
@python_2_unicode_compatible
class AreaBurnt(models.Model):
    tenure = models.ForeignKey(Tenure, related_name='tenures')
    fuel_type = models.ForeignKey(FuelType, related_name='fuel_types') # vegetation_type was renamed to fuel_type in PBS
    #area = models.DecimalField(verbose_name="Area (ha)", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    #origin = models.BooleanField(verbose_name="Point of Origin", default=False)
    bushfire = models.ForeignKey(Bushfire, related_name='areas_burnt')

#    def clean(self):
#        if self.bushfire.areas_burnt.all().count() == 0:
#            raise ValidationError("You must enter one Area Burnt record")

    def to_json(self):
        return json.dumps(self.to_dict)

    def to_dict(self):
        #return dict(tenure=self.tenure.name, fuel_type=self.fuel_type.name, area=round(self.area,2), origin=self.origin)
        return dict(tenure=self.tenure.name, fuel_type=self.fuel_type.name)

    def __str__(self):
        #return 'Tenure: {}, Fuel Type: {}, Area: {}, Origin: {}'.format(
        #    self.tenure.name, self.fuel_type.name, self.area, self.origin)
        return 'Tenure: {}, Fuel Type: {}'.format(
            self.tenure.name, self.fuel_type.name)

    class Meta:
        unique_together = ('bushfire', 'tenure', 'fuel_type',)
        default_permissions = ('add', 'change', 'delete', 'view')


@python_2_unicode_compatible
class GroundForces(models.Model):
    GF_AGENCY_CHOICES = (
        (1, 'Initial DEC Dispatch'),
        (2, 'DEC Peak'),
        (3, 'Other Agencies Peak'),
    )

    name = models.PositiveSmallIntegerField(choices=GF_AGENCY_CHOICES, verbose_name="Agency Name", null=True, blank=True)
    persons = models.PositiveSmallIntegerField(null=True, blank=True)
    pumpers = models.PositiveSmallIntegerField(null=True, blank=True)
    plant = models.PositiveSmallIntegerField(null=True, blank=True)
    bushfire = models.ForeignKey(Bushfire, related_name='ground_forces')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('bushfire', 'name',)
        default_permissions = ('add', 'change', 'delete', 'view')


@python_2_unicode_compatible
class AerialForces(models.Model):
    AF_AGENCY_CHOICES = (
        (1, 'Fixed Wing'),
        (2, 'Helicopter'),
    )

    name = models.PositiveSmallIntegerField(choices=AF_AGENCY_CHOICES, verbose_name="Agency Name", null=True, blank=True)
    observer = models.PositiveSmallIntegerField(null=True, blank=True)
    transporter = models.PositiveSmallIntegerField(null=True, blank=True)
    ignition = models.PositiveSmallIntegerField(null=True, blank=True)
    water_bomber = models.PositiveSmallIntegerField(null=True, blank=True)
    bushfire = models.ForeignKey(Bushfire, related_name='aerial_forces')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('bushfire', 'name',)
        default_permissions = ('add', 'change', 'delete', 'view')

"""
Attendance/Behaviour
"""
@python_2_unicode_compatible
class FireBehaviour(models.Model):
    name = models.CharField(verbose_name="Name/Description", max_length=50, null=True, blank=True)
    fuel_type = models.ForeignKey(FuelType, related_name='fuel_types_fire', null=True, blank=True) # vegetation_type was renamed to fuel_type in PBS
    fuel_weight = models.PositiveSmallIntegerField(null=True, blank=True)
    fdi = models.PositiveSmallIntegerField(null=True, blank=True)
    ros = models.PositiveSmallIntegerField(null=True, blank=True)
    bushfire = models.ForeignKey(Bushfire, related_name='fire_behaviour')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('bushfire', 'name',)
        default_permissions = ('add', 'change', 'delete', 'view')


@python_2_unicode_compatible
class AttendingOrganisation(models.Model):
    name = models.ForeignKey('Organisation', null=True, blank=True)
    other = models.CharField(max_length=25, null=True, blank=True)
    bushfire = models.ForeignKey(Bushfire, related_name='attending_organisations')

    def clean_name(self):
        if self.name == 'Other' and not self.other:
            raise ValidationError("You must enter 'Other' attending organisation")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('bushfire', 'name',)
        default_permissions = ('add', 'change', 'delete', 'view')


"""
Damages/Legal
"""
@python_2_unicode_compatible
class Legal(models.Model):
    protection = models.PositiveSmallIntegerField(verbose_name="Community Protection (%)", validators=[MinValueValidator(0), MaxValueValidator(100)])
    cost = models.DecimalField(verbose_name="Est. Cost of Damages ($)", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    restricted_period = models.BooleanField(default=False)
    prohibited_period = models.BooleanField(default=False)
    inv_undertaken = models.ForeignKey(InvestigationType, verbose_name="Investigation Undertaken")
    legal_result = models.ForeignKey(LegalResultType)
    bushfire = models.ForeignKey(Bushfire, related_name='legal')

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.legal_result.name


@python_2_unicode_compatible
class PublicDamage(models.Model):
    damage_type = models.ForeignKey(PublicDamageType)
    fuel_type = models.ForeignKey(FuelType)
    area = models.DecimalField(verbose_name="Area (ha)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)])
    bushfire = models.ForeignKey(Bushfire, related_name='public_damages')

    def __str__(self):
        return self.damage_type

    class Meta:
        unique_together = ('bushfire', 'damage_type', 'fuel_type',)
        default_permissions = ('add', 'change', 'delete', 'view')


@python_2_unicode_compatible
class PrivateDamage(models.Model):
    damage_type = models.ForeignKey(PrivateDamageType)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    bushfire = models.ForeignKey(Bushfire, related_name='private_damages')

    def __str__(self):
        return self.damage_type

    class Meta:
        unique_together = ('bushfire', 'damage_type',)
        default_permissions = ('add', 'change', 'delete', 'view')


"""
Final Comments
"""
@python_2_unicode_compatible
class Comment(Audit):
    comment = models.TextField()
    bushfire = models.ForeignKey(Bushfire, related_name='comments')

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.comment


"""
Details
"""
#@python_2_unicode_compatible
#class Detail(models.Model):
#    CAUSE_CHOICES = (
#        (1, 'Known'),
#        (2, 'Possible'),
#    )
#
#    tenure = models.ForeignKey(Tenure)
#    fuel_type = models.ForeignKey(FuelType)
#    area = models.DecimalField(verbose_name="Area (ha)", max_digits=12, decimal_places=1, validators=[MinValueValidator(0)])
#
#    first_attack = models.ForeignKey(Agency)
#    other_agency = models.CharField(verbose_name='Other', max_length=25, null=True, blank=True)
#
#    # TODO form must include AttendingOrganisation list (choices is common, but info is different)
#    dec = models.BooleanField(verbose_name="DEC", default=False)
#    lga_bfb = models.BooleanField(verbose_name="LGA BFB", default=False)
#    fesa = models.BooleanField(verbose_name="FESA", default=False)
#    ses = models.BooleanField(verbose_name="SES", default=False)
#    police = models.BooleanField(verbose_name="POLICE", default=False)
#    other_force = models.CharField(verbose_name='Other', max_length=25, null=True, blank=True)
#
#    cause = models.ForeignKey(Cause)
#    known_possible = models.PositiveSmallIntegerField(choices=CAUSE_CHOICES, verbose_name="Known/Possible")
#    other_cause = models.CharField(verbose_name='Other', max_length=25, null=True, blank=True)
#    investigation_req = models.BooleanField(verbose_name="Invest'n Required", default=False)
#    bushfire = models.OneToOneField(Bushfire, related_name='detail')
#
#    def clean(self):
#        import ipdb; ipdb.set_trace()
#
#        if self.first_attack.name == 'OTHER' and not self.other_agency:
#            raise ValidationError("You must enter 'Other' Forces Agency")
#
#        if not (self.dec and self.lga_bfb and self.fesa and self.police) and len(self.other_force)==0:
#            raise ValidationError("You must specify an Attending Organisation or Other")
#
#        if self.cause.name == 'OTHER' and not self.other_cause:
#            raise ValidationError("You must enter 'Other' First Attack Agency")
#
#    def __str__(self):
#        return self.tenure.name


"""
Initial Comments
"""

#@python_2_unicode_compatible
#class Initial(Audit):
#    fuel = models.CharField(max_length=50)
#    ros = models.CharField(verbose_name="Rate of Spread", max_length=50)
#    flame_height = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
#    assistance_required = models.CharField(max_length=50)
#    fire_contained = models.BooleanField(default=False)
#    containment_time = models.CharField(verbose_name="ET to Contain", max_length=50)
#    ops_point = models.CharField(verbose_name="OPS Point (grid ref)", max_length=50)
#    communications = models.CharField(verbose_name='Communication', max_length=50)
#    weather = models.CharField(max_length=50)
#    field_officer = models.ForeignKey(User, verbose_name="Field Officer", related_name='field_officer')
#    authorised_by = models.ForeignKey(User, verbose_name="Authorising Officer", blank=True, null=True)
#    authorised_date = models.DateTimeField(default=timezone.now)
#
#    bushfire = models.OneToOneField(Bushfire, related_name='initial_report')
#
#    def user_unicode_patch(self):
#        """ overwrite the User model's __unicode__() method """
#        if self.first_name or self.last_name:
#            return '%s %s' % (self.first_name, self.last_name)
#        return self.username
#    User.__unicode__ = user_unicode_patch
#
#    def __str__(self):
#        return self.field_officer.get_full_name()


"""
Main Area
"""
@python_2_unicode_compatible
class Activity(models.Model):
    #activity = models.PositiveSmallIntegerField(choices=ACTIVITY_CHOICES)
    activity = models.ForeignKey(ActivityType)
    date = models.DateTimeField(default=timezone.now)
    bushfire = models.ForeignKey(Bushfire, related_name='activities')


    def to_json(self):
        return json.dumps(self.to_dict)

    def to_dict(self):
        return dict(name=self.activity.name, date=self.date.strftime('%Y-%m-%d %H:%M:%S'))

    def __str__(self):
        return self.activity.name

    class Meta:
#        ordering = ['activity']
        unique_together = ('bushfire', 'activity',)
        default_permissions = ('add', 'change', 'delete', 'view')


#@python_2_unicode_compatible
#class Activity2(models.Model):
#    #activity = models.PositiveSmallIntegerField(choices=ACTIVITY_CHOICES)
#    activity = models.ForeignKey(ActivityType)
#    date = models.DateTimeField(default=timezone.now)
#    bushfire = models.ForeignKey(BushfireTest2, related_name='activities2')
#
#    class Meta:
#        ordering = ['activity']
#
#    def __str__(self):
#        return self.activity.name
#
#    class Meta:
#        unique_together = ('bushfire', 'activity',)
#
#
#@python_2_unicode_compatible
#class Reporter(models.Model):
#
#    source = models.ForeignKey(Source, verbose_name="Reported By", null=True, blank=True)
#    cause = models.ForeignKey(Cause)
#    arson_squad_notified = models.BooleanField(verbose_name="Arson Squad Notified", default=False)
#    #prescription = models.ForeignKey(Prescription, verbose_name="ePFP (if cause is Escape)", related_name='prescribed_burn', null=True, blank=True)
#    prescription = models.ForeignKey(Prescription, verbose_name="Prescription Burn ID", null=True, blank=True)
#    offence_no = models.CharField(verbose_name="Offence No.", max_length=10)
#    bushfire = models.OneToOneField(Bushfire, related_name='reporting')
#
#    def __str__(self):
#        return self.offence_no


class BushfireTest(models.Model):
    region = models.ForeignKey(Region)
    district = ChainedForeignKey(
        District, chained_field="region", chained_model_field="region",
        show_all=False, auto_choose=True)


#class BushfireTest2(Audit):
class BushfireTest2(models.Model):

    FIRE_LEVEL_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )

    region = models.ForeignKey(Region)
    district = ChainedForeignKey(
        District, chained_field="region", chained_model_field="region",
        show_all=False, auto_choose=True)

    name = models.CharField(max_length=100, verbose_name="Fire Name")
    incident_no = models.CharField(verbose_name="Fire Incident No.", max_length=10)
    season = models.CharField(max_length=9)
    dfes_incident_no = models.CharField(verbose_name="DFES Incident No.", max_length=10)
    job_code = models.CharField(verbose_name="Job Code", max_length=10, null=True, blank=True)
    potential_fire_level = models.PositiveSmallIntegerField(choices=FIRE_LEVEL_CHOICES)

    init_authorised_by = models.ForeignKey(User, verbose_name="Authorised By", blank=True, null=True)
    init_authorised_date = models.DateTimeField(verbose_name='Authorised Date', default=timezone.now, null=True, blank=True)




