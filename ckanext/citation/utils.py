import inspect
import os

m = __import__("ckanext.citation", fromlist=[""])
P = os.path.join(
    os.path.dirname(inspect.getfile(m)), "public", "ckanext", "citation", "csl"
)
CSL_P = os.path.join(P, "styles")
