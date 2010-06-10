from settings import *

try:
   from local_settings import *
except ImportError:
   pass

try:
   from production_settings import *
except ImportError:
   pass


TEMPLATE_DIRS = (
	"/Users/Jeje/Documents/Django_Projects/UniformZulu/aec.monppl.com/templates",
	"/Users/Jeje/Documents/Django_Projects/UniformZulu/templates",
)
