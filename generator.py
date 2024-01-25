import random
import string

FIELD_TYPES = (
    "smallint",
    "integer",
    "bigint",
    "decimal",
    "Numeric",
    "Double precision",
#    "serial",  can be only first
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
PSYMBOLS = "%!#$%&()*+,-./:;<=>?@[\]^`{|~ "   #removed from spec symbols: ", '
NAME_EXCEPTIONS = ("OR", "AND", "IS", "AS", "AT", "BY", "ON", "DO", "IN", "GO", "IF", "LN", "NO",
                   "OR", "TO", "XOR", "USE", "UID", "TOP", "SUM", "SSL", "SET", "REF", "ROW", "PLI", "PAD",
                    "OUT", "OLD", "OFF", "NOT", "MIN", "MAX", "MAP", "KEY", "INT", "GET", "FOR", "EXP",
                    "END", "DIV"," DEC", "CSV", "BIT", "AVG", "ASC", "ARE", "ANY", "ALL", "ADD", "ADA", "ABS")

class SqlGenerator:
    def __init__(self):
        pass

    def get_fields_type(self):
        return FIELD_TYPES

    def get_special_symbols(self):
        return PSYMBOLS

    def random_correct_name(self, len = 0):
        """ Returns string consisting from random ascii letters and digits,
        starting from an ascii letter. Length of string is equal to len  if defined,
        otherwise is random value from 1 to 64    """

        if len>0 and len<=64:
            count = len
        else:
            count = random.randrange(1,MAX_NAME_LENGTH+1)
        first_letter = random.choice(string.ascii_letters)
        symbols = string.ascii_letters + string.digits #+"$_" #}
        if count == 1:
            name = first_letter
        else:
            name = first_letter + "".join([random.choice(symbols) for i in range(count-2)])

        while name.upper() in NAME_EXCEPTIONS:
            name = self.random_correct_name()
        return name

    def random_wrong_name(self, len = 0, wsymbol = ""):
        """ Returns string that contains wsymbol or a random non-ascii symbol,
        if wsymbol is not defined.
        Length of string (>=2) is equal to len  if defined,
        otherwise random value from 2 to 64  """
        if len>1 and len<=64:
            count = len
        else:
            count = random.randrange(2,MAX_NAME_LENGTH)
        first_letter = random.choice(string.ascii_letters)
        if wsymbol == "":
            wrong_letter = random.choice(PSYMBOLS)
        else:
            wrong_letter = wsymbol

        symbols = "".join([random.choice(string.ascii_letters) for i in range(count)])

        place = 1 if count < 3 else random.choice(range(random.randrange(1,count)))

        return first_letter + symbols[:place] + wrong_letter + symbols[place:]

    def random_correct_fields(self, fields_number = 0, fields_type = ""):
        """ Returns list of valid field descriptions like
        ["fieldname1 fieldtype1", "fieldname2 fieldtype2", .. "fieldnameN fieldtypeN"]
         where N is field_number if defined, otherwise random value from 1 to 1600,
         fieldtypen is fields_type for all fileds if defined, otherwise random type from FIELD_TYPES
        """
        if fields_number > 0: #and fields_number <= MAX_COL_NUMBER:
            count = fields_number
        else:
            count = random.randrange(1, MAX_COL_NUMBER + 1)
        i = 0
        result = []
        namelist = []

        for i in range(count):
            name = self.random_correct_name()
            while name.lower() in namelist:
                name = self.random_correct_name()
            result.append(name + " " + (random.choice(FIELD_TYPES) if fields_type == "" else fields_type))
            namelist.append(name.lower())

        return result
