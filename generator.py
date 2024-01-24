import random
import string

FIELD_TYPES = (
    "smallint",
    "integer",
    "bigint",
    "decimal",
    "Numeric",
    "Double precision",
    "serial",
    "Bigserial",
    "text",
    "money",
    "bytea",
    "Boolean",
    "cidr",
    "inet",
    "macaddr",
    "Tsvector",
    "Tsquery",
    "UUID",
    "XML",
    "JSON",
    "timestamp",
    "TIMESTAMPTZ",
    "date",
    "time",
    "point",
    "line",
    "lseg",
    "box",
    "path",
    "polygon",
    "Circle",
    "int4range",
    "int8range",
    "numrange",
    "tsrange",
    "tstzrange",
    "daterange",
    "bit(1024)",
    "bit varying(10)",
    "char(64)",
    "character(64)",
    "varchar(1024)",
    "character varying(1024)"
)

FIELD_TYPES_VAR= (
    "bit(n)",
    "bit varying(n)",
    "char(size)",
    "character(size)",
    "varchar(size)",
    "character varying(size)"
)

MAX_NAME_LENGTH = 64
MAX_COL_NUMBER = 1600
DEFAULT_COL_NUMBER = 10


class SqlGenerator:
    def __init__(self):
        pass

    def get_fields_type(self):
        return FIELD_TYPES

    def random_correct_name(self, len = 0):
        """ Returns string consisting from random ascii letters and digits,
        starting from an ascii letter. Length of string is equal to len  if defined,
        otherwise is random value from 1 to 64    """

        if len>0 and len<=64:
            count = len
        else:
            count = random.randrange(1,MAX_NAME_LENGTH+1)
        first_letter = random.choice(string.ascii_letters)
        symbols = string.ascii_letters + string.digits +"$"
        return first_letter + "".join([random.choice(symbols) for i in range(random.randrange(1,count+1))])

    def random_wrong_name(self, len = MAX_NAME_LENGTH):
        """ Returns string consisting from random non-ascii symbols.
        Length of string is equal to len  if defined,
        otherwis random value from 1 to 64  """

        count = MAX_NAME_LENGTH -1
        if len>0 and len<64:
            count = len -1
        first_letter = random.choice(string.ascii_letters)
        wrongsymbols = string.punctuation + string.whitespace
        wrong_letter = random.choice(wrongsymbols)
        place = random.choice(random.randrange(2,count-1))
        symbols = "".join([random.choice(string.ascii_letters) for i in range(random.randrange(1,count+1))])

        return first_letter + symbols[:place] + wrong_letter + symbols[place:]

    def random_correct_fields(self, fields_number = 0, fields_type = ""):
        """ Returns list of valid field descriptions like
        ["fieldname1 fieldtype1", "fieldname2 fieldtype2", .. "fieldnameN fieldtypeN"]
         where N is field_number if defined, otherwise random value from 1 to 1600,
         fieldtypen is fields_type for all fileds if defined, otherwise random type from FIELD_TYPES
        """
        if fields_number > 0 and fields_number <= MAX_COL_NUMBER:
            count = fields_number
        else:
            count = random.randrange(1, MAX_COL_NUMBER + 1)

        result = []
        for i in range(count):
            result.append(self.random_correct_name() + " " +
                          (random.choice(FIELD_TYPES) if fields_type == "" else fields_type))
        return result
