# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Entdatatiingo(models.Model):
    stockid = models.CharField(primary_key=True, max_length=10)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    date = models.DateField()
    close_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    high_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    low_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    open_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    adj_close = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_high = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_low = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_open = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_volume = models.BigIntegerField(blank=True, null=True)
    div_cash = models.IntegerField(blank=True, null=True)
    split_factor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EntDataTiingo'
        unique_together = (('stockid', 'date'),)


class UDbDetails(models.Model):
    db_id = models.CharField(db_column='DB_ID', primary_key=True, max_length=16)  # Field name made lowercase.
    db_desc = models.CharField(db_column='DB_DESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT')  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_DB_DETAILS'
        unique_together = (('db_id', 'eff_start_dt'),)


class UElectronicAddress(models.Model):
    address = models.ForeignKey('USkeyAddress', models.DO_NOTHING, db_column='ADDRESS_ID', blank=True, null=True)  # Field name made lowercase.
    electronic_address = models.CharField(db_column='ELECTRONIC_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_ELECTRONIC_ADDRESS'


class UPlanDbDetails(models.Model):
    plan = models.OneToOneField('UPlanDetails', models.DO_NOTHING, db_column='PLAN_ID', primary_key=True)  # Field name made lowercase.
    db = models.ForeignKey(UDbDetails, models.DO_NOTHING, db_column='DB_ID')  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT')  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_PLAN_DB_DETAILS'
        unique_together = (('plan', 'db', 'eff_start_dt'),)


class UPlanDetails(models.Model):
    plan_id = models.CharField(db_column='PLAN_ID', primary_key=True, max_length=16)  # Field name made lowercase.
    plan_desc = models.CharField(db_column='PLAN_DESC', max_length=200, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_PLAN_DETAILS'


class UPostalAddress(models.Model):
    address = models.ForeignKey('USkeyAddress', models.DO_NOTHING, db_column='ADDRESS_ID', blank=True, null=True)  # Field name made lowercase.
    addr_line_1 = models.CharField(db_column='ADDR_LINE_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    addr_line_2 = models.CharField(db_column='ADDR_LINE_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    addr_line_3 = models.CharField(db_column='ADDR_LINE_3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=200, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=200, blank=True, null=True)  # Field name made lowercase.
    zip_cd = models.CharField(db_column='ZIP_CD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_POSTAL_ADDRESS'


class USkeyAddress(models.Model):
    address_id = models.CharField(db_column='ADDRESS_ID', primary_key=True, max_length=16)  # Field name made lowercase.
    source_key = models.CharField(db_column='SOURCE_KEY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    domain = models.CharField(db_column='DOMAIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    create_dt = models.DateTimeField(db_column='CREATE_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_SKEY_ADDRESS'


class UTelephoneAddress(models.Model):
    address = models.ForeignKey(USkeyAddress, models.DO_NOTHING, db_column='ADDRESS_ID', blank=True, null=True)  # Field name made lowercase.
    phone_country_cd = models.CharField(db_column='PHONE_COUNTRY_CD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    identification_cd = models.CharField(db_column='IDENTIFICATION_CD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subscriber_number = models.CharField(db_column='SUBSCRIBER_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_TELEPHONE_ADDRESS'


class UUserAddressDetails(models.Model):
    user = models.OneToOneField('UUserDetails', models.DO_NOTHING, db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    address = models.ForeignKey(USkeyAddress, models.DO_NOTHING, db_column='ADDRESS_ID')  # Field name made lowercase.
    addr_usage_type = models.CharField(db_column='ADDR_USAGE_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    user_addr_type_cd = models.CharField(db_column='USER_ADDR_TYPE_CD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_USER_ADDRESS_DETAILS'
        unique_together = (('user', 'address'),)


class UUserDbDetails(models.Model):
    user = models.OneToOneField('UUserDetails', models.DO_NOTHING, db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    db = models.ForeignKey(UDbDetails, models.DO_NOTHING, db_column='DB_ID')  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT')  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_USER_DB_DETAILS'
        unique_together = (('user', 'db', 'eff_start_dt'),)


class UUserDetails(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=40)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    first_nm = models.CharField(db_column='FIRST_NM', max_length=150, blank=True, null=True)  # Field name made lowercase.
    middle_nm = models.CharField(db_column='MIDDLE_NM', max_length=150, blank=True, null=True)  # Field name made lowercase.
    last_nm = models.CharField(db_column='LAST_NM', max_length=150, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_USER_DETAILS'


class UUserLoginDetails(models.Model):
    user_id = models.CharField(db_column='USER_ID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.
    user_enabled_flag = models.CharField(db_column='USER_ENABLED_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_USER_LOGIN_DETAILS'


class UUserPlanDetails(models.Model):
    user = models.OneToOneField(UUserDetails, models.DO_NOTHING, db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    plan = models.ForeignKey(UPlanDetails, models.DO_NOTHING, db_column='PLAN_ID')  # Field name made lowercase.
    eff_start_dt = models.DateTimeField(db_column='EFF_START_DT', blank=True, null=True)  # Field name made lowercase.
    eff_end_dt = models.DateTimeField(db_column='EFF_END_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'U_USER_PLAN_DETAILS'
        unique_together = (('user', 'plan'),)


class AdGtrend(models.Model):
    date = models.DateField(primary_key=True)
    unscaled = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    ispartial = models.CharField(max_length=10, blank=True, null=True)
    scale = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    g_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    stockid = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ad_gtrend'
        unique_together = (('date', 'stockid'),)


class AdWikiPgviews(models.Model):
    stockid = models.CharField(primary_key=True, max_length=10)
    date = models.DateField()
    pageviews = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'ad_wiki_pgviews'
        unique_together = (('stockid', 'date'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoPlotlyDashDashapp(models.Model):
    id = models.BigAutoField(primary_key=True)
    instance_name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=110)
    base_state = models.TextField()
    creation = models.DateTimeField()
    update = models.DateTimeField()
    save_on_change = models.IntegerField()
    stateless_app = models.ForeignKey('DjangoPlotlyDashStatelessapp', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_plotly_dash_dashapp'


class DjangoPlotlyDashStatelessapp(models.Model):
    id = models.BigAutoField(primary_key=True)
    app_name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=110)

    class Meta:
        managed = False
        db_table = 'django_plotly_dash_statelessapp'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EntertainmentTickerinfo(models.Model):
    serial_no = models.IntegerField(blank=True, null=True)
    stockid = models.CharField(primary_key=True, max_length=10)
    stock_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entertainment_tickerinfo'


class FbDailyData(models.Model):
    date = models.DateField(primary_key=True)
    stockid = models.CharField(max_length=20)
    fb_likes = models.IntegerField(blank=True, null=True)
    fb_followers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fb_daily_data'
        unique_together = (('date', 'stockid'),)


class PredictInfo(models.Model):
    stockid = models.CharField(primary_key=True, max_length=20)
    date = models.DateField()
    predicted_value = models.FloatField(blank=True, null=True)
    mape = models.FloatField(blank=True, null=True)
    model_score = models.FloatField(blank=True, null=True)
    stan_dev = models.FloatField(blank=True, null=True)
    sharpe_ratio = models.FloatField(blank=True, null=True)
    sortino_ratio = models.FloatField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'predict_info'
        unique_together = (('stockid', 'date'),)



class RedditDailyData(models.Model):
    date = models.DateField(primary_key=True)
    stockid = models.CharField(max_length=20)
    redditmention = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'reddit_daily_data'
        unique_together = (('date', 'stockid'),)


class SAlphaTable(models.Model):
    stockid = models.CharField(max_length=10)
    date = models.DateField()
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    open_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    close_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    low_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    high_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    wiki_pageviews = models.IntegerField(blank=True, null=True)
    fb_followers = models.IntegerField(blank=True, null=True)
    fb_likes = models.IntegerField(blank=True, null=True)
    twitterfollower = models.IntegerField(blank=True, null=True)
    redditmention = models.IntegerField(blank=True, null=True)
    gics_sector = models.CharField(max_length=45, blank=True, null=True)
    gics_sub_industry = models.CharField(max_length=45, blank=True, null=True)
    predicted_value = models.FloatField()
    mape = models.FloatField(blank=True, null=True)
    model_score = models.FloatField(blank=True, null=True)
    stan_dev = models.FloatField(blank=True, null=True)
    sharpe_ratio = models.FloatField(blank=True, null=True)
    sortino_ratio = models.FloatField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 's_alpha_table'


class Snp500StockDaily(models.Model):
    stockid = models.CharField(primary_key=True, max_length=10)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    date = models.DateField()
    close_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    high_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    low_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    open_value = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    adj_close = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_high = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_low = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_open = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    adj_volume = models.BigIntegerField(blank=True, null=True)
    div_cash = models.IntegerField(blank=True, null=True)
    split_factor = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'snp500_stock_daily'
        unique_together = (('stockid', 'date'),)


class Snp500StockInfo(models.Model):
    stockid = models.CharField(primary_key=True, max_length=10)
    stock_name = models.CharField(max_length=45, blank=True, null=True)
    sec_filings = models.CharField(max_length=45, blank=True, null=True)
    gics_sector = models.CharField(max_length=45, blank=True, null=True)
    gics_sub_industry = models.CharField(max_length=45, blank=True, null=True)
    headquater = models.CharField(max_length=45, blank=True, null=True)
    date_first_added = models.CharField(max_length=45, blank=True, null=True)
    cik = models.IntegerField(blank=True, null=True)
    founded_year = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'snp500_stock_info'


class TwitterDailyData(models.Model):
    date = models.DateField(primary_key=True)
    stockid = models.CharField(max_length=20)
    twitterfollower = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'twitter_daily_data'
        unique_together = (('date', 'stockid'),)
