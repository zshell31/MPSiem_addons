import logging
import requests
from mpsiemlib.common import MPSIEMAuth


class Settings:
    connection_timeout = 60
    connection_timeout_x = 6  # коэф. увеличения timeout при генерауии отчета.
    storage_events_timezone = "UTC"  # в ES все события приведены к UTC
    local_timezone = "Europe/Moscow"  # в какой временной зоне работает скрипт
    storage_bucket_size = 33000  # размер бакета агрегации в Elastic (по умолчанию в конфиге 50000)
    storage_batch_size = 1000  # размер выгружаемой пачки событий без агрегации
    tables_batch_size = 1000  # размер выгружаемой пачки записей из табличек
    kb_objects_batch_size = 1000  # размер выгружаемой пачки правил из KB
    incidents_batch_size = 100  # размер выгружаемой пачки инцидентов
    source_monitor_batch_size = 100  # размер выгружаемой пачки источников


class AuthType:
    LOCAL = 0
    LDAP = 1


class ModuleNames:
    AUTH = "auth"
    EVENTS = "events"
    TABLES = "tables"
    FILTERS = "filters"
    TASKS = "tasks"
    HEALTH = "health"
    URM = "users_and_roles"
    KB = "knowledge_base"
    INCIDENTS = "incidents"
    SOURCE_MONITOR = "source_monitor"


class MPComponents:
    """
    Именование компонент. Должны совпадать с названиями в IAM
    """

    CORE = "mpx"
    SIEM = "siem"
    STORAGE = "storage"
    MS = "idmgr"
    KB = "ptkb"


class MPContentTypes:
    NORMALIZATION = "Normalization"
    AGGREGATION = "Aggregation"
    ENRICHMENT = "Enrichment"
    CORRELATION = "Correlation"
    TABLE = "TabularList"


class StorageVersion:
    ES7 = "7"
    ES17 = "1.7"
    ALL = "ALL"


class Creds:

    def __init__(self, params=None):
        self.__core_hostname = None
        self.__core_login = None
        self.__core_pass = None
        self.__siem_hostname = None
        self.__storage_hostname = None

        if params is not None:
            self.__core_hostname = params.get('core', {}).get('hostname', None)
            self.__core_login = params.get('core', {}).get('login', None)
            self.__core_pass = params.get('core', {}).get('pass', None)
            self.__core_auth_type = params.get('core', {}).get('auth_type', None)
            self.__siem_hostname = params.get('siem', {}).get('hostname', None)
            self.__storage_hostname = params.get('storage', {}).get('hostname', None)

    @property
    def core_hostname(self):
        return self.__core_hostname

    @core_hostname.setter
    def core_hostname(self, p):
        self.__core_hostname = p

    @property
    def core_login(self):
        return self.__core_login

    @core_login.setter
    def core_login(self, p):
        self.__core_login = p

    @property
    def core_pass(self):
        return self.__core_pass

    @core_pass.setter
    def core_pass(self, p):
        self.__core_pass = p

    @property
    def core_auth_type(self):
        return self.__core_auth_type

    @core_auth_type.setter
    def core_auth_type(self, p):
        if p not in [0, 1]:
            raise Exception('Auth Type must be 0 - Local or 1 - LDAP')
        self.__core_auth_type = p

    @property
    def siem_hostname(self):
        return self.__siem_hostname

    @siem_hostname.setter
    def siem_hostname(self, p):
        self.__siem_hostname = p

    @property
    def storage_hostname(self):
        return self.__storage_hostname

    @storage_hostname.setter
    def storage_hostname(self, p):
        self.__storage_hostname = p


class WorkerInterface:
    """
    Базовый интерфейс любого модуля для работы с MP SIEM
    """

    def __init__(self, creds: Creds, settings: Settings):
        self.creds = creds
        self.settings = settings

    def get_module(self, module_name: ModuleNames):
        """
        Получить экземпляр модуля
        :param module_name: имя модуля
        :return: экземпляр класса
        """
        pass


class ModuleInterface:

    def __init__(self, auth: MPSIEMAuth, settings: Settings):
        self.auth = auth
        self.settings = settings

    def close(self):
        pass


class AuthInterface:

    def __init__(self, creds: Creds, settings: Settings):
        self.creds = creds
        self.settings = settings

    def connect(self, component: MPComponents, creds: Creds = None) -> requests.Session:
        pass

    def disconnect(self):
        pass

    def get_session(self) -> requests.Session:
        pass

    def get_component(self) -> MPComponents:
        pass

    def get_creds(self) -> Creds:
        pass


class LoggingHandler:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
